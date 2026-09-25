import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

RESULTS = Path(__file__).resolve().parents[1] / "results"
ARCHIVED_DIRS = {"_archive", "_attempts"}


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def is_archived(path):
    return any(part in ARCHIVED_DIRS for part in path.parts)


def load_rows():
    rows = []
    for meta_path in RESULTS.rglob("meta.json"):
        if is_archived(meta_path):
            continue
        meta = read_json(meta_path)
        if meta.get("dry_run"):
            continue
        result_dir = meta_path.parent
        usage = meta.get("usage") or {}
        trace = read_json(result_dir / "trace.json")
        judge = read_json(result_dir / "judge.json")
        input_tokens = usage.get("input_tokens")
        cached_tokens = usage.get("cached_input_tokens", 0) or 0
        output_tokens = usage.get("output_tokens")
        total_tokens = (
            input_tokens + output_tokens
            if isinstance(input_tokens, (int, float))
            and isinstance(output_tokens, (int, float))
            else None
        )
        quality = judge.get("Q")
        efficiency = (
            quality / (total_tokens / 1000)
            if isinstance(quality, (int, float)) and total_tokens
            else None
        )
        rows.append(
            {
                "experiment": meta.get("experiment"),
                "condition": meta.get("condition"),
                "run_id": meta.get("run_id"),
                "model": meta.get("model"),
                "reasoning_effort": meta.get("reasoning_effort"),
                "elapsed_seconds": meta.get("elapsed_seconds"),
                "exit_code": meta.get("exit_code"),
                "input_tokens": input_tokens,
                "cached_input_tokens": cached_tokens,
                "uncached_input_tokens": (
                    input_tokens - cached_tokens
                    if isinstance(input_tokens, (int, float))
                    else None
                ),
                "output_tokens": output_tokens,
                "reasoning_output_tokens": usage.get("reasoning_output_tokens"),
                "total_reported_tokens": total_tokens,
                "deep_research_used": trace.get("deep_research_used"),
                "agents_md_seen": trace.get("agents_md_seen"),
                "external_sources_count": trace.get("external_sources_count"),
                "primary_sources_count": trace.get("primary_sources_count"),
                "Q": quality,
                "E_Q": round(efficiency, 4) if efficiency is not None else None,
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            str(row["experiment"]),
            str(row["condition"]),
            str(row["model"]),
            str(row["reasoning_effort"]),
            str(row["run_id"]),
        ),
    )


def average(values):
    numbers = [value for value in values if isinstance(value, (int, float))]
    return sum(numbers) / len(numbers) if numbers else None


def fmt(value, decimals=1):
    return "" if value is None else f"{value:.{decimals}f}"


def build_summary(rows):
    groups = defaultdict(list)
    for row in rows:
        key = (
            row["experiment"],
            row["condition"],
            row["model"],
            row["reasoning_effort"],
        )
        groups[key].append(row)

    lines = [
        "# Benchmark summary",
        "",
        "Las medias usan corridas con exit_code=0 y se separan por modelo y esfuerzo. "
        "Este resumen es descriptivo; no demuestra causalidad ni ahorro generalizable.",
        "",
        "| Experimento | Condición | Modelo | Esfuerzo | Completadas | Fallidas | Tokens prom. | DE tokens | Tiempo prom. s | Q prom. | n con Q |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for (experiment, condition, model, effort), group in sorted(groups.items()):
        failed = sum(row["exit_code"] != 0 for row in group)
        successful = [row for row in group if row["exit_code"] == 0]
        token_values = [
            row["total_reported_tokens"]
            for row in successful
            if isinstance(row["total_reported_tokens"], (int, float))
        ]
        token_sd = statistics.stdev(token_values) if len(token_values) > 1 else None
        quality_values = [row["Q"] for row in successful]
        lines.append(
            f"| {experiment} | {condition} | {model or ''} | {effort or ''} | "
            f"{len(successful)} | {failed} | "
            f"{fmt(average(token_values), 0)} | {fmt(token_sd, 0)} | "
            f"{fmt(average([row['elapsed_seconds'] for row in successful]), 1)} | "
            f"{fmt(average(quality_values), 2)} | "
            f"{sum(isinstance(value, (int, float)) for value in quality_values)} |"
        )
    return "\n".join(lines) + "\n"


def main():
    rows = load_rows()
    fields = list(rows[0].keys()) if rows else ["experiment", "condition", "run_id"]
    with (RESULTS / "summary.csv").open("w", newline="", encoding="utf-8-sig") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    (RESULTS / "summary.md").write_text(build_summary(rows), encoding="utf-8")
    print(RESULTS / "summary.csv")
    print(RESULTS / "summary.md")


if __name__ == "__main__":
    main()
