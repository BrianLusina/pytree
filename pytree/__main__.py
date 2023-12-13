"""
Entry point of the game
"""
import sys
from pathlib import Path
from pytree.cli import get_command_line_args
from pytree.entities import DirectoryTree


def main() -> None:
    """Entry point of the weather application. Gets the command line arguments"""
    args = get_command_line_args()
    root_dir = Path(args.directory)
    if not root_dir.is_dir():
        print("The specified root directory doesn't exist")
        sys.exit()
    tree = DirectoryTree(root_dir)
    tree.generate()


if __name__ == "__main__":
    main()
