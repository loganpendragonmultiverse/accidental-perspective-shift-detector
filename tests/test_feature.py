from copy import deepcopy

import pytest

from perspective_shift_detector.core import analyze


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_source_slices_scenes_and_compatibility(newline):
    text = f"  é I walk. “She knows.”  {newline}{newline}  I walk.  {newline}{newline}He waits."
    data = {"scenes": [{"text": text}, {"text": '  You wait. "I know."  '}]}
    original = deepcopy(data)
    baseline = analyze(data)
    report = analyze({**data, "include_source_spans": True})
    assert data == original
    assert report["possible_shifts"] == baseline["possible_shifts"]
    for row, old in zip(report["paragraphs"], baseline["paragraphs"], strict=True):
        source = data["scenes"][row["scene"] - 1]["text"]
        span = row.pop("source_span")
        assert source[span["start"] : span["end"]] == row["text"]
        assert row.pop("scene_paragraph") == (row["paragraph"] if row["scene"] == 1 else 1)
        for item in row["evidence"]:
            span = item.pop("source_span")
            assert source[span["start"] : span["end"]] == item["word"]
        assert row == old
    assert baseline["paragraphs"][0]["counts"]["third"] == 0


def test_repeated_paragraphs_and_top_level_coordinates():
    text = " \tI wait.\n\n  I wait.  "
    report = analyze({"text": text, "include_source_spans": True})
    rows = report["paragraphs"]
    assert [row["source_span"]["start"] for row in rows] == [2, 13]
    assert text[rows[1]["source_span"]["start"] : rows[1]["source_span"]["end"]] == "I wait."
    assert analyze({"text": text}) == analyze({"text": text, "include_source_spans": False})
    with pytest.raises(TypeError, match="boolean"):
        analyze({"text": text, "include_source_spans": 1})
