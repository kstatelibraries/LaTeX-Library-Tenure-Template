#!/usr/bin/env python3
"""Build both document roots with retained logs; never modify source inputs.

Run from any directory. --verbose streams subprocess output in addition to
saving it. Each invocation truncates its driver logs to avoid stale diagnostics.
"""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
FATAL = re.compile(r'^!|undefined (?:citation|reference)|(?:Citation|Reference).*undefined|^ERROR|^.*?:[0-9]+: (?:Undefined control sequence|.*Error)|Fatal error occurred', re.I)
WARNING = re.compile(r'\bWarning:|\bWARN\b|Overfull|Underfull', re.I)


def audit(directory, stem):
    """Require native logs and PDF, keeping layout warnings visible but nonfatal."""
    errors, warnings = [], []
    for suffix in ('log', 'blg', 'pdf'):
        path = directory / f'{stem}.{suffix}'
        if not path.exists() or path.stat().st_size == 0:
            errors.append(f'missing/empty output: {path}')
        elif suffix != 'pdf':
            for number, line in enumerate(path.read_text(errors='replace').splitlines(), 1):
                if FATAL.search(line):
                    errors.append(f'{path.name}:{number}: {line}')
                elif WARNING.search(line):
                    warnings.append(f'{path.name}:{number}: {line}')
    return errors, warnings


def run(command, log, verbose):
    """Capture combined output and preserve the command's original exit status."""
    started = time.monotonic()
    print('Stage:', ' '.join(command), flush=True)
    with log.open('w') as output:
        output.write('Command: ' + ' '.join(command) + '\n')
        output.flush()
        with subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True, errors='replace') as process:
            for line in process.stdout:
                output.write(line)
                # latexmk schedules actual engine/biber passes; surface its rule
                # transitions without guessing a pass count or duplicating output.
                if not verbose and line.startswith("Run number "):
                    print('Stage:', line.strip(), flush=True)
                if verbose:
                    print(line, end='')
            code = process.wait()
        output.write(f'\nExit: {code}; elapsed: {time.monotonic()-started:.2f}s\n')
    print(f'Exit {code}; {time.monotonic()-started:.1f}s; log: {log}', flush=True)
    if code and not verbose:
        print('\n'.join(log.read_text(errors='replace').splitlines()[-35:]))
    return code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('roots', nargs='*', choices=('main.tex', 'main-cv.tex'))
    args = parser.parse_args()
    directory = ROOT / 'build'
    directory.mkdir(exist_ok=True)
    print('Stage: dependency checks', flush=True)
    versions = [sys.version.splitlines()[0]]
    for tool in ('latexmk', 'pdflatex', 'biber'):
        if not shutil.which(tool):
            print(f'Missing dependency: {tool}; see BUILDING.md', file=sys.stderr)
            return 2
        result = subprocess.run([tool, '--version'], capture_output=True, text=True)
        if result.returncode:
            print(f'Dependency check failed: {tool}: {result.stderr}', file=sys.stderr)
            return 2
        versions.append(tool + ': ' + (result.stdout or result.stderr).strip())
    (directory / 'tool-versions.txt').write_text('\n'.join(versions) + '\n')
    if run([sys.executable, 'tests/check_latex.py'], directory / 'static.log', args.verbose):
        return 1
    failed = False
    for stem in [Path(root).stem for root in (args.roots or ['main.tex', 'main-cv.tex'])]:
        code = run(['latexmk', '-pdf', '-file-line-error', '-interaction=nonstopmode',
                    '-halt-on-error', '-outdir=build', stem + '.tex'],
                   directory / f'{stem}-build.log', args.verbose)
        print(f'Stage: log audit for {stem}', flush=True)
        errors, warnings = audit(directory, stem)
        (directory / f'{stem}-diagnostics.txt').write_text('\n'.join(errors + warnings) + '\n')
        for message in errors + warnings:
            print(message)
        failed |= bool(code or errors)
        if not code and not errors:
            print(f'Stage: output ready — {directory / (stem + ".pdf")}; warnings: {len(warnings)}')
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
