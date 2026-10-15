#!/usr/bin/env python3
"""Check local targets in inline Markdown links without third-party packages."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))")
SKIP_DIRS = {".git", ".github", "node_modules", "vendor", ".venv"}
BACKTICK = chr(96)


def markdown_files() -> list[Path]:
    return sorted(
        path for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".md", ".markdown"}
        and not any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts)
    )


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    in_fence = False
    fence_marker = ""
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.lstrip()
        marker = BACKTICK * 3 if stripped.startswith(BACKTICK * 3) else ("~~~" if stripped.startswith("~~~") else "")
        if marker:
            if not in_fence:
                in_fence = True
                fence_marker = marker[0]
            elif marker[0] == fence_marker:
                in_fence = False
            continue
        if in_fence:
            continue

        for match in LINK_RE.finditer(line):
            target = match.group(1) or match.group(2) or ""
            if not target or target.startswith("#"):
                continue
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            local_path = unquote(parsed.path)
            if not local_path:
                continue
            candidate = (path.parent / local_path).resolve()
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: link escapes repository: {target}")
                continue
            if not candidate.exists():
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: missing local target: {target}")
    return errors


def main() -> int:
    files = markdown_files()
    errors = [error for path in files for error in check_file(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"Found {len(errors)} broken local Markdown link(s) across {len(files)} files.", file=sys.stderr)
        return 1
    print(f"Checked local inline Markdown links in {len(files)} Markdown files; no missing targets found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
