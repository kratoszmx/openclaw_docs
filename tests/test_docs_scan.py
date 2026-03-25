from pathlib import Path

from docs_scan import iter_markdown_files, scan_file


def test_iter_markdown_files_finds_md(tmp_path: Path):
    sub = tmp_path / "sub"
    sub.mkdir()
    a = tmp_path / "a.md"
    b = sub / "b.md"
    a.write_text("# A\n")
    b.write_text("# B\n")

    found = iter_markdown_files([str(tmp_path)])
    assert a in found
    assert b in found


def test_scan_file_extracts_headings_and_links(tmp_path: Path):
    p = tmp_path / "sample.md"
    p.write_text(
        "# Title\n\n"
        "Intro line one.\n"
        "Intro line two.\n"
        "## Section\n"
        "See [Install](/install).\n"
        "Another useful body line.\n"
    )

    data = scan_file(p)
    assert data["empty_or_truncated"] is False
    assert data["headings"][0][2] == "Title"
    assert data["headings"][1][2] == "Section"
    assert data["links"][0][1] == "Install"
    assert data["links"][0][2] == "/install"


def test_scan_file_marks_empty_or_truncated(tmp_path: Path):
    p = tmp_path / "empty.md"
    p.write_text("")
    data = scan_file(p)
    assert data["empty_or_truncated"] is True
