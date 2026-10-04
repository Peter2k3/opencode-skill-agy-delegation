#!/usr/bin/env python3
"""Dependency-free structural checks for the published OpenCode skill."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "agy-delegation" / "SKILL.md"
REFERENCE = ROOT / "skills" / "agy-delegation" / "references" / "agy-cli.md"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not SKILL.is_file():
        fail(f"missing skill file: {SKILL}")
    if not REFERENCE.is_file():
        fail(f"missing reference: {REFERENCE}")

    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")

    end = text.find("\n---\n", 4)
    if end == -1:
        fail("SKILL.md has no closing frontmatter delimiter")
    frontmatter = text[4:end]
    body = text[end + len("\n---\n") :]

    required_fields = ("name:", "description:", "license:", "metadata:", "author:", "version:")
    for field in required_fields:
        if not re.search(rf"(?m)^\s*{re.escape(field)}", frontmatter):
            fail(f"missing frontmatter field: {field}")

    name = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", frontmatter)
    if not name or name.group(1) != "agy-delegation":
        fail("skill name must be agy-delegation")

    description = re.search(r"(?m)^description:\s*[\"'](.*)[\"']\s*$", frontmatter)
    if not description:
        fail("description must be quoted and single-line")
    if len(description.group(1)) > 250:
        fail("description exceeds 250 characters")

    sections = [
        "## Activation Contract",
        "## Hard Rules",
        "## Decision Gates",
        "## Execution Steps",
        "## Output Contract",
        "## References",
    ]
    positions = [body.find(section) for section in sections]
    if any(position == -1 for position in positions):
        fail("SKILL.md is missing a required runtime section")
    if positions != sorted(positions):
        fail("runtime sections are out of order")

    if len(re.findall(r"\b[\w'-]+\b", body)) > 1000:
        fail("skill body exceeds the 1000-word hard limit")
    if "references/agy-cli.md" not in text:
        fail("skill must reference its local CLI notes")

    machine_path_patterns = (
        re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+"),
        re.compile(r"[A-Za-z]:[\\/]Users[\\/][A-Za-z0-9._-]+"),
    )
    for markdown_file in (ROOT / "skills").rglob("*.md"):
        markdown = markdown_file.read_text(encoding="utf-8")
        if any(pattern.search(markdown) for pattern in machine_path_patterns):
            fail(f"skill reference contains a machine-specific home directory: {markdown_file}")

    print("PASS: agy-delegation skill structure is valid")


if __name__ == "__main__":
    main()
