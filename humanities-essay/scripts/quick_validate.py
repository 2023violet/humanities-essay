#!/usr/bin/env python3
"""Validate the static structure of humanities-essay. Standard library only.

Does not validate factual accuracy, external citations, prose quality, or model behavior.
"""
import re
import sys
from pathlib import Path

EXPECTED = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/corpus-findings.md",
    "references/story-architectures.md",
    "references/narrative-toolkit.md",
    "references/rhetorical-craft.md",
    "references/evidence-protocol.md",
    "references/platform-playbooks.md",
    "references/editorial-qa.md",
    "assets/creative-brief.md",
    "assets/evidence-ledger.md",
    "evals/acceptance-cases.md",
    "evals/regression-matrix.md",
    "README.md",
    "CHANGELOG.md",
    "scripts/quick_validate.py",
    "scripts/check_length.py",
    "scripts/metrics_report.py",
    "references/visual-editorial.md",
    "references/five-case-study.md",
    "references/measurement.md",
    "references/first-person-and-era-essays.md",
    "references/rhythm-and-line-editing.md",
    "references/revision-governance.md",
    "references/sixth-case-lessons.md",
    "assets/author-experience-ledger.md",
    "assets/revision-decision-log.md",
    "assets/metrics-template.csv",
}


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = []
    paths = sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts and ".git" not in p.parts and p.suffix not in {".pyc", ".pyo"})
    rels = {p.relative_to(root).as_posix() for p in paths}
    for missing in sorted(EXPECTED - rels):
        errors.append(f"Missing required file: {missing}")
    for path in paths:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append(f"Not UTF-8: {path.relative_to(root)}")
            continue
        # Placeholders only: test cases deliberately contain phrases about invented sources.
        if path.suffix in {".md", ".yaml"} and re.search(r"(?i)(TODO\s*:\s*fill|\[insert\s+description\]|your-skill-name|<YOUR_SKILL_NAME>)", content):
            errors.append(f"Template placeholder: {path.relative_to(root)}")
        if path.suffix == ".md":
            for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", content):
                target = target.split("#", 1)[0]
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                referenced = (path.parent / target).resolve()
                if not referenced.is_file() or not referenced.is_relative_to(root):
                    errors.append(f"Broken relative link in {path.relative_to(root)}: {target}")
    skill = (root / "SKILL.md").read_text(encoding="utf-8") if "SKILL.md" in rels else ""
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
    if not frontmatter:
        errors.append("SKILL.md frontmatter missing or malformed")
    else:
        front = frontmatter.group(1)
        name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", front, re.M)
        desc = re.search(r"^description:\s*(.+)$", front, re.M)
        version = re.search(r'^\s*version:\s*["\']?([0-9.]+)["\']?\s*$', front, re.M)
        if not name or name.group(1) != root.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name.group(1)):
            errors.append("Invalid or mismatched skill name")
        if not desc or not (1 <= len(desc.group(1)) <= 1024):
            errors.append("Invalid description length")
        if not version or version.group(1) != "3.2.0":
            errors.append("Expected metadata.version 3.2.0")
    # Agent Skills top-level metadata requirements.
    if frontmatter:
        front = frontmatter.group(1)
        if not re.search(r"^license:\s*Apache-2\.0\s*$", front, re.M):
            errors.append("Expected skill license metadata Apache-2.0")
    agent = (root / "agents/openai.yaml").read_text(encoding="utf-8") if "agents/openai.yaml" in rels else ""
    if "interface:" not in agent or "policy:" not in agent:
        errors.append("agents/openai.yaml missing interface or policy")
    if "$humanities-essay" not in agent:
        errors.append("Codex default_prompt does not reference $humanities-essay")
    if not re.search(r"^\s*allow_implicit_invocation:\s*true\s*$", agent, re.M):
        errors.append("Codex implicit invocation configuration mismatch")
    if errors:
        print("FAIL:")
        for error in errors:
            print(" -", error)
        return 1
    print(f"PASS: static validation; {len(paths)} UTF-8 files, required paths, metadata and internal links verified")
    print("NOTE: This does not verify historical claims or real model generation quality")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
