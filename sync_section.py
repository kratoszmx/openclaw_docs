#!/usr/bin/env python3
from __future__ import annotations

import sys

from sync_common import all_doc_urls, filter_rels_by_prefix, rels_from_urls, sync_rels, write_url_list


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 sync_section.py <section>")

    section = sys.argv[1]
    urls = all_doc_urls()
    rels = filter_rels_by_prefix(rels_from_urls(urls), section)
    write_url_list(f"{section}.txt", [f"https://docs.openclaw.ai/{rel}" for rel in rels])

    downloaded, failures = sync_rels(rels, force_download=True)
    print(f"{section}: {len(rels)}")
    print(f"downloaded: {downloaded}")
    if failures:
        print("FAILURES:")
        for rel, msg in failures:
            print(f"{rel}\t{msg}")


if __name__ == "__main__":
    main()
