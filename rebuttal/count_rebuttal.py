"""Count Unicode characters including whitespace, with reserved space for author TODOs."""
import argparse
import re
from pathlib import Path

BLOCK = re.compile(r'<block\s+characters="(\d+)"\s+contents-ignored\s*>((?:(?!</?block\b).)*)</block>', re.S)


def projected_length(text):
    reserved = sum(int(match[1]) for match in BLOCK.finditer(text))
    visible = BLOCK.sub("", text)
    if re.search(r"</?block\b", visible):
        raise ValueError("Malformed or nested placeholder block")
    return len(visible) + reserved


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--limit", type=int, required=True)
    args = parser.parse_args()
    count = projected_length(args.file.read_text(encoding="utf-8-sig"))
    print(f"{count}/{args.limit} characters ({args.limit - count} remaining)")
    raise SystemExit(int(count > args.limit))
