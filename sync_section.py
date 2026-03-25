#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path('/Users/ddy88haojiqi/projects/openclaw_docs')
URLS_DIR = ROOT / 'urls'
URLS_DIR.mkdir(exist_ok=True)
section = sys.argv[1]

text = subprocess.check_output(
    'curl -L --max-time 30 https://docs.openclaw.ai/llms.txt 2>/dev/null',
    shell=True,
    text=True,
    executable='/bin/bash',
)
pattern = re.compile(r'\((https://docs\.openclaw\.ai/(' + re.escape(section) + r'/[^)]+\.md))\)')
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

(URLS_DIR / f'{section}.txt').write_text('\n'.join(url for url, _ in ordered) + '\n')

def download(url: str, out: Path) -> bool:
    cmd = f'curl --http1.1 -L --retry 3 --retry-delay 1 --max-time 45 "{url}" -o "{out}"'
    result = subprocess.run(cmd, shell=True, executable='/bin/bash')
    return result.returncode == 0

fails = []
for url, rel in ordered:
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    ok = download(url, out)
    if not ok:
        fails.append((rel, url, 'initial'))

for _, rel in ordered:
    p = ROOT / rel
    txt = p.read_text(errors='ignore') if p.exists() else ''
    body = [ln for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith('>')]
    if len(txt.strip()) == 0 or len(body) <= 3:
        url = f'https://docs.openclaw.ai/{rel}'
        ok = download(url, p)
        if not ok:
            fails.append((rel, url, 'redownload'))

print(f'{section}: {len(ordered)}')
if fails:
    print('FAILURES:')
    for rel, url, reason in fails:
        print(f'{reason}\t{rel}\t{url}')
