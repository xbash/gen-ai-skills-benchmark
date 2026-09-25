import argparse
import json
import subprocess
import tempfile
import time
from pathlib import Path

from runner import resolve_codex


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "benchmark.config.json"
RESULTS = ROOT / "results"
CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
CONFIG["codex_command"] = resolve_codex(CONFIG["codex_command"])

RUBRIC = (
    "Eval\u00faa AN\u00d3NIMAMENTE esta respuesta. No premies longitud ni que mencione una "
    "skill. Punt\u00faa 0,1,2: cobertura, evidencia, fuentes, trazabilidad, "
    "riesgos_limitaciones, aplicabilidad. Devuelve SOLO JSON valido: "
    '{"cobertura":N,"evidencia":N,"fuentes":N,"trazabilidad":N,'
    '"riesgos_limitaciones":N,"aplicabilidad":N,"Q":N,'
    '"justificacion_breve":"..."}. RESPUESTA:\n---\n%s\n---'
)
SCORES = (
    "cobertura",
    "evidencia",
    "fuentes",
    "trazabilidad",
    "riesgos_limitaciones",
    "aplicabilidad",
)


def parse_events(text):
    events = []
    for line in text.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def final_message(events):
    messages = []
    for event in events:
        if event.get("type") != "item.completed":
            continue
        item = event.get("item", {})
        if item.get("type") == "agent_message" and isinstance(item.get("text"), str):
            messages.append(item["text"])
    return messages[-1] if messages else ""


def parse_json_response(text):
    """Parse a JSON object without a greedy regex fallback."""
    decoder = json.JSONDecoder()
    stripped = text.strip()
    try:
        value, end = decoder.raw_decode(stripped)
        if isinstance(value, dict) and not stripped[end:].strip():
            return value
    except json.JSONDecodeError:
        pass

    for index, character in enumerate(text):
        if character != "{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return {"_parse_error": True, "_raw": text}


def judge_command(model, effort):
    return [
        CONFIG["codex_command"],
        "exec",
        "--json",
        "--model",
        model,
        "--sandbox",
        "read-only",
        "-c",
        f'model_reasoning_effort="{effort}"',
        "--skip-git-repo-check",
        "-",
    ]


def score_result(result, process, events, model, effort, elapsed):
    values = [result.get(key) for key in SCORES]
    valid = process.returncode == 0 and all(
        type(value) is int and 0 <= value <= 2 for value in values
    )
    if valid:
        result["Q"] = sum(values)
    else:
        result.pop("Q", None)
        result["_invalid_evaluation"] = True
    result["_judge_exit_code"] = process.returncode
    result["_judge_usage"] = next(
        (
            event.get("usage", {})
            for event in reversed(events)
            if event.get("type") == "turn.completed"
        ),
        {},
    )
    result["_judge_model"] = model
    result["_judge_effort"] = effort
    result["_judge_elapsed_seconds"] = round(elapsed, 3)
    return result


def judge_experiment(experiment):
    judge_config = CONFIG.get("judge", {})
    model = judge_config.get("model", "gpt-5.6-luna")
    effort = judge_config.get("reasoning_effort", "medium")
    timeout = int(judge_config.get("timeout_seconds", 900))
    result_dirs = sorted(
        meta_path.parent
        for meta_path in RESULTS.rglob("meta.json")
        if not any(part in {"_archive", "_attempts"} for part in meta_path.parts)
        and json.loads(meta_path.read_text(encoding="utf-8")).get("experiment") == experiment
    )
    if not result_dirs:
        raise FileNotFoundError(f"No existen resultados para el experimento: {experiment}")

    with tempfile.TemporaryDirectory(prefix="genai-judge-") as temporary_dir:
        for result_dir in result_dirs:
            final_path = result_dir / "final.txt"
            judge_path = result_dir / "judge.json"
            if not final_path.is_file() or not final_path.read_text(encoding="utf-8").strip():
                continue
            if judge_path.exists():
                continue
            meta = json.loads((result_dir / "meta.json").read_text(encoding="utf-8"))
            if meta.get("exit_code") != 0 or meta.get("timed_out") or meta.get("dry_run"):
                continue

            prompt = RUBRIC % final_path.read_text(encoding="utf-8", errors="replace")
            started = time.perf_counter()
            process = subprocess.run(
                judge_command(model, effort),
                cwd=temporary_dir,
                input=prompt,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )
            events = parse_events(process.stdout or "")
            result = parse_json_response(final_message(events))
            result = score_result(
                result,
                process,
                events,
                model,
                effort,
                time.perf_counter() - started,
            )
            judge_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
            (result_dir / "judge.jsonl").write_text(process.stdout or "", encoding="utf-8")
            (result_dir / "judge.stderr.txt").write_text(process.stderr or "", encoding="utf-8")
            print(result_dir.name, result.get("Q"), flush=True)
            if process.returncode != 0:
                raise SystemExit(f"Juez detenido: {result_dir.name}, exit_code={process.returncode}")


def main():
    parser = argparse.ArgumentParser(description="Evalua respuestas de un experimento.")
    parser.add_argument("experiment", help="Nombre del experimento bajo results/")
    args = parser.parse_args()
    judge_experiment(args.experiment)


if __name__ == "__main__":
    main()
