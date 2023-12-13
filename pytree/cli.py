"""
Defines the CLI command arguments
"""
import argparse
from argparse import Namespace


def get_command_line_args() -> Namespace:
    """
    Creates a parser and adds arguments for the parser returning the namespace for the argument parser to use in a CLI
    Returns:
        Namespace: populated namespace object
    """
    parser = argparse.ArgumentParser(
        prog="pytree",
        description="Gets weather and temperature information for a city",
        epilog="Thank you for using PyTree CLI"
    )

    # TODO: parse version from git tag information
    parser.version = f"PyTree v0.0.0"

    # Argument to get the version name
    parser.add_argument(
        "-v",
        "--version",
        action="version",
    )

    # Argument to get the directory name
    parser.add_argument(
        "-d",
        "--directory",
        nargs="?",
        metavar="ROOT_DIR",
        type=str,
        default=".",
        help="Generate full directory tree starting at ROOT_DIR",
    )

    return parser.parse_args()
