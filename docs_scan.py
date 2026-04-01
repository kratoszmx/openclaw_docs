#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import project_env  # noqa: F401
from markdown_utils import (
    count_markdown_body_lines,
    extract_markdown_headings,
    extract_markdown_links,
    iter_markdown_files,
    is_empty_or_sparse_markdown,
)


def scan_file(path: Path) -> dict:
    text = path.read_text(errors="ignore")
    lines = text.splitlines()
    headings = extract_markdown_headings(text)
    links = extract_markdown_links(text)
    body_lines = count_markdown_body_lines(text)
    return {
        "path": str(path),
        "chars": len(text),
        "lines": len(lines),
        "body_lines": body_lines,
        "empty_or_truncated": is_empty_or_sparse_markdown(text),
        "headings": headings,
        "links": links,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan markdown headings and links for OpenClaw docs.")
    parser.add_argument("paths", nargs="+", help="Markdown files or directories")
    parser.add_argument("--show-links", action="store_true", help="Print markdown links too")
    args = parser.parse_args()

    files = iter_markdown_files(args.paths)
    if not files:
        print("No markdown files found.")
        return

    for path in files:
        data = scan_file(path)
        print(f"===== {data['path']} =====")
        print(
            f"chars={data['chars']} lines={data['lines']} body_lines={data['body_lines']} "
            f"empty_or_truncated={data['empty_or_truncated']}"
        )
        for line_no, level, title in data["headings"]:
            indent = "  " * (level - 1)
            print(f"{indent}- L{line_no} H{level}: {title}")
        if args.show_links and data["links"]:
            print("links:")
            for line_no, label, target in data["links"]:
                print(f"  - L{line_no}: [{label}] -> {target}")
        print()


if __name__ == "__main__":
    main()
