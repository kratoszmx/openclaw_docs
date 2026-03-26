#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS_ROOT = ROOT / 'docs'
SECTIONS = ['install', 'channels', 'tools', 'plugins', 'platforms', 'gateway', 'reference', 'help']
URLS_DIR = DOCS_ROOT / 'urls'
URLS_DIR.mkdir(parents=True, exist_ok=True)

text = subprocess.check_output(
    'curl -L --max-time 30 https://docs.openclaw.ai/llms.txt 2>/dev/null',
    shell=True,
    text=True,
    executable='/bin/bash',
)
pattern = re.compile(r'\((https://docs\.openclaw\.ai/((?:' + '|'.join(SECTIONS) + r')/[^)]+\.md))\)')
items = []
for line in text.splitlines():
    m = pattern.search(line)
    if m:
        items.append((m.group(1), m.group(2)))

seen = set()
ordered = []
for url, rel in items:
    if rel not in seen:
        seen.add(rel)
        ordered.append((url, rel))

(URLS_DIR / 'selected_sections.txt').write_text('\n'.join(url for url, _ in ordered) + '\n')

failures = []

def download(url: str, out: Path) -> bool:
    cmd = f'curl --http1.1 -L --retry 3 --retry-delay 1 --max-time 45 "{url}" -o "{out}"'
    result = subprocess.run(cmd, shell=True, executable='/bin/bash')
    return result.returncode == 0

for url, rel in ordered:
    out = DOCS_ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    ok = download(url, out)
    if not ok:
        failures.append((rel, url, 'initial-download-failed'))

for _, rel in ordered:
    p = DOCS_ROOT / rel
    txt = p.read_text(errors='ignore') if p.exists() else ''
    body = [ln for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith('>')]
    if len(txt.strip()) == 0 or len(body) <= 3:
        url = f'https://docs.openclaw.ai/{rel}'
        ok = download(url, p)
        if not ok:
            failures.append((rel, url, 'redownload-failed'))

print(f'SYNCED {len(ordered)} files')
for section in SECTIONS:
    count = sum(1 for _, rel in ordered if rel.startswith(section + '/'))
    print(f'{section}: {count}')
if failures:
    print('FAILURES:')
    for rel, url, reason in failures:
        print(f'{reason}\t{rel}\t{url}')
