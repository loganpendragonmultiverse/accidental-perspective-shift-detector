import pytest

from perspective_shift_detector.core import analyze, render_markdown


def test_scene_contract_quotes_and_suppression() -> None:
    report = analyze(
        {
            "scenes": [
                {
                    "text": 'I walk. "He says she knows."\n\nShe walks.',
                    "intended_viewpoint": "first",
                },
                {"text": "You wait.\n\nHe waits.", "suppression_note": "Deliberate transition"},
            ]
        }
    )
    assert len(report["possible_shifts"]) == 1
    first = report["paragraphs"][0]
    assert first["counts"]["third"] == 0
    assert first["evidence"][0]["word"] == "I"
    assert report["paragraphs"][1]["review_intended_viewpoint"]
    assert '**I** walk. "He says she knows."' in render_markdown(report)


def test_custom_rules_and_ties() -> None:
    report = analyze(
        {
            "text": "Xe walks.\n\nI and xe wait.",
            "pronoun_rules": {"first": ["I"], "second": [], "third": ["xe"]},
        }
    )
    assert report["paragraphs"][0]["dominant"] == "third"
    assert report["paragraphs"][1]["dominant"] == "unknown"


@pytest.mark.parametrize(
    "data",
    [
        {"text": []},
        {"scenes": []},
        {"scenes": [None]},
        {"scenes": [{"text": "A", "intended_viewpoint": "guess"}]},
        {"scenes": [{"text": "A", "suppression_note": []}]},
        {"text": "A", "pronoun_rules": {}},
        {"text": "A", "pronoun_rules": {"first": [1], "second": [], "third": []}},
        {"text": "A", "pronoun_rules": {"first": ["i"], "second": ["i"], "third": []}},
    ],
)
def test_invalid_scene_contract(data) -> None:
    with pytest.raises(ValueError):
        analyze(data)
