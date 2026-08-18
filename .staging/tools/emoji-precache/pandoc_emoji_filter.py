#!/usr/bin/env python3
"""pandoc_emoji_filter: Pandoc filter that replaces Unicode emojis with inline images.

Intended for use with pandoc when producing output formats (e.g. PDF via LaTeX)
that cannot render colored Unicode emoji natively.  Each emoji character found
in a ``Str`` node is replaced by an ``Image`` inline element pointing to the
corresponding PNG asset in ``assets/emojis/``.  Surrounding text is preserved
as ``Str`` nodes so that the document structure is unchanged.

Usage::

    pandoc --filter scripts/pandoc_emoji_filter.py input.md -o output.pdf

References:
    - https://github.com/jgm/pandocfilters
    - https://github.com/masbicudo/Pandoc-Emojis-Filter
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import emoji
from emoji.core import EmojiMatch
from pandocfilters import Image, Str, attributes, toJSONFilter

if TYPE_CHECKING:
    from pandocfilters import PandocFormat, PandocMeta

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parent.parent
EMOJI_ASSET_DIR = str(_REPO_ROOT / "assets" / "emojis")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _asset_name_for(char: str) -> str | None:
    """Return the PNG base-name (without extension) for *char*, or ``None``.

    The lookup prefers the ``en`` (CLDR) name then falls back to any known
    aliases.  Only names that have a matching file inside ``EMOJI_ASSET_DIR``
    are returned.

    Args:
        char: A single emoji character (may include variation selectors).

    Returns:
        The base filename (e.g. ``"fire"``) when a PNG asset exists, otherwise
        ``None``.
    """
    data = emoji.EMOJI_DATA.get(char, {})
    candidates: list[str] = []

    if "en" in data:
        candidates.append(data["en"].strip(":"))
    candidates.extend(alias.strip(":") for alias in data.get("alias", []))

    for name in candidates:
        if Path(EMOJI_ASSET_DIR, f"{name}.png").is_file():
            return name

    return None


def _split_on_emojis(text: str) -> list[tuple[str, bool]]:
    """Partition *text* into ``(segment, is_emoji)`` pairs.

    Consecutive non-emoji characters are grouped into a single segment so
    that the number of resulting pandoc nodes is minimised.

    Args:
        text: The plain-text content of a pandoc ``Str`` node.

    Returns:
        A list of ``(chars, is_emoji)`` tuples in order of appearance.
    """
    tokens = list(emoji.analyze(text, non_emoji=True))
    segments: list[tuple[str, bool]] = []
    buf: list[str] = []

    for tok in tokens:
        if isinstance(tok.value, EmojiMatch):
            if buf:
                segments.append(("".join(buf), False))
                buf = []
            segments.append((tok.chars, True))
        else:
            buf.append(tok.chars)

    if buf:
        segments.append(("".join(buf), False))

    return segments


def _emoji_image(char: str, name: str) -> dict:  # type: ignore[type-arg]
    """Build a pandoc ``Image`` inline node for *char*.

    The alt text uses the emoji name (e.g. ``"fire"``) rather than the raw
    emoji character to avoid triggering this filter again when pandocfilters
    recursively walks the returned node.

    Args:
        char: The raw emoji character (used for the image title).
        name: The PNG base-name from ``EMOJI_ASSET_DIR``.

    Returns:
        A pandoc ``Image`` node dictionary.
    """
    asset_path = str(Path(EMOJI_ASSET_DIR) / f"{name}.png")
    return Image(
        attributes({"class": "emoji", "alt": char}),
        [Str(name)],
        [asset_path, char],
    )


# ---------------------------------------------------------------------------
# Filter action
# ---------------------------------------------------------------------------


def emoji_filter(
    key: str,
    value: object,
    fmt: PandocFormat,  # noqa: ARG001
    meta: PandocMeta,  # noqa: ARG001
) -> list[dict] | None:  # type: ignore[type-arg]
    """Replace emoji characters inside ``Str`` nodes with inline images.

    For each ``Str`` node whose text contains one or more emoji characters
    that have a corresponding PNG asset, the node is replaced by a list of
    ``Str`` / ``Image`` nodes preserving the surrounding text.

    If no emoji with a matching asset is found the node is left unchanged
    (returns ``None``).

    Args:
        key: Pandoc element type (e.g. ``"Str"``).
        value: Element value; a plain string for ``Str`` nodes.
        fmt: Target output format supplied by pandoc.
        meta: Document metadata supplied by pandoc.

    Returns:
        A replacement list of inline nodes, or ``None`` to leave unchanged.
    """
    if key != "Str":
        return None

    text: str = value  # type: ignore[assignment]
    segments = _split_on_emojis(text)

    # Fast-path: no emoji characters at all.
    if len(segments) == 1 and not segments[0][1]:
        return None

    nodes: list[dict] = []  # type: ignore[type-arg]
    replaced = False

    for chars, is_emoji in segments:
        if is_emoji:
            asset_name = _asset_name_for(chars)
            if asset_name is not None:
                nodes.append(_emoji_image(chars, asset_name))
                replaced = True
            else:
                # No asset found - keep as plain text.
                nodes.append(Str(chars))
        else:
            nodes.append(Str(chars))

    return nodes if replaced else None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    toJSONFilter(emoji_filter)
