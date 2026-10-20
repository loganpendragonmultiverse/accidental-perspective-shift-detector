import json
from pathlib import Path

import pytest

from perspective_shift_detector.cli import main
from perspective_shift_detector.core import analyze, render_markdown


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_quotation_across_paragraphs_preserves_source_evidence(newline):
    text = f"  I wait. “He speaks.{newline}{newline}She answers.”{newline}{newline}You leave.  "
    report = analyze({"text": text, "include_source_spans": True})
    assert len(report["paragraphs"]) == 3
    assert [row["dominant"] for row in report["paragraphs"]] == ["first", "unknown", "second"]
    assert not report["possible_shifts"]
    for row in report["paragraphs"]:
        assert row["counts"]["third"] == 0
        span = row["source_span"]
        assert text[span["start"] : span["end"]] == row["text"]
    # Quotes cannot suppress evidence in another scene.
    assert (
        analyze({"scenes": [{"text": '"I wait.'}, {"text": 'He waits."'}]})["paragraphs"][1][
            "counts"
        ]["third"]
        == 1
    )


def test_markdown_keeps_authored_html_and_fences_literal():
    report = analyze(
        {"text": '<img src="x"> I [walk](https://example.com). ```json\n<script>he</script>'}
    )
    rendered = render_markdown(report)
    assert "<img" not in rendered.split("## Paragraphs")[0]
    assert "&lt;img" in rendered
    assert "**I**" in rendered
    assert "````json" in rendered
    assert "\\[walk\\]" in rendered


def test_existing_and_dangling_output_links_are_preserved(tmp_path: Path):
    source = tmp_path / "source.json"
    source.write_text(json.dumps({"text": "I wait."}), encoding="utf-8")
    target = tmp_path / "missing"
    output = tmp_path / "report.md"
    try:
        output.symlink_to(target)
    except OSError:
        pytest.skip("symlinks unavailable")
    assert main([str(source), "--output", str(output)]) == 2
    assert output.is_symlink() and not target.exists()
