# Development contract

Highlight possible unintended changes in grammatical person across manuscript paragraphs.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, `CHANGELOG.md`, README claims and limitations, repository metadata, release assets, and the Forge catalog together.

## 1.1.0 improvement session

Add explicit scene contracts, viewpoint intent, suppression notes and configurable quote-aware pronoun evidence.

Supply `scenes` as text objects with optional `intended_viewpoint` (first, second, third, unspecified) and `suppression_note`. Transitions between scenes do not produce shift warnings; a suppression note keeps evidence but suppresses that scene's prompts. Optional `pronoun_rules` supplies first/second/third word arrays, which must not overlap. Evidence gives character offsets and Markdown highlighting outside recognized quotation spans. Tied pronoun counts are unknown. Quotation parsing and viewpoint inference remain heuristics for author review, not findings of narrative errors.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.

## Version 1.2.0

Set `include_source_spans` to `true` to add a half-open `source_span` to each trimmed paragraph and pronoun evidence item, plus a one-based `scene_paragraph` number. Offsets count Python Unicode characters in the original `text`, or in that row's `scenes[scene - 1].text`; each scene starts at zero. CRLF characters count separately. Existing evidence `start`/`end` remain relative to the trimmed paragraph. Slice the specified original string with `[start:end]` to recover the exact paragraph or pronoun. Defaults, quote handling, counts and scene boundaries are unchanged.

## Version 1.2.1: quotation boundaries and literal reports

Quotation spans are recognized across blank lines within each scene, so multi-paragraph dialogue does not become narrative pronoun evidence. Scene boundaries remain independent; unmatched quotes remain a documented heuristic limitation. Original source spans still slice the supplied text exactly. Markdown renders authored HTML and formatting as literal text while retaining generated pronoun emphasis, and JSON sections use fences that cannot be closed by manuscript backticks. Output creation uses exclusive file creation, including refusal of dangling symbolic links.

Run the full test suite, including `tests/test_gold.py`, and both packaged examples from an installed wheel and a source distribution before release.
