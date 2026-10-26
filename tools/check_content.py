"""Static content and source integrity checks for the learning site."""
from __future__ import annotations

import ast
import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

from build_content import parse_rows
from solutions import SOLUTIONS


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_IDS = (
    "1 49 128 283 11 15 42 3 438 560 239 76 53 56 189 238 41 73 54 48 "
    "240 160 206 234 141 142 21 2 19 24 25 138 148 23 146 94 104 226 101 "
    "543 102 108 98 230 199 114 105 437 236 124 200 994 207 208 46 78 17 "
    "39 22 79 131 51 35 74 34 33 153 4 20 155 394 739 84 215 347 295 121 "
    "55 45 763 70 118 198 279 322 139 300 152 416 32 62 64 5 1143 72 136 "
    "169 75 31 287"
).split()


class IndexParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.scripts: list[str] = []
        self.styles: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "script" and values.get("src"):
            self.scripts.append(values["src"] or "")
        if tag == "link" and values.get("rel") == "stylesheet" and values.get("href"):
            self.styles.append(values["href"] or "")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    rows = parse_rows()
    if len(rows) != 100:
        fail(f"expected 100 rows, got {len(rows)}")
    ids = [str(row["id"]) for row in rows]
    if ids != EXPECTED_IDS:
        fail("problem IDs/order differ from the verified official study-plan snapshot")
    if len(set(ids)) != 100 or len({row["slug"] for row in rows}) != 100:
        fail("duplicate problem ID or slug")
    if len({row["category"] for row in rows}) != 17:
        fail("expected 17 categories")
    difficulty = Counter(row["difficulty"] for row in rows)
    if difficulty != Counter({"EASY": 20, "MEDIUM": 68, "HARD": 12}):
        fail(f"unexpected difficulty distribution: {difficulty}")

    required = ("title", "summary", "signal", "invariant", "steps", "time", "space", "pitfall", "code")
    for row in rows:
        for key in required:
            if not row[key]:
                fail(f"problem {row['id']} missing {key}")
        if len(row["steps"]) < 3:
            fail(f"problem {row['id']} needs at least three reasoning steps")
        if "待补充" in row["code"]:
            fail(f"problem {row['id']} still has placeholder code")
        try:
            ast.parse(str(row["code"]))
        except SyntaxError as error:
            fail(f"problem {row['id']} Python syntax error: {error}")

    if len(SOLUTIONS) != 100 or set(SOLUTIONS) != set(ids):
        fail("solution mapping does not match problem set")

    expected_files = ["index.html", "styles.css", "app.js", "problems.js"]
    for name in expected_files:
        if not (ROOT / "dist" / name).is_file():
            fail(f"missing dist/{name}")

    parser = IndexParser()
    parser.feed((ROOT / "dist" / "index.html").read_text(encoding="utf-8"))
    required_ids = {
        "problem-list", "search-input", "category-nav", "status-filters",
        "difficulty-filters", "problem-dialog", "problem-detail", "mark-done"
    }
    missing_ids = required_ids - parser.ids
    if missing_ids:
        fail(f"missing interactive elements: {sorted(missing_ids)}")
    for local_asset in ("styles.css", "problems.js", "app.js"):
        if local_asset not in parser.scripts + parser.styles:
            fail(f"index does not reference {local_asset}")

    bundle = (ROOT / "dist" / "problems.js").read_text(encoding="utf-8")
    prefix = "window.HOT100_PROBLEMS="
    if not bundle.startswith(prefix) or not bundle.rstrip().endswith(";"):
        fail("invalid problems.js wrapper")
    payload = json.loads(bundle[len(prefix):].strip()[:-1])
    if len(payload) != 100:
        fail("generated browser bundle does not contain 100 problems")

    print("PASS: 100 problems / 17 categories / 100 Python solutions")
    print(f"PASS: difficulty distribution {dict(difficulty)}")
    print("PASS: HTML hooks, local assets, JSON bundle, and Python syntax")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()

