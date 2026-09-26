from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / 'benchmark.config.json'
RESULTS = ROOT / 'results'
FIX = ROOT / 'fixtures'
PROMPTS = ROOT / 'prompts'
EXPS = ROOT / 'experiments'


def J(path):
    return json.loads(path.read_text(encoding='utf-8'))


def iso():
    return datetime.now(timezone.utc).astimezone().isoformat()


def safe_component(value):
    return ''.join(
        ch if ch.isalnum() or ch in ('-', '_', '.') else '_'
        for ch in str(value)
    )


def result_root(c, experiment, dry=False):
    base = ROOT / 'output' / 'dry-run' if dry else RESULTS
    cohort = c.get('cohort_id')

    if not cohort:
        return base / experiment

    return (
        base
        / safe_component(cohort)
        / safe_component(c['model'])
        / safe_component(c['reasoning_effort'])
        / experiment
    )


def workspace_root(c, experiment, dry=False):
    base = ROOT / '.workspaces' / 'dry-run' if dry else ROOT / '.workspaces'
    cohort = c.get('cohort_id')

    if not cohort:
        return base / experiment

    return (
        base
        / safe_component(cohort)
        / safe_component(c['model'])
        / safe_component(c['reasoning_effort'])
        / experiment
    )
def resolve_codex(command):
    found = shutil.which(str(command))
    if found:
        return found

    candidates = []
    user = Path(os.environ.get('USERPROFILE', ''))
    for base in (
        user / '.vscode' / 'extensions',
        user / '.vscode-insiders' / 'extensions',
    ):
        candidates.extend(
            base.glob('openai.chatgpt-*/bin/windows-x86_64/codex.exe')
        )

    if candidates:
        return str(max(candidates, key=lambda path: path.stat().st_mtime))
    raise FileNotFoundError(
        'No se encontró el comando Codex en PATH ni en la extensión OpenAI de VS Code'
    )


def codex_argv(c, *args):
    """Construye el comando portable para invocar Codex CLI.

    En Windows, una instalación npm suele resolver `codex` a `codex.CMD`;
    CreateProcess no ejecuta directamente wrappers .CMD, por lo que se
    invocan explícitamente mediante cmd.exe.
    """
    command = str(c['codex_command'])
    argv = [command, *map(str, args)]

    if os.name == 'nt' and Path(command).suffix.lower() in ('.cmd', '.bat'):
        return ['cmd.exe', '/d', '/s', '/c', *argv]

    return argv


def run_codex(c, *args, **kwargs):
    """Ejecuta Codex conservando un único punto de invocación."""
    return subprocess.run(codex_argv(c, *args), **kwargs)


def doctor(c):
    src = Path(c['source_repo'])
    required = c.get('required_files', ['AGENTS.md', 'README.md'])

    print('root:', ROOT)
    print('repo:', src, 'exists=', src.exists())

    checks = {
        item: (src / item).is_file() if src.exists() else False
        for item in required
    }
    for item, exists in checks.items():
        print(f'required[{item}]=', exists)

    try:
        p = run_codex(
            c,
            '--version',
            text=True,
            capture_output=True,
            timeout=20,
        )
        print('codex:', (p.stdout or p.stderr).strip())
        if p.returncode:
            return 2

        auth = run_codex(
            c,
            'login',
            'status',
            text=True,
            capture_output=True,
            timeout=20,
        )
        print('auth:', (auth.stdout or auth.stderr).strip())
        if auth.returncode:
            return 2
    except Exception as e:
        print('ERROR codex:', e)
        return 2

    print('model=', c['model'], 'effort=', c['reasoning_effort'])
    return 0 if src.exists() and all(checks.values()) else 2
def copyrepo(src, dst):
    shutil.copytree(
        src,
        dst,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(
            '.git',
            '.venv',
            'node_modules',
            '__pycache__',
            '.pytest_cache',
            'results',
            '.workspaces',
        ),
    )


def prep(c, mode, agents, dst):
    dst.mkdir(parents=True, exist_ok=True)

    if mode == 'full':
        src = Path(c['source_repo'])
        if not src.exists():
            raise FileNotFoundError(src)
        copyrepo(src, dst)
    elif mode not in ('empty', 'agents_only'):
        raise ValueError(mode)

    ap = dst / 'AGENTS.md'
    if agents == 'none':
        if ap.exists():
            ap.unlink()
    elif agents in ('baseline', 'routed', 'resume'):
        shutil.copy2(FIX / f'AGENTS.{agents}.md', ap)
    else:
        raise ValueError(agents)
