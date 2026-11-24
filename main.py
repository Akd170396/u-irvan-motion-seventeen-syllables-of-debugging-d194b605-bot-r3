#!/usr/bin/env python3
"""Seventeen Syllables of Debugging (round 3).

Writes one haiku about debugging to $MAKEFUN_OUTPUT_DIR/entry.txt.
Stdlib only, deterministic: the same bytes on every run.
"""
import os
import sys

HAIKU = (
    "git blame points at me\n"
    "the commit is from last spring\n"
    "past me strikes again\n"
)

# Syllable counts for every word in the haiku, counted by hand.
SYLLABLES = {
    "git": 1, "blame": 1, "points": 1, "at": 1, "me": 1,
    "the": 1, "commit": 2, "is": 1, "from": 1, "last": 1, "spring": 1,
    "past": 1, "strikes": 1, "again": 2,
}


def count_syllables(word):
    """Syllables in one word: exact table lookup, else vowel-group estimate."""
    w = word.strip(".,;:!?\"'").lower()
    if w in SYLLABLES:
        return SYLLABLES[w]
    groups = 0
    prev_vowel = False
    for ch in w:
        vowel = ch in "aeiouy"
        if vowel and not prev_vowel:
            groups += 1
        prev_vowel = vowel
    if w.endswith("e") and groups > 1:
        groups -= 1
    return max(1, groups)


def line_syllables(line):
    return sum(count_syllables(w) for w in line.split())


def validate(text):
    """Gate the entry exactly the way the sealed scorer does, plus the
    5-7-5 shape: 1-200 chars, not only whitespace, three lines, 5-7-5."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > 200:
        raise ValueError("entry is %d chars, over the 200-char limit" % len(text))
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 3:
        raise ValueError("entry must be exactly 3 lines, got %d" % len(lines))
    counts = [line_syllables(line) for line in lines]
    if counts != [5, 7, 5]:
        raise ValueError("syllable shape is %s, must be [5, 7, 5]" % counts)
    return counts


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    counts = validate(HAIKU)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(HAIKU)
    # Read-back verification: the file on disk must be byte-identical to
    # the validated haiku, or the run fails loudly instead of submitting
    # a truncated or altered entry.
    with open(path, "r", encoding="utf-8", newline="") as f:
        on_disk = f.read()
    if on_disk != HAIKU:
        raise SystemExit(
            "read-back mismatch: %s holds %r, expected the validated haiku"
            % (path, on_disk)
        )
    sys.stderr.write("wrote %s (%d chars, syllables %s)\n" % (path, len(HAIKU), counts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
