#!/usr/bin/env python3
"""Make the AI Judge Laugh — entry program.

Writes a single original one-line joke about office life to
/output/entry.txt (the grader sandbox output path) and to
out/entry.txt next to this script. Fully deterministic: the same
fixed text every run, no network, no randomness, no external input.
"""

import os
import sys

JOKE = "The printer jammed again, so IT emailed me a PDF on why printers jam. I printed it."

MAX_CHARS = 200


def validate_entry(text: str) -> str | None:
    """Return an error message if the entry is invalid, else None.

    Guards the invariants the grader expects: one printable line,
    within the character budget, with no stray control characters.
    """
    if not (1 <= len(text) <= MAX_CHARS):
        return f"entry is {len(text)} chars; must be 1-{MAX_CHARS}"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        return "entry contains a control character"
    return None


def output_paths() -> list:
    """Paths to write. The grader sandbox provides /output; a local
    copy beside this script makes the result verifiable without
    racing other builders on the shared /output mount."""
    here = os.path.dirname(os.path.abspath(__file__))
    paths = [os.path.join(here, "out", "entry.txt")]
    if os.path.isdir("/output"):
        paths.append("/output/entry.txt")
    return paths


def write_entry(text: str, paths: list) -> None:
    """Write the entry (plus trailing newline) to every output path."""
    for path in paths:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text + "\n")


def main() -> int:
    text = JOKE.strip()
    error = validate_entry(text)
    if error is not None:
        print(error, file=sys.stderr)
        return 1
    paths = output_paths()
    write_entry(text, paths)
    print(f"wrote {len(text)} chars to {', '.join(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
