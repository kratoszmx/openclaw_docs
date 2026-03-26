#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
URLS_DIR = ROOT / "urls"
LLMS_URL = "https://docs.openclaw.ai/llms.txt"
DOC_PREFIX = "https://docs.openclaw.ai/"


def fetch_bytes(url: str, timeout: int = 45, retries: int = 5) -> bytes:
    last_err: Exception | None = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(1.1 * (i + 1))
    raise RuntimeError(f"fetch failed: {url} :: {last_err}")


def fetch_text(url: str, timeout: int = 45, retries: int = 5) -> str:
    return fetch_bytes(url, timeout=timeout, retries=retries).decode("utf-8", "ignore")


def body_line_count(text: str) -> int:
    return sum(1 for ln in text.splitlines() if ln.strip() and not ln.strip().startswith(">"))


def extract_doc_urls(llms_text: str) -> list[str]:
    urls = sorted(set(re.findall(r"https://docs\.openclaw\.ai/[^\s)]+\.md", llms_text)))
    return urls


def main() -> None:
    parser = argparse.ArgumentParser(description="Check/repair full docs.openclaw.ai markdown mirror")
    parser.add_argument("--check-only", action="store_true", help="Only check missing/bad docs, do not download")
    parser.add_argument("--update-all", action="store_true", help="Download all docs even when local file exists")
    parser.add_argument("--timeout", type=int, default=45, help="HTTP timeout seconds (default: 45)")
    args = parser.parse_args()

    URLS_DIR.mkdir(exist_ok=True)

    llms = fetch_text(LLMS_URL, timeout=args.timeout)
    urls = extract_doc_urls(llms)
    rels = [u.replace(DOC_PREFIX, "") for u in urls]
    (URLS_DIR / "all.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")

    missing: list[str] = []
    bad: list[str] = []
    failures: list[tuple[str, str]] = []
    downloaded = 0

    for rel in rels:
        path = ROOT / rel

        if args.check_only:
            if not path.exists():
                missing.append(rel)
                continue
            txt = path.read_text(encoding="utf-8", errors="ignore")
            if len(txt.strip()) == 0 or body_line_count(txt) <= 3:
                bad.append(rel)
            continue

        need_download = args.update_all or (not path.exists())

        if not need_download:
            txt = path.read_text(encoding="utf-8", errors="ignore")
            if len(txt.strip()) == 0 or body_line_count(txt) <= 3:
                need_download = True

        if not need_download:
            continue

        url = DOC_PREFIX + rel
        try:
            data = fetch_bytes(url, timeout=args.timeout)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            downloaded += 1
        except Exception as e:  # noqa: BLE001
            failures.append((rel, f"download:{e}"))
            continue

        txt = path.read_text(encoding="utf-8", errors="ignore")
        if len(txt.strip()) == 0 or body_line_count(txt) <= 3:
            try:
                data = fetch_bytes(url, timeout=args.timeout)
                path.write_bytes(data)
            except Exception as e:  # noqa: BLE001
                failures.append((rel, f"redownload:{e}"))
                continue

            txt2 = path.read_text(encoding="utf-8", errors="ignore")
            if len(txt2.strip()) == 0 or body_line_count(txt2) <= 3:
                bad.append(rel)

    print(f"expected_docs={len(rels)}")
    if args.check_only:
        print(f"missing={len(missing)}")
        print(f"bad={len(bad)}")
    else:
        print(f"downloaded={downloaded}")
        print(f"postcheck_bad={len(bad)}")
        print(f"failures={len(failures)}")

    if missing:
        print("MISSING:")
        for rel in missing:
            print(rel)

    if bad:
        print("BAD:")
        for rel in bad:
            print(rel)

    if failures:
        print("FAILURES:")
        for rel, msg in failures:
            print(f"{rel}\t{msg}")


if __name__ == "__main__":
    main()
