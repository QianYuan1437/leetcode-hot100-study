"""Fetch structured problem statements/examples for the curated HOT 100 list.

The source repository is CC BY-SA 4.0 licensed.  This script keeps a source URL
for every record so the generated learning material remains auditable.
"""
from __future__ import annotations

import concurrent.futures
import html
import json
import re
import subprocess
import time
from pathlib import Path
from urllib.parse import quote

from build_content import parse_rows


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "doocs/leetcode"
BASE_WEB_URL = "https://github.com/doocs/leetcode/blob/main/"


def gh_api(endpoint: str, *, raw: bool = False, attempts: int = 8) -> str:
    command = ["gh", "api", "--cache", "1h"]
    if raw:
        command.extend(["-H", "Accept: application/vnd.github.raw+json"])
    command.append(endpoint)
    for attempt in range(1, attempts + 1):
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode == 0:
            return result.stdout
        if attempt == attempts:
            raise RuntimeError(f"GitHub API failed for {endpoint}: {result.stderr.strip()}")
        time.sleep(attempt)
    raise AssertionError("unreachable")


def plain_text(fragment: str) -> str:
    fragment = re.sub(r"<sup[^>]*>(.*?)</sup>", r"^\1", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<sub[^>]*>(.*?)</sub>", r"_\1", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"</(?:p|div|li|h\d|pre)>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"<li[^>]*>", "- ", fragment, flags=re.I)
    fragment = re.sub(r"</?[A-Za-z][^>]*>", "", fragment)
    text = html.unescape(fragment).replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def normalize_statement(description: str, fallback: str) -> str:
    first_example = re.search(
        r"<(?:strong|b)[^>]*(?:class=\"example\")?[^>]*>\s*示例|<(?:strong|b)[^>]*>\s*输入",
        description,
        flags=re.I,
    )
    lead = description[: first_example.start()] if first_example else description
    lead = re.sub(r"<p>\s*&nbsp;\s*</p>", "", lead, flags=re.I)
    text = plain_text(lead)
    if len(text) < 20:
        text = fallback
    # Light editorial normalization keeps the page a readable Chinese restatement
    # instead of exposing raw HTML copied from the reference repository.
    replacements = (
        ("请你设计并实现", "需要设计并实现"),
        ("请你", "需要"),
        ("请判断", "需要判断"),
        ("请返回", "需要输出"),
        ("返回", "输出"),
        ("给你", "输入给出"),
        ("给定", "输入给出"),
    )
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def extract_examples(description: str) -> list[str]:
    examples: list[str] = []
    for block in re.findall(r"<pre[^>]*>(.*?)</pre>", description, flags=re.I | re.S):
        text = plain_text(block)
        if text and ("输入" in text or "Input" in text) and ("输出" in text or "Output" in text):
            examples.append(text)
    # Newer LeetCode descriptions use ordinary paragraphs inside an
    # ``example-block`` div instead of a preformatted block. Splitting on the
    # explicit example heading also survives nested divs and embedded lists.
    sections = re.split(
        r"<p[^>]*>\s*<(?:strong|b)[^>]*>\s*示例\s*\d*\s*[：:]?\s*</(?:strong|b)>\s*</p>",
        description,
        flags=re.I,
    )[1:]
    for section in sections:
        section = re.split(
            r"<p[^>]*>\s*<(?:strong|b)[^>]*>\s*(?:示例\s*\d*|提示|Constraints)\s*[：:]?\s*</(?:strong|b)>",
            section,
            maxsplit=1,
            flags=re.I,
        )[0]
        text = plain_text(section)
        if text and ("输入" in text or "Input" in text) and ("输出" in text or "Output" in text):
            examples.append(text)
    return list(dict.fromkeys(examples))


def extract_constraints(description: str) -> list[str]:
    marker = re.search(
        r"<(?:strong|b)[^>]*>\s*(?:提示|Constraints)\s*[：:]?\s*</(?:strong|b)>",
        description,
        flags=re.I,
    )
    tail = description[marker.end():] if marker else description
    match = re.search(r"<ul[^>]*>(.*?)</ul>", tail, flags=re.I | re.S)
    if not match:
        lists = re.findall(r"<ul[^>]*>(.*?)</ul>", description, flags=re.I | re.S)
        match_text = lists[-1] if lists else ""
    else:
        match_text = match.group(1)
    constraints = [plain_text(item) for item in re.findall(r"<li[^>]*>(.*?)</li>", match_text, flags=re.I | re.S)]
    return [item.removeprefix("- ").strip() for item in constraints if item.strip()]


def discover_paths(rows: list[dict[str, object]]) -> dict[str, str]:
    ids = {str(row["id"]) for row in rows}
    ranges = sorted({(int(problem_id) // 100) * 100 for problem_id in ids})
    paths: dict[str, str] = {}
    for start in ranges:
        directory = f"solution/{start:04d}-{start + 99:04d}"
        listing = json.loads(gh_api(f"repos/{REPOSITORY}/contents/{directory}"))
        for item in listing:
            match = re.match(r"(\d{4})\.", item.get("name", ""))
            if not match:
                continue
            problem_id = str(int(match.group(1)))
            if problem_id in ids:
                paths[problem_id] = f"{item['path']}/README.md"
    missing = sorted(ids - paths.keys(), key=int)
    if missing:
        raise RuntimeError(f"Cannot find source paths for IDs: {missing}")
    return paths


def fetch_one(row: dict[str, object], path: str) -> tuple[str, dict[str, object]]:
    endpoint = f"repos/{REPOSITORY}/contents/{quote(path, safe='/')}"
    markdown = gh_api(endpoint, raw=True)
    match = re.search(
        r"<!-- description:start -->(.*?)<!-- description:end -->",
        markdown,
        flags=re.S,
    )
    if not match:
        raise RuntimeError(f"Missing description block for problem {row['id']}")
    description = match.group(1)
    examples = extract_examples(description)
    constraints = extract_constraints(description)
    if not examples:
        raise RuntimeError(f"No input/output example found for problem {row['id']}")
    return str(row["id"]), {
        "statement": normalize_statement(description, str(row["summary"])),
        "examples": examples,
        "constraints": constraints,
        "source_url": BASE_WEB_URL + quote(path, safe="/"),
        "source_license": "CC BY-SA 4.0",
    }


def main() -> None:
    rows = parse_rows()
    paths = discover_paths(rows)
    details: dict[str, dict[str, object]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(fetch_one, row, paths[str(row["id"])]) for row in rows]
        for index, future in enumerate(concurrent.futures.as_completed(futures), 1):
            problem_id, record = future.result()
            details[problem_id] = record
            print(f"fetched {index:3d}/100: {problem_id}", flush=True)
    ordered = {str(row["id"]): details[str(row["id"])] for row in rows}
    target = ROOT / "tools" / "problem_details.json"
    target.write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(ordered)} structured problem details to {target}")


if __name__ == "__main__":
    main()
