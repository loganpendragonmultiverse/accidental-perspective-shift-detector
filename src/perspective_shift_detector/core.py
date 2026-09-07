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
    text = data.get("text", "")
    if not isinstance(text, str):
        raise ValueError("text must be a string")
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
    rules = data.get("pronoun_rules")
    if rules is not None:
        if not isinstance(rules, dict) or set(rules) != set(groups):
            raise ValueError("pronoun_rules must specify first, second, and third arrays")
        for key, words in rules.items():
            if not isinstance(words, list) or not all(
                isinstance(word, str) and re.fullmatch(r"[a-zA-Z]+", word) for word in words
            ):
                raise ValueError(f"pronoun_rules.{key} must contain words")
            groups[key] = {word.casefold() for word in words}
        if sum(len(words) for words in groups.values()) != len(set().union(*groups.values())):
            raise ValueError("pronoun_rules groups must not overlap")
    scenes = data.get("scenes", [{"text": text}])
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("scenes must be a nonempty array")
    rows: list[dict[str, Any]] = []
    for scene_index, scene in enumerate(scenes, 1):
        if (
            not isinstance(scene, dict)
            or not isinstance(scene.get("text"), str)
            or not scene["text"].strip()
        ):
            raise ValueError(f"scenes[{scene_index}].text must be nonempty text")
        intended = scene.get("intended_viewpoint", "unspecified")
        note = scene.get("suppression_note", "")
        if not isinstance(intended, str) or intended not in {*groups, "unspecified"}:
            raise ValueError(f"scenes[{scene_index}].intended_viewpoint is invalid")
        if not isinstance(note, str):
            raise ValueError(f"scenes[{scene_index}].suppression_note must be text")
        for paragraph in (
            item.strip() for item in re.split("\\n\\s*\\n", scene["text"]) if item.strip()
        ):
            quoted = [
                (m.start(), m.end())
                for m in re.finditer(
                    r'"[^"\n]*(?:\n[^"\n]*)*"|“[^”]*”|(?<!\w)\x27[^\x27]*\x27(?!\w)|‘[^’]*’',
                    paragraph,
                )
            ]
            evidence = []
            counts = dict.fromkeys(groups, 0)
            for token in re.finditer(r"\b[a-z]+\b", paragraph, re.IGNORECASE):
                if any(start <= token.start() < end for start, end in quoted):
                    continue
                for key, words in groups.items():
                    if token.group().casefold() in words:
                        counts[key] += 1
                        evidence.append(
                            {
                                "start": token.start(),
                                "end": token.end(),
                                "word": paragraph[token.start() : token.end()],
                                "person": key,
                            }
                        )
            highest = max(counts.values())
            winners = [key for key, value in counts.items() if value == highest]
            dominant = winners[0] if highest and len(winners) == 1 else "unknown"
            rows.append(
                {
                    "paragraph": len(rows) + 1,
                    "scene": scene_index,
                    "dominant": dominant,
                    "counts": counts,
                    "preview": paragraph[:80],
                    "text": paragraph,
                    "evidence": evidence,
                    "quoted_ranges": quoted,
                    "intended_viewpoint": intended,
                    "suppression_note": note,
                    "review_intended_viewpoint": not note
                    and intended != "unspecified"
                    and dominant not in {intended, "unknown"},
                }
            )
    shifts = [
        {
            "from": left["paragraph"],
            "to": right["paragraph"],
            "from_person": left["dominant"],
            "to_person": right["dominant"],
            "scene": right["scene"],
        }
        for left, right in pairwise(rows)
        if "unknown" not in (left["dominant"], right["dominant"])
        and left["dominant"] != right["dominant"]
        and left["scene"] == right["scene"]
        and not right["suppression_note"]
    ]
    return {
        "paragraphs": rows,
        "possible_shifts": shifts,
        "interpretation": "Pronoun evidence for author review, not a determination of narrative error. Quotation handling is heuristic.",
    }


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return {"version": 1, "project": PROJECT, **_perspective(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for row in report["paragraphs"]:
        text = row["text"]
        for item in reversed(row["evidence"]):
            text = (
                text[: item["start"]]
                + "**"
                + text[item["start"] : item["end"]]
                + "**"
                + text[item["end"] :]
            )
        lines.extend([f"### Scene {row['scene']}, paragraph {row['paragraph']}", "", text, ""])
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            lines.append(f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
