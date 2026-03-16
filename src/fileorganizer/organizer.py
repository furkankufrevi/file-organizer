"""Core file organizing logic."""

import json
import shutil
from pathlib import Path

CATEGORIES = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
        ".webp", ".ico", ".tiff", ".heic",
    },
    "Documents": {
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt",
        ".pptx", ".txt", ".odt", ".csv", ".rtf",
    },
    "Videos": {
        ".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".m4v",
    },
    "Audio": {
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
    },
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz"},
    "Code": {
        ".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp",
        ".go", ".rs", ".rb", ".php", ".sh", ".json", ".yaml", ".yml",
        ".xml", ".sql", ".md",
    },
    "Executables": {".exe", ".msi", ".dmg", ".app", ".deb", ".rpm", ".bin"},
    "Fonts": {".ttf", ".otf", ".woff", ".woff2", ".eot"},
    "Data": {".db", ".sqlite", ".sqlite3", ".parquet", ".feather", ".hdf5"},
}

LOG_FILE = ".file_organizer_log.json"


def get_category(ext: str) -> str:
    """Return the category name for a given file extension."""
    ext = ext.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def organize(target_dir: Path, dry_run: bool = False) -> list[dict]:
    """Organize files in target_dir into category subfolders."""
    moves = []
    for item in target_dir.iterdir():
        if item.is_dir() or item.name.startswith("."):
            continue

        category = get_category(item.suffix)
        dest_dir = target_dir / category
        dest_file = dest_dir / item.name

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


def undo(target_dir: Path) -> int:
    """Undo the last organize operation. Returns number of restored files."""
    log_path = target_dir / LOG_FILE
    if not log_path.exists():
        return -1

    with open(log_path, encoding="utf-8") as f:
        moves = json.load(f)

    restored = 0
    for move in reversed(moves):
        src, dest = Path(move["src"]), Path(move["dest"])
        if dest.exists():
            shutil.move(str(dest), str(src))
            restored += 1

    for category in list(CATEGORIES.keys()) + ["Other"]:
        cat_dir = target_dir / category
        if cat_dir.is_dir() and not any(cat_dir.iterdir()):
            cat_dir.rmdir()

    log_path.unlink()
    return restored


def save_log(target_dir: Path, moves: list[dict]) -> None:
    """Save the move log for undo support."""
    log_path = target_dir / LOG_FILE
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(moves, f, indent=2)