def parse(path):
    events = []
    usage = {}
    thread_id = None

    if not path.exists():
        return events, usage, thread_id

    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        try:
            event = json.loads(line)
        except Exception:
            continue

        events.append(event)
        if event.get('type') == 'thread.started':
            thread_id = event.get('thread_id', thread_id)
        if event.get('type') == 'turn.completed' and isinstance(
            event.get('usage'), dict
        ):
            usage = event['usage']

    return events, usage, thread_id


def final(events):
    messages = []

    for event in events:
        if event.get('type') != 'item.completed':
            continue

        item = event.get('item', {})
        if item.get('type') == 'agent_message' and isinstance(
            item.get('text'), str
        ):
            messages.append(item['text'])

    return messages[-1] if messages else ''


def trace(text):
    for line in reversed(text.splitlines()):
        if not line.strip().startswith('TRACE_JSON:'):
            continue

        raw = line.split('TRACE_JSON:', 1)[1].strip()
        try:
            return json.loads(raw)
        except Exception:
            return {'_parse_error': True, '_raw': raw}

    return None


def cmd(c, prompt):
    return codex_argv(
        c,
        'exec',
        '--json',
        '--model',
        c['model'],
        '--sandbox',
        c.get('sandbox', 'read-only'),
        '-c',
        f'model_reasoning_effort="{c["reasoning_effort"]}"',
        '--skip-git-repo-check',
        '-',
    )
