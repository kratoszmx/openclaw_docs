#!/usr/bin/env python3
from __future__ import annotations

import argparse

from sync_common import all_doc_urls, filter_rels_by_prefixes, rels_from_urls, sync_rels, urls_from_rels, write_url_list

SECTIONS = ["install", "channels", "tools", "plugins", "platforms", "gateway", "reference", "help"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync selected docs.openclaw.ai sections")
    parser.add_argument("--timeout", type=int, default=45, help="HTTP timeout seconds (default: 45)")
    args = parser.parse_args()

    rels = filter_rels_by_prefixes(rels_from_urls(all_doc_urls(timeout=args.timeout)), SECTIONS)
    write_url_list("selected_sections.txt", urls_from_rels(rels))

    downloaded, failures = sync_rels(rels, timeout=args.timeout, force_download=True)
    print(f"SYNCED {len(rels)} files")
    print(f"downloaded: {downloaded}")
    for section in SECTIONS:
        count = sum(1 for rel in rels if rel.startswith(section + "/"))
        print(f"{section}: {count}")
    if failures:
        print("FAILURES:")
        for rel, msg in failures:
            print(f"{rel}\t{msg}")


if __name__ == "__main__":
    main()
