import argparse
import os
import re
from pathlib import Path


ADMONITION_RE = re.compile(
    r"^([ \t]*)(!!!|\?\?\?)(\+?)\s+([A-Za-z0-9_-]+)(?:\s+(.*?))?\s*$"
)
FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})")
UTF8_BOM = b"\xef\xbb\xbf"
SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", "site"}


def split_eol(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def normalize_title(raw_title: str | None) -> str:
    if not raw_title:
        return ""

    title = raw_title.strip()
    if len(title) >= 2 and title[0] == title[-1] and title[0] in {'"', "'"}:
        return title[1:-1]
    return title


def callout_suffix(marker: str, plus: str) -> str:
    if marker == "!!!":
        return ""
    return "+" if plus else "-"


def body_prefixes(indent: str) -> tuple[str, str]:
    return indent + "    ", indent + "\t"


def is_body_line(text: str, indent: str) -> bool:
    return any(text.startswith(prefix) for prefix in body_prefixes(indent))


def strip_body_indent(text: str, indent: str) -> str:
    prefixes = sorted(body_prefixes(indent), key=len, reverse=True)
    for prefix in prefixes:
        if text.startswith(prefix):
            return text[len(prefix):]
    return text


def next_nonblank_is_body(lines: list[str], start: int, indent: str) -> bool:
    for line in lines[start + 1:]:
        text, _ = split_eol(line)
        if not text.strip():
            continue
        return is_body_line(text, indent)
    return False


def convert_lines(lines: list[str]) -> tuple[list[str], int]:
    converted: list[str] = []
    count = 0
    in_fence = False
    fence_char = ""
    fence_len = 0
    index = 0

    while index < len(lines):
        line = lines[index]
        text, eol = split_eol(line)
        fence = FENCE_RE.match(text)

        if fence:
            fence_marker = fence.group(1)
            char = fence_marker[0]
            length = len(fence_marker)
            if not in_fence:
                in_fence = True
                fence_char = char
                fence_len = length
            elif char == fence_char and length >= fence_len:
                in_fence = False
                fence_char = ""
                fence_len = 0

            converted.append(line)
            index += 1
            continue

        match = None if in_fence else ADMONITION_RE.match(text)
        if not match:
            converted.append(line)
            index += 1
            continue

        indent, marker, plus, kind, raw_title = match.groups()
        suffix = callout_suffix(marker, plus)
        title = normalize_title(raw_title)
        title_part = f" {title}" if title else ""
        converted.append(f"{indent}> [!{kind}]{suffix}{title_part}{eol}")
        count += 1

        body_lines: list[str] = []
        body_index = index + 1
        while body_index < len(lines):
            body_text, body_eol = split_eol(lines[body_index])

            if not body_text.strip():
                if next_nonblank_is_body(lines, body_index, indent):
                    body_lines.append(body_eol)
                    body_index += 1
                    continue
                break

            if not is_body_line(body_text, indent):
                break

            body_lines.append(strip_body_indent(body_text, indent) + body_eol)
            body_index += 1

        nested_lines, nested_count = convert_lines(body_lines)
        count += nested_count

        for body_line in nested_lines:
            body_text, body_eol = split_eol(body_line)
            if body_text:
                converted.append(f"{indent}> {body_text}{body_eol}")
            else:
                converted.append(f"{indent}>{body_eol}")

        index = body_index

    return converted, count


def convert_text(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    converted_lines, count = convert_lines(lines)
    return "".join(converted_lines), count


def read_utf8(path: Path) -> tuple[str, bool]:
    data = path.read_bytes()
    has_bom = data.startswith(UTF8_BOM)
    if has_bom:
        data = data[len(UTF8_BOM):]
    return data.decode("utf-8"), has_bom


def write_utf8(path: Path, text: str, has_bom: bool) -> None:
    data = text.encode("utf-8")
    if has_bom:
        data = UTF8_BOM + data
    path.write_bytes(data)


def iter_markdown_files(paths: list[Path]):
    for path in paths:
        if path.is_file() and path.suffix.lower() == ".md":
            yield path
            continue

        if not path.is_dir():
            continue

        for root, dirs, files in os.walk(path):
            dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
            for filename in files:
                child = Path(root) / filename
                if child.suffix.lower() == ".md":
                    yield child


def convert_file(path: Path, write: bool) -> tuple[bool, int]:
    original, has_bom = read_utf8(path)
    converted, count = convert_text(original)
    changed = converted != original

    if changed and write:
        write_utf8(path, converted, has_bom)

    return changed, count


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Convert MkDocs admonitions (!!!, ???, ???+) to Obsidian-style "
            "callouts while preserving type, title, and fold state."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["docs"],
        help="Markdown files or folders to scan. Defaults to docs.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write converted files. Without this flag, only show a dry-run report.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with status 1 if any file would change.",
    )
    args = parser.parse_args()

    paths = [Path(path).expanduser().resolve() for path in args.paths]
    total_files = 0
    changed_files = 0
    total_blocks = 0

    for markdown_file in iter_markdown_files(paths):
        total_files += 1
        changed, count = convert_file(markdown_file, args.write)
        if not changed:
            continue

        changed_files += 1
        total_blocks += count
        action = "Converted" if args.write else "Would convert"
        print(f"{action}: {markdown_file} ({count} block{'s' if count != 1 else ''})")

    mode = "write" if args.write else "dry-run"
    print(
        f"Done ({mode}). Scanned {total_files} Markdown files, "
        f"{changed_files} file{'s' if changed_files != 1 else ''} changed, "
        f"{total_blocks} admonition block{'s' if total_blocks != 1 else ''} found."
    )

    if args.check and changed_files:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
