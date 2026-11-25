"""One Line, Big Laugh — a one-line entry for make.fun.

The program writes exactly one funny line to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Python 3.13, standard library only, no network.
"""

import os
from pathlib import Path

LINE = "My therapist told me to schedule my worries instead of spiraling, so now I have a full-blown panic attack every Tuesday at 4 p.m., with an agenda and snacks."

MAX_CHARS = 200


def _validate(text: str) -> None:
    """Check the entry against the bounty's single-line / length rules."""
    assert text, "entry must not be empty"
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert 1 <= len(text) <= MAX_CHARS, f"entry is {len(text)} chars, cap is {MAX_CHARS}"


def main() -> None:
    text = LINE.strip()
    _validate(text)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(text, encoding="utf-8")

    # Read back and verify what actually landed on disk, byte for byte.
    # This guards against truncated writes or encoding surprises: the file
    # on disk, not just the in-memory string, is what gets scored.
    written = out_path.read_text(encoding="utf-8")
    assert written == text, f"read-back mismatch: file has {written!r}, expected {text!r}"
    assert len(written) == len(text) == 157, (
        f"read-back length mismatch: file={len(written)}, expected={len(text)}"
    )
    print(f"wrote {len(text)} chars to {out_path} (read-back verified, 157-char entry)")


if __name__ == "__main__":
    main()
