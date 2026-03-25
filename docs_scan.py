#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)$')
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def iter_markdown_files(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            out.extend(sorted(p.rglob('*.md')))
        elif p.is_file() and p.suffix.lower() == '.md':
            out.append(p)
    return out


def scan_file(path: Path) -> dict:
    text = path.read_text(errors='ignore')
    lines = text.splitlines()
    headings = []
    links = []
    body_lines = 0
    for i, line in enumerate(lines, 1):
        m = HEADING_RE.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))
        if line.strip() and not line.strip().startswith('>'):
            body_lines += 1
        for label, target in LINK_RE.findall(line):
            links.append((i, label.strip(), target.strip()))
    return {
        'path': str(path),
        'chars': len(text),
        'lines': len(lines),
        'body_lines': body_lines,
        'empty_or_truncated': len(text.strip()) == 0 or body_lines <= 3,
        'headings': headings,
        'links': links,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Scan markdown headings and links for OpenClaw docs.')
    parser.add_argument('paths', nargs='+', help='Markdown files or directories')
    parser.add_argument('--show-links', action='store_true', help='Print markdown links too')
    args = parser.parse_args()

    files = iter_markdown_files(args.paths)
    if not files:
        print('No markdown files found.')
        return

    for path in files:
        data = scan_file(path)
        print(f"===== {data['path']} =====")
        print(f"chars={data['chars']} lines={data['lines']} body_lines={data['body_lines']} empty_or_truncated={data['empty_or_truncated']}")
        for line_no, level, title in data['headings']:
            indent = '  ' * (level - 1)
            print(f"{indent}- L{line_no} H{level}: {title}")
        if args.show_links and data['links']:
            print('links:')
            for line_no, label, target in data['links']:
                print(f"  - L{line_no}: [{label}] -> {target}")
        print()


if __name__ == '__main__':
    main()
