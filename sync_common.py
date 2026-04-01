#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import project_env  # noqa: F401
from http_utils import fetch_bytes, fetch_text
from markdown_utils import count_markdown_body_lines, is_empty_or_sparse_markdown

ROOT = Path(__file__).resolve().parent
DOCS_ROOT = ROOT / "docs"
OTHERS_ROOT = DOCS_ROOT / "others"
URLS_DIR = ROOT / "urls"
LLMS_URL = "https://docs.openclaw.ai/llms.txt"
DOC_PREFIX = "https://docs.openclaw.ai/"


def body_line_count(text: str) -> int:
    return count_markdown_body_lines(text)


def is_empty_or_truncated(text: str) -> bool:
    return is_empty_or_sparse_markdown(text)


def extract_doc_urls(llms_text: str) -> list[str]:
    return sorted(set(re.findall(r"https://docs\.openclaw\.ai/[^\s)]+\.md", llms_text)))


def all_doc_urls(timeout: int = 45) -> list[str]:
    return extract_doc_urls(fetch_text(LLMS_URL, timeout=timeout))


def rels_from_urls(urls: list[str]) -> list[str]:
    return [url.replace(DOC_PREFIX, "") for url in urls]


def urls_from_rels(rels: list[str]) -> list[str]:
    return [DOC_PREFIX + rel for rel in rels]


def doc_path(rel: str) -> Path:
    """Map a docs.openclaw.ai relative markdown path to the local mirror path.

    Local layout rule:
    - nested docs keep their original section path under `docs/`
    - root-level markdown files are grouped under `docs/others/`
    """
    rel_path = Path(rel)
    if rel_path.parent == Path("."):
        return OTHERS_ROOT / rel_path.name
    return DOCS_ROOT / rel_path


def ensure_dirs() -> None:
    DOCS_ROOT.mkdir(exist_ok=True)
    OTHERS_ROOT.mkdir(exist_ok=True)
    URLS_DIR.mkdir(exist_ok=True)


def write_url_list(name: str, urls: list[str]) -> None:
    ensure_dirs()
    (URLS_DIR / name).write_text("\n".join(urls) + "\n", encoding="utf-8")


def filter_rels_by_prefix(rels: list[str], prefix: str) -> list[str]:
    return [rel for rel in rels if rel.startswith(prefix + "/")]


def filter_rels_by_prefixes(rels: list[str], prefixes: list[str]) -> list[str]:
    allowed = tuple(prefix + "/" for prefix in prefixes)
    return [rel for rel in rels if rel.startswith(allowed)]


def download_rel(rel: str, timeout: int = 45) -> tuple[bool, str | None]:
    url = DOC_PREFIX + rel
    path = doc_path(rel)
    try:
        data = fetch_bytes(url, timeout=timeout)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    except Exception as exc:  # noqa: BLE001
        return False, f"download:{exc}"

    text = path.read_text(encoding="utf-8", errors="ignore")
    if is_empty_or_truncated(text):
        try:
            data = fetch_bytes(url, timeout=timeout)
            path.write_bytes(data)
        except Exception as exc:  # noqa: BLE001
            return False, f"redownload:{exc}"
    return True, None


def sync_rels(rels: list[str], timeout: int = 45, force_download: bool = True) -> tuple[int, list[tuple[str, str]]]:
    ensure_dirs()
    downloaded = 0
    failures: list[tuple[str, str]] = []

    for rel in rels:
        path = doc_path(rel)
        need_download = force_download or (not path.exists())
        if not need_download:
            text = path.read_text(encoding="utf-8", errors="ignore")
            need_download = is_empty_or_truncated(text)
        if not need_download:
            continue

        ok, err = download_rel(rel, timeout=timeout)
        if ok:
            downloaded += 1
        else:
            failures.append((rel, err or "unknown"))

    return downloaded, failures


def check_rels(rels: list[str]) -> tuple[list[str], list[str]]:
    missing: list[str] = []
    bad: list[str] = []
    for rel in rels:
        path = doc_path(rel)
        if not path.exists():
            missing.append(rel)
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if is_empty_or_truncated(text):
            bad.append(rel)
    return missing, bad
