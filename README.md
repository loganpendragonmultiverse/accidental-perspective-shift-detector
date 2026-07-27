# Accidental Perspective Shift Detector

[![CI](https://github.com/loganpendragonmultiverse/accidental-perspective-shift-detector/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/accidental-perspective-shift-detector/actions/workflows/ci.yml)

Highlight possible unintended changes in grammatical person across manuscript paragraphs. The command runs locally, uses explicit UTF-8 JSON input, and produces deterministic JSON or Markdown reports without modifying the supplied source material.

## Three-minute start

```bash
python -m pip install .
perspective-shifts examples/sample.json
perspective-shifts examples/sample.json --format json --output report.json
```

The example documents the complete v1 input shape. Markdown is intended for immediate review; JSON preserves structured evidence for scripts and later comparison. An existing output file is never overwritten.

## Privacy and platforms

All manuscript text stays local.

Python 3.10 or newer is supported on Windows, macOS, and Linux. The package has no runtime dependencies, telemetry, account, or hosted service.

## Interpretation boundary

The detector uses pronoun counts and cannot identify true viewpoint, free indirect discourse, quoted speech, or intentional stylistic shifts.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).
