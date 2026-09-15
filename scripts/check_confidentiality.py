#!/usr/bin/env python3
"""Fail on known confidential-record signals in tracked files and reachable history.

Uses only the standard library and Git. Diagnostics report rules and paths, never
matched text. This is a review aid, not a guarantee that prose is non-confidential.
"""
import argparse
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
# This public template keeps supporting records out of version control. A new
# binary asset needs a separate review and an explicit policy change.
ATTACHMENTS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
               '.png', '.jpg', '.jpeg', '.gif', '.tif', '.tiff', '.webp',
               '.zip', '.tar', '.gz', '.7z', '.rar', '.sqlite', '.db'}
CONTENT = {'.tex', '.bib', '.md', '.txt', '.csv', '.tsv', '.json', '.yml',
           '.yaml', '.toml', '.xml', '.html', '.rst'}

RULES = [
    ('tenure vote count', re.compile(
        r'(?:number\s+voting\s+(?:yes|no|abstaining)|'
        r'(?:yes|no|abstain\w*)\s+votes?|votes?\s+(?:for|against)|'
        r'vote\s+(?:count|tally|results?))\s*[:=\-]?\s*\d+', re.I)),
    ('tenure vote count', re.compile(
        r'\b\d+\s+(?:votes?\s+(?:for|against|yes|no)|'
        r'acceptable\s+(?:and|[,;]))', re.I)),
    ('supervisor or committee record', re.compile(
        r'\b(?:supervisor|department\s+head|reviewer|committee)(?:[\x27\u2019]s)?\s+'
        r'(?:comments?|feedback|evaluation|recommendation|rating)\s*[:=]\s*'
        r'(?!\[?redacted\b|\[?omitted\b|\[?placeholder\b)\S', re.I)),
    ('individual evaluation rating', re.compile(
        r'\b(?:overall|individual|performance|supervisor)\s+(?:rating|evaluation)'
        r'\s*[:=]\s*(?:exceeds|meets|below|does\s+not\s+meet|unsatisfactory|outstanding)', re.I)),
    ('individual evaluation rating', re.compile(
        r'\b(?:rated|rating\s+of)\s+[\x22\x27\u201c\u201d]*'
        r'(?:exceeds|meets|below|does\s+not\s+meet)\s+expectations\b', re.I)),
    ('confidential content marker', re.compile(r'\[(?:strictly\s+)?confidential\]', re.I)),
]
UNIVERSAL = [
    ('private document link', re.compile(
        r'https?://(?:[\w.-]+\.)?(?:sharepoint\.com|staffnet\.atlassian\.net|'
        r'staffnet\.lib\.k-state\.edu)(?:[/:]|\b)', re.I)),
    ('private key', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----')),
    ('access token', re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b')),
]


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)


def scan_blob(path, data, mode='100644'):
    """Return rule names only. Do not expose potentially private matched values."""
    if mode not in ('100644', '100755'):
        return ['symlink or submodule requires review']
    suffix = PurePosixPath(path).suffix.lower()
    if suffix in ATTACHMENTS:
        return ['attachment requires confidentiality review']
    if b'\x00' in data:
        return ['binary content requires confidentiality review']
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return ['non-UTF-8 content requires confidentiality review']
    rules = list(UNIVERSAL)
    # Include prose/config records; code still receives credential/private-link
    # checks. Synthetic detector tests are code, not candidate records.
    if suffix in CONTENT:
        rules += RULES
    # Normalize common LaTeX spacing to catch e.g. "Number voting yes: & 19".
    normalized = re.sub(r'[{}&~]', ' ', text)
    return sorted({name for name, pattern in rules if pattern.search(normalized)})


def check(root, history=False):
    findings = []
    entries = git(root, 'ls-files', '--stage', '-z').split(b'\x00')
    for entry in filter(None, entries):
        header, raw_path = entry.split(b'\t', 1)
        mode, _, _ = header.decode().split()
        path = raw_path.decode('utf-8')
        file = root / path
        if not file.exists() and not file.is_symlink():
            continue  # A locally deleted file is checked in history below.
        data = b'' if file.is_symlink() else file.read_bytes()
        for rule in scan_blob(path, data, mode):
            findings.append(('working tree', path, rule))
    if history:
        if git(root, 'rev-parse', '--is-shallow-repository').strip() == b'true':
            raise ValueError('History scan requires a full checkout (fetch-depth: 0).')
        seen = set()
        for commit in git(root, 'rev-list', 'HEAD').decode().splitlines():
            for entry in filter(None, git(root, 'ls-tree', '-r', '-z', commit).split(b'\x00')):
                header, raw_path = entry.split(b'\t', 1)
                mode, kind, oid = header.decode().split()
                path = raw_path.decode('utf-8')
                key = (path, oid, mode)
                if key in seen:
                    continue
                seen.add(key)
                data = git(root, 'cat-file', 'blob', oid) if kind == 'blob' else b''
                for rule in scan_blob(path, data, mode):
                    findings.append((commit[:12], path, rule))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--history', action='store_true', help='also scan every commit reachable from HEAD')
    args = parser.parse_args()
    try:
        findings = check(ROOT, args.history)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        # Exception text can contain subprocess paths; never dump source content.
        print('Confidentiality check could not complete: ' + str(error), file=sys.stderr)
        return 2
    for revision, path, rule in findings:
        print(f'{revision}: {path}: {rule}', file=sys.stderr)
    if findings:
        print(f'Confidentiality check failed: {len(findings)} finding(s). Review locally; do not paste private content into issues.', file=sys.stderr)
        return 1
    print('Confidentiality check passed for tracked files' + (' and reachable history.' if args.history else '.'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
