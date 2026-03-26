#!/usr/bin/env python3
from __future__ import annotations

from sync_common import all_doc_urls, filter_rels_by_prefixes, rels_from_urls, sync_rels, write_url_list

SECTIONS = ["install", "channels", "tools", "plugins", "platforms", "gateway", "reference", "help"]


def main() -> None:
    urls = all_doc_urls()
    rels = filter_rels_by_prefixes(rels_from_urls(urls), SECTIONS)
    write_url_list("selected_sections.txt", [f"https://docs.openclaw.ai/{rel}" for rel in rels])

    downloaded, failures = sync_rels(rels, force_download=True)
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
