# AGENTS.md — contribution guardrails

- Respect the task scope. Review-only means no file edits, commits or release changes.
- Before modifying a source, read it and write a verifiable, minimal plan when nontrivial.
- Never invent a historical citation, a user's lived experience, model-evaluation success, publishing metrics or third-party permissions.
- Keep changes surgical. Only update directly impacted files, references and tests.
- Require explicit confirmation before deleting files, changing permissions, force-pushing or publishing releases.
- Keep `humanities-essay/SKILL.md` lean; detailed patterns belong under `references/`.
- Run `python humanities-essay/scripts/quick_validate.py humanities-essay` and `python -m unittest discover -s tests -v` before proposing a PR.
- Do not commit private creator-dashboard screenshots, personal records, copyrighted source essays, generated art without rights review, or API credentials.
- Include a test or an evidence rationale for changed behavior. Static PASS is not model-quality PASS.
