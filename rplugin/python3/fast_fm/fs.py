from __future__ import annotations

from os import makedirs
from os import remove as rm
from os.path import dirname, isdir, sep
from pathlib import Path
from shutil import copy2, copytree
from shutil import move as mv
from shutil import rmtree
from typing import Iterator, Set

from .consts import file_mode, folder_mode


def is_parent(*, parent: str, child: str) -> bool:
    return child.startswith(parent)


def ancestors(path: str) -> Iterator[str]:
    if not path or path == sep:
        return
    else:
        parent = dirname(path)
        yield from ancestors(parent)
        yield parent


def unify(paths: Set[str]) -> Iterator[str]:
    for path in paths:
        if not any(a in paths for a in ancestors(path)):
            yield path


def new(dest: str) -> None:
    if dest.endswith(sep):
        makedirs(dest, mode=folder_mode, exist_ok=True)
    else:
        parent = dirname(dest)
        makedirs(parent, mode=folder_mode, exist_ok=True)
        Path(dest).touch(mode=file_mode, exist_ok=True)


def rename(src: str, dest: str) -> None:
    parent = dirname(dest)
    makedirs(parent, mode=folder_mode, exist_ok=True)
    mv(src, dest)


def remove(src: str) -> None:
    if isdir(src):
        rmtree(src)
    else:
        rm(src)


def cut(src: str, dest: str) -> None:
    mv(src, dest)


def copy(src: str, dest: str) -> None:
    if isdir(src):
        copytree(src, dest)
    else:
        copy2(src, dest)
