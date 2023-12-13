"""
Contains structured models wrapping functionality around data obtained from listing files in a directory
"""
import os
from typing import List
from pathlib import Path
from pytree.constants import PIPE, ELBOW, TEE, PIPE_PREFIX, SPACE_PREFIX


class DirectoryTree:
    """
    DirectoryTree represents a Directory tree structure. This will be used to generate the directory diagram
    """

    def __init__(self, root_dir: Path, dir_only: bool = False):
        self._generator = _TreeGenerator(root_dir, dir_only)

    def generate(self):
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)


class _TreeGenerator:
    """
    Low-level nonpublic tree generator class that parses the directory root provided and returns a tree
    """

    def __init__(self, root_dir: Path, dir_only: bool = False):
        self._root_dir = root_dir
        self._dir_only = dir_only
        self._tree: List[str] = []

    def build_tree(self) -> List[str]:
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self) -> None:
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory: Path, prefix="") -> None:
        entries = self._prepare_entries(directory)
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)

    def _add_directory(self, directory: Path, index: int, entries_count: int, prefix: str, connector: str) -> None:
        """
        Adds a directory to be parsed in the tree body to be displayed
        Args:
            directory (Path): Directory to parse
            index (int): Current index in the list
            entries_count (int): Number of entries in the path
            prefix (str): The current prefix
            connector (str): connector being used to build up the tree
        """
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file: Path, prefix: str, connector) -> None:
        """
        Adds a file to the tree being build
        Args:
            file (Path): name of the file
            prefix (str): Prefix to use for displaying the file
            connector (str): Connector to use for displaying the file
        """
        self._tree.append(f"{prefix}{connector} {file.name}")

    def _prepare_entries(self, directory: Path):
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries
        entries = sorted(entries, key=lambda e: e.is_file())
        return entries
