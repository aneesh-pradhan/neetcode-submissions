#!/usr/bin/env python3
"""Rebuild the problem index in README.md from solution files on disk.

The problem column is the problem-folder name with ``-`` and ``_`` turned
into spaces. Category is the top-level topic folder. Difficulty is set only
when a folder or file name contains the token easy, medium, or hard.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START = "<!-- INDEX:START -->"
END = "<!-- INDEX:END -->"

SKIP_DIR_NAMES = {".git", ".github", "scripts", "__pycache__"}

EXTENSIONS = {
    ".c": "C",
    ".cc": "C++",
    ".cpp": "C++",
    ".cs": "C#",
    ".cxx": "C++",
    ".go": "Go",
    ".java": "Java",
    ".js": "JavaScript",
    ".kt": "Kotlin",
    ".py": "Python",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".sql": "SQL",
    ".swift": "Swift",
    ".ts": "TypeScript",
}

DIFFICULTIES = {"easy", "medium", "hard"}
TOKEN_SPLIT = re.compile(r"[^A-Za-z0-9]+")
SUBMISSION_NAME = re.compile(r"submission-(\d+)\Z")


def display_name(slug: str) -> str:
    return TOKEN_SPLIT.sub(" ", slug).strip().title()


def difficulty_from_parts(parts: tuple[str, ...]) -> str:
    for part in parts:
        stem = Path(part).stem
        for token in TOKEN_SPLIT.split(stem):
            if token.lower() in DIFFICULTIES:
                return token.title()
    return ""


def submission_sort_key(stem: str) -> tuple[int, int | str]:
    match = SUBMISSION_NAME.fullmatch(stem)
    if match:
        return (0, int(match.group(1)))
    return (1, stem)


def iter_solutions() -> list[dict[str, str]]:
    rows: list[dict[str, object]] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in SKIP_DIR_NAMES or part.startswith(".") for part in relative.parts):
            continue
        language = EXTENSIONS.get(path.suffix.lower())
        if language is None:
            continue
        parts = relative.parts
        if len(parts) >= 3:
            category = parts[0]
            problem_slug = parts[-2]
        elif len(parts) == 2:
            category = parts[0]
            problem_slug = path.stem
        else:
            category = ""
            problem_slug = path.stem
        rows.append(
            {
                "problem": display_name(problem_slug),
                "slug": problem_slug,
                "category": category,
                "difficulty": difficulty_from_parts(parts),
                "language": language,
                "file": path.name,
                "rel": relative.as_posix(),
                "sort": (
                    category.casefold(),
                    problem_slug.casefold(),
                    submission_sort_key(path.stem),
                    relative.as_posix().casefold(),
                ),
            }
        )
    rows.sort(key=lambda row: row["sort"])
    return [
        {
            "problem": str(row["problem"]),
            "category": str(row["category"]),
            "difficulty": str(row["difficulty"]),
            "language": str(row["language"]),
            "file": str(row["file"]),
            "rel": str(row["rel"]),
        }
        for row in rows
    ]


def markdown_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def solution_link(relative: str, label: str) -> str:
    href = urllib.parse.quote(relative, safe="/")
    safe_label = markdown_cell(label)
    return f"[{safe_label}]({href})"


def render_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "| Problem | Category | Difficulty | Language | Solution |",
        "| --- | --- | --- | --- | --- |",
    ]
    if not rows:
        lines.append("| | | | | |")
        return "\n".join(lines)
    for row in rows:
        lines.append(
            "| {problem} | {category} | {difficulty} | {language} | {solution} |".format(
                problem=markdown_cell(row["problem"]),
                category=markdown_cell(row["category"]),
                difficulty=markdown_cell(row["difficulty"]),
                language=markdown_cell(row["language"]),
                solution=solution_link(row["rel"], row["file"]),
            )
        )
    return "\n".join(lines)


def replace_index(text: str, table: str) -> str:
    start = text.find(START)
    end = text.find(END)
    if start == -1 or end == -1 or end < start:
        raise SystemExit(f"{README.name} is missing the {START} / {END} markers")
    end += len(END)
    block = f"{START}\n\n{table}\n\n{END}"
    return text[:start] + block + text[end:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 when README.md does not match the solution files",
    )
    args = parser.parse_args(argv)
    original = README.read_text(encoding="utf-8")
    updated = replace_index(original, render_table(iter_solutions()))
    if args.check:
        if original != updated:
            print(
                "README.md index is stale. Run: python3 scripts/gen_index.py",
                file=sys.stderr,
            )
            return 1
        print("README.md index is up to date.")
        return 0
    if updated != original:
        README.write_text(updated, encoding="utf-8")
        print("Updated README.md")
    else:
        print("README.md index already matches the tree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
