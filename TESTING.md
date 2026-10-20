# Testing

Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`. CI also audits dependencies and runs the supported OS/Python matrix.

## 1.1.0 regression acceptance

Run the complete existing suite plus the new regression fixtures. Confirm the documented command produces the selected output, malformed input remains actionable, and source files remain unchanged. Add explicit scene contracts, viewpoint intent, suppression notes and configurable quote-aware pronoun evidence.

## Version 1.2.0 acceptance

`tests/test_feature.py` covers the new option, boundary cases, and unchanged default reports using synthetic text only. Run `perspective-shifts examples/feature.json --format json` and the README sample commands against an installed wheel and an extracted source archive. Inspect packaged README, CHANGELOG, DEVELOPMENT and TESTING documents and confirm package version 1.2.0.

## Version 1.2.1: quotation boundaries and literal reports

Quotation spans are recognized across blank lines within each scene, so multi-paragraph dialogue does not become narrative pronoun evidence. Scene boundaries remain independent; unmatched quotes remain a documented heuristic limitation. Original source spans still slice the supplied text exactly. Markdown renders authored HTML and formatting as literal text while retaining generated pronoun emphasis, and JSON sections use fences that cannot be closed by manuscript backticks. Output creation uses exclusive file creation, including refusal of dangling symbolic links.

Run the full test suite, including `tests/test_gold.py`, and both packaged examples from an installed wheel and a source distribution before release.
