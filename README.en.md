<div align="center">

# Humanities Essay

**Evidence-led Chinese humanities storytelling, with honest facts and memorable prose.**

[![Validation](https://github.com/2023violet/humanities-essay/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/2023violet/humanities-essay/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
![Version](https://img.shields.io/badge/version-3.1.0-informational)

[简体中文](README.md) · **English**

</div>

`humanities-essay` is an [Agent Skills](https://agentskills.io/)-compatible writing and editing workflow for Chinese-language history, poetry, literature, myth, and cultural criticism. It provides source separation, structural choices, contradiction testing, restrained prose, review-only editing, and optional single-image publishing guidance.

## Features

| Capability | Approach |
|---|---|
| Research and framing | Two competing thesis candidates, source ledger, counterevidence |
| Six narrative engines | Close reading, version comparison, moral contrast, image archaeology, time echo, honest observation |
| Evidence safeguards | Separate documentary records, interpretation, adaptation, reconstruction, dispute, and unverified claims |
| Editorial review | Facts-first gate; protect user-frozen passages; minimal approved changes |
| Visual treatment | Single-image-first, variable medium and composition, no forced carousel |
| Local helpers | Standard-library-only character count and CSV metrics reports |

## Quick start

Clone the repository and copy the **entire** `humanities-essay/` directory to a compatible agent's skill path. Keep the `SKILL.md` manifest and sibling `references/`, `assets/`, and `scripts/` together. Tool-specific installation directories and invocation syntax may differ.

```bash
git clone https://github.com/2023violet/humanities-essay.git
python humanities-essay/humanities-essay/scripts/quick_validate.py humanities-essay/humanities-essay
python -m unittest discover -s humanities-essay/tests -v
```

Example: “Use humanities-essay to write a Chinese narrative about a historical figure with a falsifiable thesis, documented quotations, one optional cover image, and an independent fact review.”

## Principles

Strong emotions do not prove historical claims. A striking turn of phrase is not a citation. Five internally reviewed stories suggested useful techniques, but they are not full model-quality validation. Editorial scores are diagnostic, never promises of viral reach. This repository does not bundle third-party texts, images, audio or private creator analytics.

## Documentation and contributions

[Architecture](docs/ARCHITECTURE.md) · [Validation](docs/VALIDATION.md) · [Roadmap](docs/ROADMAP.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [Security](SECURITY.md)

Original instructions and scripts: [Apache-2.0](LICENSE); third-party content retains its own rights.
