#!/usr/bin/env python3
from __future__ import annotations

import argparse

from sync_common import all_doc_urls, filter_rels_by_prefix, rels_from_urls, sync_rels, urls_from_rels, write_url_list


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync one docs.openclaw.ai section")
    parser.add_argument("section", help="Top-level section name, e.g. tools")
    parser.add_argument("--timeout", type=int, default=45, help="HTTP timeout seconds (default: 45)")
    args = parser.parse_args()

    rels = filter_rels_by_prefix(rels_from_urls(all_doc_urls(timeout=args.timeout)), args.section)
    write_url_list(f"{args.section}.txt", urls_from_rels(rels))

    downloaded, failures = sync_rels(rels, timeout=args.timeout, force_download=True)
    print(f"{args.section}: {len(rels)}")
    print(f"downloaded: {downloaded}")
    if failures:
        print("FAILURES:")
        for rel, msg in failures:
            print(f"{rel}\t{msg}")


if __name__ == "__main__":
    main()
