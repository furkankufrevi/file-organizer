"""CLI entry point for fileorganizer."""

import argparse
import sys
from pathlib import Path

from . import __version__
from .organizer import organize, save_log, undo


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="fileorganizer",
        description="Organize files in a directory by type.",
    )
    parser.add_argument("directory", help="Target directory to organize")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview changes without moving files",
    )
    parser.add_argument(
        "--undo", action="store_true",
        help="Undo the last organize operation",
    )
    parser.add_argument(
        "--version", action="version",
        version=f"%(prog)s {__version__}",
    )
    args = parser.parse_args()

    target = Path(args.directory).expanduser().resolve()
    if not target.is_dir():
        print(f"Error: '{target}' is not a valid directory.")
        sys.exit(1)

    if args.undo:
        restored = undo(target)
        if restored == -1:
            print("No log file found. Nothing to undo.")
            sys.exit(1)
        print(f"Restored {restored} file(s).")
        return

    moves = organize(target, dry_run=args.dry_run)

    if not moves:
        print("No files to organize.")
        return

    label = "Would move" if args.dry_run else "Moved"
    for move in moves:
        src_name = Path(move["src"]).name
        dest_folder = Path(move["dest"]).parent.name
        print(f"  {label}: {src_name} -> {dest_folder}/")

    print(f"\n{label} {len(moves)} file(s).")

    if not args.dry_run:
        save_log(target, moves)
        print("Undo log saved. Run with --undo to revert.")


if __name__ == "__main__":
    main()
