"""
Contains structured models wrapping functionality around data obtained from listing files in a directory
"""
import os
from typing import List
import pathlib
from pytree.constants import PIPE, ELBOW, TEE


class DirectoryTree:
    """
    DirectoryTree represents a Directory tree structure. This will be used to generate the directory diagram
    """

    def __init__(self, root_dir: str):
        self._generator = _TreeGenerator(root_dir)

    def generate(self):
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)


class _TreeGenerator:
    """
    Low-level nonpublic tree generator class that parses the directory root provided and returns a tree
    """

    def __init__(self, root_dir: str):
        self._root_dir = pathlib.Path(root_dir)
        self._tree = []

    def build_tree(self) -> List:
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=""):
        entries = directory.iterdir()
        entries = sorted(entries, key=lambda e: e.is_file())
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)
