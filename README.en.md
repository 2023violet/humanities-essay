<div align="center">

# Humanities Essay

**Evidence-led Chinese humanities storytelling, with honest facts and memorable prose.**

[![Validation](https://github.com/2023violet/humanities-essay/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/2023violet/humanities-essay/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
![Version](https://img.shields.io/badge/version-3.2.0-informational)

[简体中文](README.md) · **English**

</div>

`humanities-essay` is an [Agent Skills](https://agentskills.io/)-compatible writing and editing workflow for Chinese-language history, poetry, literature, cultural criticism, contemporary essays, and authentic first-person narratives. It provides source separation, structural choices, contradiction testing, restrained prose, review-only editing, and optional single-image publishing guidance.

## Features

| Capability | Approach |
|---|---|
| Research and framing | Two competing thesis candidates, source ledger, counterevidence |
| Seven optional narrative routes | Close reading, version comparison, moral contrast, image archaeology, time echo, honest observation, contemporary personal perspective |
| Evidence safeguards | Separate documentary records, interpretation, adaptation, reconstruction, dispute, and unverified claims |
| Editorial review | Facts-first gate; protect user-frozen passages; minimal approved changes |
| First-person provenance | Distinguish user-confirmed experience from external facts and hypotheses |
| Natural language editing | Check correctness, flow and literary effect independently; punctuation counts are not KPIs |
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

## v3.2: Beyond historical biographies

The skill now supports source-grounded first-person essays, contemporary technology and society observations, and ordinary people's lived experience, without forcing a historical parallel. It distinguishes verified autobiographical claims from researched external facts and editorial hypotheses.

Language editing uses three separate checks: grammatical correctness, natural sentence flow, and literary effect. Sentence-ending punctuation counts are **not** quality metrics. Author-approved lines and endings are protected, and editorial iteration stops when remaining differences are only matters of taste. New references: `first-person-and-era-essays.md`, `rhythm-and-line-editing.md`, `revision-governance.md`. The anonymized sixth-case retrospective contains no personal essay text.