def onerun(c,en,cond,idx,mode,agents,pf,dry=False):
    rid = f'{cond}-{idx:02d}'
    rd = result_root(c, en, dry) / cond / rid

    if not dry and (rd / 'meta.json').exists():
        raise FileExistsError(
            f'Corrida existente: {rd}. Archiva los resultados antes de repetir.'
        )

    rd.mkdir(parents=True, exist_ok=True)
    prompt = (PROMPTS / pf).read_text(encoding='utf-8')
    (rd / 'prompt.txt').write_text(prompt, encoding='utf-8')
    ws = workspace_root(c, en, dry) / rid

    if not ws.resolve().is_relative_to((ROOT / '.workspaces').resolve()):
        raise ValueError('Workspace fuera del directorio permitido')
    if ws.exists():
        shutil.rmtree(ws)

    prep(c, mode, agents, ws)
    meta = {
        'experiment': en,
        'condition': cond,
        'run_id': rid,
        'workspace_mode': mode,
        'agents_variant': agents,
        'prompt_file': pf,
        'model': c['model'],
        'reasoning_effort': c['reasoning_effort'],
        'started_at': iso(),
    }
    cc = cmd(c, prompt)
    (rd / 'command.json').write_text(
        json.dumps(cc, indent=2, ensure_ascii=False), encoding='utf-8'
    )

    if dry:
        meta['dry_run'] = True
        (rd / 'meta.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
        print('[DRY]', en, rid)
        return

    t = time.perf_counter()
    try:
        with (
            (rd / 'codex.jsonl').open('w', encoding='utf-8') as out,
            (rd / 'stderr.txt').open('w', encoding='utf-8') as err,
        ):
            p = subprocess.run(
                cc,
                cwd=ws,
                input=prompt,
                text=True,
                encoding='utf-8',
                stdout=out,
                stderr=err,
                timeout=int(c.get('timeout_seconds', 1200)),
            )
    except subprocess.TimeoutExpired:
        meta.update({
            'elapsed_seconds': round(time.perf_counter() - t, 3),
            'timed_out': True,
            'exit_code': None,
        })
        (rd / 'meta.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
        print('[TIMEOUT]', en, rid, flush=True)
        return False
    except OSError as e:
        meta.update({
            'finished_at': iso(),
            'elapsed_seconds': round(time.perf_counter() - t, 3),
            'timed_out': False,
            'exit_code': None,
            'execution_status': 'process_error',
            'error_type': type(e).__name__,
            'error': str(e),
        })
        (rd / 'meta.json').write_text(
            json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8'
        )
        print('[ERROR]', en, rid, type(e).__name__, str(e), flush=True)
        if not c.get('keep_workspaces', False):
            shutil.rmtree(ws, ignore_errors=True)
        return False

    ev, u, tid = parse(rd / 'codex.jsonl')
    ft = final(ev)
    (rd / 'final.txt').write_text(ft, encoding='utf-8')
    tr = trace(ft)
    if tr is not None:
        (rd / 'trace.json').write_text(
            json.dumps(tr, indent=2, ensure_ascii=False), encoding='utf-8'
        )

    meta.update({
        'finished_at': iso(),
        'elapsed_seconds': round(time.perf_counter() - t, 3),
        'timed_out': False,
        'exit_code': p.returncode,
        'execution_status': 'success' if p.returncode == 0 else 'codex_exit_error',
        'thread_id': tid,
        'event_count': len(ev),
        'usage': u,
    })
    (rd / 'meta.json').write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8'
    )
    print('[OK]' if p.returncode == 0 else '[FAIL]', en, rid, u)

    if not c.get('keep_workspaces', False):
        shutil.rmtree(ws, ignore_errors=True)
    return p.returncode == 0
def runexp(c,n,dry=False,resume=False,limit=None):
    s = J(EXPS / f'{n}.json')
    c = dict(c)
    c['timeout_seconds'] = s.get(
        'timeout_seconds', c.get('timeout_seconds', 1200)
    )
    print('\n===', n, s.get('description', ''), '===', flush=True)
    completed = 0

    for b in s['runs']:
        for i in range(1, int(b['repetitions']) + 1):
            mp = (
                result_root(c, n, dry)
                / b['condition']
                / f"{b['condition']}-{i:02d}"
                / 'meta.json'
            )
            if resume and not dry and mp.exists():
                m = J(mp)
                if (
                    m.get('exit_code') == 0
                    and not m.get('timed_out')
                    and not m.get('dry_run')
                ):
                    print('[SKIP]', n, m.get('run_id'), flush=True)
                    continue

                rd = mp.parent
                attempts = RESULTS / '_attempts' / n / b['condition']
                attempts.mkdir(parents=True, exist_ok=True)
                stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                archived = attempts / f'{rd.name}-{stamp}'
                if not rd.resolve().is_relative_to(RESULTS.resolve()):
                    raise ValueError('Ruta de archivo fuera de results')
                if not archived.resolve().is_relative_to(
                    (RESULTS / '_attempts').resolve()
                ):
                    raise ValueError('Ruta de archivo fuera de results')
                shutil.move(str(rd), str(archived))
                print('[ARCHIVE]', rd.name, '->', archived.relative_to(ROOT), flush=True)

            if limit is not None and completed >= limit:
                return

            ok = onerun(
                c, n, b['condition'], i, b['workspace'], b['agents'], b['prompt'], dry
            )
            completed += 1
            if ok is False and s.get('stop_on_failure', False):
                raise SystemExit(
                    'Experimento detenido: corrida fallida; revisar logs antes de continuar.'
                )
def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd', required=True)
    subparsers.add_parser('doctor')
    subparsers.add_parser('list')
    run_parser = subparsers.add_parser('run')
    run_parser.add_argument('experiment')
    run_parser.add_argument('--dry-run', action='store_true')
    run_parser.add_argument('--resume', action='store_true')
    run_parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    config = J(CFG)

    try:
        config['codex_command'] = resolve_codex(config['codex_command'])
    except Exception as e:
        print('ERROR codex:', e)
        raise SystemExit(2)

    if args.cmd == 'doctor':
        raise SystemExit(doctor(config))

    names = [p.stem for p in sorted(EXPS.glob('*.json'))]
    if args.cmd == 'list':
        for name in names:
            print(name, '-', J(EXPS / f'{name}.json').get('description', ''))
    elif args.cmd == 'run':
        if args.limit is not None and args.limit < 1:
            raise SystemExit('--limit debe ser positivo')

        targets = names if args.experiment == 'all' else [args.experiment]
        for name in targets:
            if name not in names:
                raise SystemExit('Experimento desconocido: ' + name)
            runexp(config, name, args.dry_run, args.resume, args.limit)
if __name__=='__main__':main()
