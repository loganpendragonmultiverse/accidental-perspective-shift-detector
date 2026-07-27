from __future__ import annotations

import json
import re
from itertools import pairwise
from typing import Any

PROJECT = "accidental-perspective-shift-detector"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _perspective(data: dict[str, Any]) -> dict[str, Any]:
    text = str(_require(data, "text"))
    groups: dict[str, set[str]] = {
        "first": {"i", "me", "my", "mine", "we", "us", "our", "ours"},
        "second": {"you", "your", "yours"},
        "third": {
            "he",
            "him",
            "his",
            "she",
            "her",
            "hers",
            "they",
            "them",
            "their",
            "theirs",
            "it",
            "its",
        },
    }
    rows = []
    for number, paragraph in enumerate(
        (item.strip() for item in re.split("\\n\\s*\\n", text) if item.strip()), 1
    ):
        unquoted = re.sub('[\\"“].*?[\\"”]', "", paragraph)
        words = re.findall("\\b[a-z]+\\b", unquoted.casefold())
        counts = {key: sum(word in values for word in words) for key, values in groups.items()}
        dominant = max(counts, key=lambda key: counts[key]) if max(counts.values()) else "unknown"
        rows.append(
            {"paragraph": number, "dominant": dominant, "counts": counts, "preview": paragraph[:80]}
        )
    shifts = [
        {
            "from": left["paragraph"],
            "to": right["paragraph"],
            "from_person": left["dominant"],
            "to_person": right["dominant"],
        }
        for left, right in pairwise(rows)
        if "unknown" not in (left["dominant"], right["dominant"])
        and left["dominant"] != right["dominant"]
    ]
    return {"paragraphs": rows, "possible_shifts": shifts}


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": 1, "project": PROJECT, **_perspective(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            lines.append(f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
