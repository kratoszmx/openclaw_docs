from pathlib import Path

from sync_common import DOCS_ROOT, OTHERS_ROOT, doc_path


def test_doc_path_maps_root_level_docs_to_others() -> None:
    assert doc_path("index.md") == OTHERS_ROOT / "index.md"
    assert doc_path("ci.md") == OTHERS_ROOT / "ci.md"
    assert doc_path("vps.md") == OTHERS_ROOT / "vps.md"


def test_doc_path_keeps_nested_docs_under_original_sections() -> None:
    assert doc_path("tools/browser.md") == DOCS_ROOT / Path("tools/browser.md")
    assert doc_path("gateway/index.md") == DOCS_ROOT / Path("gateway/index.md")
    assert doc_path("reference/templates/USER.md") == DOCS_ROOT / Path("reference/templates/USER.md")
