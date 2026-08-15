#!/usr/bin/env python3
"""Interactive Python startup configuration.

Set ``PYTHONSTARTUP`` to this file to get readline completion, persistent
history, friendlier tracebacks, and a small set of commonly used helpers in
interactive sessions.
"""

from __future__ import annotations

import atexit
import builtins
import code
import datetime as dt
import importlib
import inspect
import json
import os
import pprint
import site
import sys
import textwrap
import types
import warnings
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, field, fields, is_dataclass
from decimal import Decimal
from enum import Enum
from functools import cache, cached_property, lru_cache, partial, reduce
from itertools import chain, combinations, count, cycle, groupby, islice, pairwise
from pathlib import Path
from types import ModuleType
from typing import Any, Final, Protocol, TypeAlias, TypeVar, cast

try:
    import readline
except ImportError:  # pragma: no cover - platform dependent
    readline = None  # type: ignore[assignment]

try:
    import rlcompleter
except ImportError:  # pragma: no cover - platform dependent
    rlcompleter = None  # type: ignore[assignment]

T = TypeVar("T")
JsonValue: TypeAlias = (
    None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
)

HISTORY_LIMIT: Final[int] = 50_000
INDENT: Final[str] = "    "


class SupportsPretty(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for objects with rich pretty-print methods."""

    def __rich_repr__(self) -> Iterable[object]:
        """Return Rich-compatible representation parts."""
        ...


def _xdg_path(env_name: str, default_suffix: str) -> Path:
    """Resolve an XDG directory with a home-relative fallback."""
    configured = os.environ.get(env_name)
    if configured:
        return Path(configured).expanduser()
    return Path.home() / default_suffix


XDG_STATE_HOME: Final[Path] = _xdg_path("XDG_STATE_HOME", ".local/state")
XDG_CACHE_HOME: Final[Path] = _xdg_path("XDG_CACHE_HOME", ".cache")
PYTHON_STATE_DIR: Final[Path] = XDG_STATE_HOME / "python"
PYTHON_CACHE_DIR: Final[Path] = XDG_CACHE_HOME / "python"
HISTORY_FILE: Final[Path] = PYTHON_STATE_DIR / "history"


def _silence_startup_error(action: Callable[[], T], default: T) -> T:
    """Run optional startup setup without breaking interpreter launch."""
    try:
        return action()
    except (OSError, RuntimeError, ValueError):
        return default


class IndentableCompleter:  # pylint: disable=too-few-public-methods
    """Readline completer that inserts spaces on an empty completion line."""

    def __init__(self, namespace: Mapping[str, object] | None = None) -> None:
        self._delegate: Any | None = None
        if rlcompleter is None:
            return
        self._delegate = rlcompleter.Completer(dict(namespace or {}))

    def complete(self, text: str, state: int) -> str | None:
        """Return a completion candidate for readline."""
        if not text.strip():
            return INDENT if state == 0 else None
        if self._delegate is None:
            return None
        return cast("str | None", self._delegate.complete(text, state))


def _configure_directories() -> None:
    """Create state/cache directories used by this startup file."""
    _silence_startup_error(
        lambda: PYTHON_STATE_DIR.mkdir(parents=True, exist_ok=True), None
    )
    _silence_startup_error(
        lambda: PYTHON_CACHE_DIR.mkdir(parents=True, exist_ok=True), None
    )


def _configure_history() -> None:
    """Configure readline history when readline is available."""
    if readline is None:
        return

    _readline = readline

    _readline.set_history_length(HISTORY_LIMIT)

    if HISTORY_FILE.exists():
        _silence_startup_error(
            lambda: _readline.read_history_file(str(HISTORY_FILE)),
            None,
        )

    def save_history() -> None:
        _silence_startup_error(
            lambda: _readline.write_history_file(str(HISTORY_FILE)),
            None,
        )

    atexit.register(save_history)


def _configure_completion() -> None:
    """Configure tab completion when readline is available."""
    if readline is None:
        return

    readline.set_completer(IndentableCompleter(vars(builtins)).complete)

    readline_doc = getattr(readline, "__doc__", "") or ""
    if "libedit" in readline_doc.lower():
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")


def _configure_displayhook() -> None:
    """Pretty-print expression results while preserving ``builtins._``."""
    original_displayhook = sys.displayhook

    def displayhook(value: object) -> None:
        if value is None:
            return
        setattr(builtins, "_", None)
        pprint.pp(value, sort_dicts=False)
        setattr(builtins, "_", value)

    if getattr(sys, "ps1", None) is None:
        sys.displayhook = original_displayhook
    else:
        sys.displayhook = displayhook


def _configure_tracebacks() -> None:
    """Install the best available traceback renderer."""
    try:
        rich_traceback = importlib.import_module("rich.traceback")
    except ImportError:
        try:
            better_exceptions = importlib.import_module("better_exceptions")
        except ImportError:
            sys.excepthook = sys.__excepthook__
        else:
            setattr(better_exceptions, "MAX_LENGTH", 8_000)
    else:
        install_traceback = getattr(rich_traceback, "install")
        install_traceback(
            show_locals=True,
            suppress=[site, inspect],
            width=120,
        )


def _configure_warnings() -> None:
    """Use visible but non-spammy warning defaults for interactive work."""
    warnings.simplefilter("default")
    warnings.filterwarnings("once", category=DeprecationWarning)
    warnings.filterwarnings("once", category=PendingDeprecationWarning)


def pp(value: object, *, width: int = 100, compact: bool = False) -> object:
    """Pretty-print ``value`` and return it for REPL chaining."""
    pprint.pp(value, width=width, compact=compact, sort_dicts=False)
    return value


def pformat(value: object, *, width: int = 100, compact: bool = False) -> str:
    """Return a pretty formatted representation of ``value``."""
    return pprint.pformat(value, width=width, compact=compact, sort_dicts=False)


def pj(value: object, *, indent: int = 2, sort_keys: bool = True) -> object:
    """Print ``value`` as JSON and return it."""
    print(json.dumps(value, indent=indent, sort_keys=sort_keys, default=str))
    return value


def slurp(path: str | os.PathLike[str], *, encoding: str = "utf-8") -> str:
    """Read a text file."""
    return Path(path).expanduser().read_text(encoding=encoding)


def spit(
    path: str | os.PathLike[str],
    content: str,
    *,
    encoding: str = "utf-8",
    append: bool = False,
) -> Path:
    """Write text to a file and return the resolved path."""
    resolved = Path(path).expanduser()
    resolved.parent.mkdir(parents=True, exist_ok=True)
    if append:
        with resolved.open("a", encoding=encoding) as handle:
            handle.write(content)
    else:
        resolved.write_text(content, encoding=encoding)
    return resolved


def jload(path: str | os.PathLike[str], *, encoding: str = "utf-8") -> JsonValue:
    """Load JSON from a file."""
    with Path(path).expanduser().open(encoding=encoding) as handle:
        return cast("JsonValue", json.load(handle))


def jdump(
    value: object,
    path: str | os.PathLike[str],
    *,
    encoding: str = "utf-8",
    indent: int = 2,
    sort_keys: bool = True,
) -> Path:
    """Write JSON to a file and return the path."""
    resolved = Path(path).expanduser()
    resolved.parent.mkdir(parents=True, exist_ok=True)
    with resolved.open("w", encoding=encoding) as handle:
        json.dump(value, handle, indent=indent, sort_keys=sort_keys, default=str)
        handle.write("\n")
    return resolved


def first(items: Iterable[T], default: T | None = None) -> T | None:
    """Return the first item from an iterable, or ``default``."""
    return next(iter(items), default)


def take(count_: int, items: Iterable[T]) -> list[T]:
    """Return the first ``count_`` items from an iterable."""
    return list(islice(items, count_))


def chunks(items: Sequence[T], size: int) -> list[Sequence[T]]:
    """Split a sequence into fixed-size chunks."""
    if size <= 0:
        raise ValueError("chunk size must be positive")
    return [items[index : index + size] for index in range(0, len(items), size)]


def flatten(items: Iterable[Iterable[T]]) -> list[T]:
    """Flatten one nesting level."""
    return list(chain.from_iterable(items))


def uniq(items: Iterable[T]) -> list[T]:
    """Return unique items while preserving insertion order."""
    return list(dict.fromkeys(items))


def attrs(value: object) -> list[str]:
    """Return public attributes for quick discovery."""
    return [name for name in dir(value) if not name.startswith("_")]


def members(value: object) -> dict[str, object]:
    """Return public non-method attributes for quick inspection."""
    return {
        name: member
        for name, member in inspect.getmembers(value)
        if not name.startswith("_") and not inspect.ismethod(member)
    }


def source(value: object) -> str:
    """Return source code for an object when available."""
    return inspect.getsource(cast("Any", value))


def doc(value: object) -> str:
    """Return a cleaned docstring for an object."""
    return inspect.getdoc(value) or ""


def typeinfo(value: object) -> dict[str, object]:
    """Return compact type and module information for an object."""
    value_type = type(value)
    return {
        "type": value_type.__qualname__,
        "module": value_type.__module__,
        "repr": repr(value),
        "size": sys.getsizeof(value),
    }


def dataclass_dict(value: object) -> dict[str, object]:
    """Convert a dataclass instance to a dictionary."""
    if not is_dataclass(value) or isinstance(value, type):
        raise TypeError("value must be a dataclass instance")
    return cast("dict[str, object]", asdict(value))


def dataclass_fields(value: object) -> tuple[str, ...]:
    """Return dataclass field names."""
    if not is_dataclass(value):
        raise TypeError("value must be a dataclass or dataclass instance")
    return tuple(field_.name for field_ in fields(value))


def modules(prefix: str | None = None) -> list[str]:
    """Return currently imported module names, optionally filtered by prefix."""
    names = sorted(
        name for name in sys.modules if prefix is None or name.startswith(prefix)
    )
    return names


def reload_module(module: ModuleType) -> ModuleType:
    """Reload an imported module."""
    return importlib.reload(module)


def banner() -> None:
    """Print a compact summary of available startup helpers."""
    helper_names = [
        "Path",
        "dt",
        "pp",
        "pj",
        "slurp",
        "spit",
        "jload",
        "jdump",
        "first",
        "take",
        "chunks",
        "flatten",
        "uniq",
        "attrs",
        "members",
        "source",
        "doc",
        "typeinfo",
        "modules",
        "reload_module",
    ]
    print("Python startup helpers:")
    print(textwrap.fill(", ".join(helper_names), width=100, subsequent_indent="  "))


def _install_helpers() -> None:
    """Expose curated helpers in builtins for interactive convenience."""
    helpers: dict[str, object] = {
        "Any": Any,
        "Callable": Callable,
        "Counter": Counter,
        "Decimal": Decimal,
        "Enum": Enum,
        "Final": Final,
        "JsonValue": JsonValue,
        "Mapping": Mapping,
        "Path": Path,
        "Protocol": Protocol,
        "Sequence": Sequence,
        "SupportsPretty": SupportsPretty,
        "TypeAlias": TypeAlias,
        "TypeVar": TypeVar,
        "asdict": asdict,
        "attrs": attrs,
        "banner": banner,
        "cache": cache,
        "cached_property": cached_property,
        "chain": chain,
        "chunks": chunks,
        "code": code,
        "combinations": combinations,
        "count": count,
        "cycle": cycle,
        "dataclass": dataclass,
        "dataclass_dict": dataclass_dict,
        "dataclass_fields": dataclass_fields,
        "defaultdict": defaultdict,
        "deque": deque,
        "doc": doc,
        "dt": dt,
        "field": field,
        "fields": fields,
        "first": first,
        "flatten": flatten,
        "groupby": groupby,
        "inspect": inspect,
        "importlib": importlib,
        "is_dataclass": is_dataclass,
        "islice": islice,
        "jdump": jdump,
        "jload": jload,
        "json": json,
        "lru_cache": lru_cache,
        "members": members,
        "modules": modules,
        "os": os,
        "pairwise": pairwise,
        "partial": partial,
        "pformat": pformat,
        "pj": pj,
        "pp": pp,
        "pprint": pprint,
        "reduce": reduce,
        "reload_module": reload_module,
        "slurp": slurp,
        "source": source,
        "spit": spit,
        "sys": sys,
        "take": take,
        "textwrap": textwrap,
        "typeinfo": typeinfo,
        "types": types,
        "uniq": uniq,
    }

    for name, value in helpers.items():
        setattr(builtins, name, value)


def _main() -> None:
    """Configure the interactive interpreter."""
    _configure_directories()
    _configure_history()
    _configure_completion()
    _configure_displayhook()
    _configure_tracebacks()
    _configure_warnings()
    _install_helpers()


_main()
