#!/usr/bin/env python3
from __future__ import annotations

import argparse

from sync_common import all_doc_urls, check_rels, rels_from_urls, sync_rels, write_url_list


def main() -> None:
    parser = argparse.ArgumentParser(description="Check/repair full docs.openclaw.ai markdown mirror")
    parser.add_argument("--check-only", action="store_true", help="Only check missing/bad docs, do not download")
    parser.add_argument("--update-all", action="store_true", help="Download all docs even when local file exists")
    parser.add_argument("--timeout", type=int, default=45, help="HTTP timeout seconds (default: 45)")
    args = parser.parse_args()

    urls = all_doc_urls(timeout=args.timeout)
    rels = rels_from_urls(urls)
    write_url_list("all.txt", urls)

    print(f"expected_docs={len(rels)}")

    if args.check_only:
        missing, bad = check_rels(rels)
        print(f"missing={len(missing)}")
        print(f"bad={len(bad)}")
        if missing:
            print("MISSING:")
            for rel in missing:
                print(rel)
        if bad:
            print("BAD:")
            for rel in bad:
                print(rel)
        return

    downloaded, failures = sync_rels(rels, timeout=args.timeout, force_download=args.update_all)
    _, bad = check_rels(rels)
    print(f"downloaded={downloaded}")
    print(f"postcheck_bad={len(bad)}")
    print(f"failures={len(failures)}")

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
