
from typing import Optional, Dict, Set, List

import os
from pathlib import Path
import shutil

from .types.aliases import T

from .utils.files import mkdir, read_text
from .utils.strings import get_string_vars, fix_string_name, add_numbers_to_sorted


def order_keys(depends_dict: Dict[T, Set[T]]) -> List[T]:
    """
    orders { key -> keys it depends on} so that no keys will be after the key it depends on

    >>> order_keys({1: {2, 3}, 2: set(), 3: set()})
    [2, 3, 1]
    >>> order_keys({1: {2, 3}, 2: {3}, 3: set()})
    [3, 2, 1]
    >>> order_keys({1: {3, 4}, 2: set(), 3: {2}, 4: set()})
    [2, 4, 3, 1]
    """

    dct = depends_dict
    res = []

    while True:
        no_deps_keys = {k for k, v in dct.items() if not v}
        assert no_deps_keys, f"all keys are dependent between one another! {dct}, {depends_dict}"
        res.extend(sorted(no_deps_keys))
        dct = {k: v - no_deps_keys for k, v in dct.items() if k not in no_deps_keys}
        if not dct:
            return res


def order_graphs(directory: str, to_directory: Optional[str] = None):
    """orders graphs in directory depends on their deps between one other"""

    all_files = list(Path(directory).glob('*.yaml'))

    assert all_files, f"{directory} has not yamls"

    file2name = {
        str(f): fix_string_name(f.stem) for f in all_files
    }
    name2file = {v: k for k, v in file2name.items()}
    file2deps: Dict[str, Set[str]] = {
        str(f): set(
            get_string_vars(read_text(f)).values()
        )
        for f in all_files
    }

    all_names = set(file2name.values())
    for f, deps in file2deps.items():
        diff = deps - all_names
        if diff:
            raise ValueError(
                f"file {f} contains unknown variables {diff}"
            )

    # order names according to deps
    ordered_names = order_keys(
        {
            file2name[f]: file2deps[f]
            for f in file2name.keys()
        }
    )

    ordered_files = [name2file[n] for n in ordered_names]
    new_file_names = add_numbers_to_sorted(
        [Path(f).name for f in ordered_files]
    )

    if to_directory:
        mkdir(to_directory)
        move = shutil.copy
    else:
        to_directory = directory
        move = shutil.move
    for file, new_name in zip(ordered_files, new_file_names):
        move(file, os.path.join(to_directory, new_name))





