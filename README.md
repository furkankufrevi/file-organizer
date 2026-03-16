# File Organizer CLI

A simple, zero-dependency Python CLI that organizes messy folders by sorting files into categorized subfolders.

## Installation

```bash
pip install messy2tidy
```

## Usage

```bash
# Organize your Downloads folder
fileorganizer ~/Downloads

# Preview changes without moving anything
fileorganizer ~/Downloads --dry-run

# Undo the last operation
fileorganizer ~/Downloads --undo

# Check version
fileorganizer --version
```

## Example Output

```
  Moved: report.pdf -> Documents/
  Moved: photo.jpg -> Images/
  Moved: song.mp3 -> Audio/
  Moved: archive.zip -> Archives/

Moved 4 file(s).
Undo log saved. Run with --undo to revert.
```

## Features

- Sorts files into folders: Images, Documents, Videos, Audio, Archives, Code, Executables, Fonts, Data, Other
- **Dry-run mode** — preview what will happen before moving anything
- **Undo** — revert the last organize operation with a single command
- Handles filename conflicts automatically
- Skips hidden files and subdirectories
- No external dependencies — pure Python 3.10+

## Supported Categories

| Category    | Extensions                                              |
|-------------|---------------------------------------------------------|
| Images      | jpg, jpeg, png, gif, bmp, svg, webp, ico, tiff, heic   |
| Documents   | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, odt, csv, rtf |
| Videos      | mp4, mov, avi, mkv, flv, wmv, webm, m4v                |
| Audio       | mp3, wav, flac, aac, ogg, wma, m4a                     |
| Archives    | zip, tar, gz, rar, 7z, bz2, xz                         |
| Code        | py, js, ts, html, css, java, c, cpp, go, rs, rb, php, sh, json, yaml, yml, xml, sql, md |
| Executables | exe, msi, dmg, app, deb, rpm, bin                       |
| Fonts       | ttf, otf, woff, woff2, eot                              |
| Data        | db, sqlite, sqlite3, parquet, feather, hdf5              |
| Other       | Everything else                                          |

## License

MIT
