#!/usr/bin/env python3
"""
File Organizer CLI — Automatically sort files into folders by type.

Usage:
    python organize.py ~/Downloads
    python organize.py ~/Downloads --dry-run
    python organize.py ~/Downloads --undo
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".odt", ".csv", ".rtf"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".m4v"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".go", ".rs", ".rb", ".php", ".sh", ".json", ".yaml", ".yml", ".xml", ".sql", ".md"},
    "Executables": {".exe", ".msi", ".dmg", ".app", ".deb", ".rpm", ".bin"},
    "Fonts": {".ttf", ".otf", ".woff", ".woff2", ".eot"},
    "Data": {".db", ".sqlite", ".sqlite3", ".parquet", ".feather", ".hdf5"},
}

LOG_FILE = ".file_organizer_log.json"


def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def organize(target_dir: Path, dry_run: bool = False) -> list[dict]:
    moves = []
    for item in target_dir.iterdir():
        if item.is_dir() or item.name.startswith("."):
            continue

        category = get_category(item.suffix)
        dest_dir = target_dir / category
        dest_file = dest_dir / item.name

        # Handle name conflicts
        if dest_file.exists():
            stem = item.stem
            suffix = item.suffix
            counter = 1
            while dest_file.exists():
                dest_file = dest_dir / f"{stem}_{counter}{suffix}"
                counter += 1

        move = {"src": str(item), "dest": str(dest_file)}
        moves.append(move)

        if not dry_run:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_file))

    return moves


def undo(target_dir: Path) -> None:
    log_path = target_dir / LOG_FILE
    if not log_path.exists():
        print("No log file found. Nothing to undo.")
        sys.exit(1)

    with open(log_path) as f:
        moves = json.load(f)

    restored = 0
    for move in reversed(moves):
        src, dest = Path(move["src"]), Path(move["dest"])
        if dest.exists():
            shutil.move(str(dest), str(src))
            restored += 1

    # Clean up empty category folders
    for category in list(CATEGORIES.keys()) + ["Other"]:
        cat_dir = target_dir / category
        if cat_dir.is_dir() and not any(cat_dir.iterdir()):
            cat_dir.rmdir()

    log_path.unlink()
    print(f"Restored {restored} file(s).")


def main():
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by type."
    )
    parser.add_argument("directory", help="Target directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    parser.add_argument("--undo", action="store_true", help="Undo the last organize operation")
    args = parser.parse_args()

    target = Path(args.directory).expanduser().resolve()
    if not target.is_dir():
        print(f"Error: '{target}' is not a valid directory.")
        sys.exit(1)

    if args.undo:
        undo(target)
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
        log_path = target / LOG_FILE
        with open(log_path, "w") as f:
            json.dump(moves, f, indent=2)
        print(f"Undo log saved. Run with --undo to revert.")


if __name__ == "__main__":
    main()
