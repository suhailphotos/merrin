#!/usr/bin/env python3
"""
find_exact_duplicates.py

Purpose
-------
Scan the staged photo and video library under SeagateSSD and generate a CSV of
confirmed exact-duplicate groups for human review.

This script is designed for the intermediate cleanup phase where files are
already separated into:

- /Volumes/SeagateSSD/Pictures/_unsorted
- /Volumes/SeagateSSD/Movies/_unsorted

What it does
------------
1. Recursively scans both _unsorted trees.
2. Groups files by file size.
3. Computes a partial hash for same-size groups only.
4. Computes a full SHA-256 hash for files that still match after partial hashing.
5. Writes a CSV listing confirmed exact-duplicate groups.
6. Writes a separate text log of missing or vanished paths encountered during the scan.

Why this workflow
-----------------
Hashing every file in a large archive is expensive. This script narrows the work
in stages:

- file size
- partial hash
- full hash

That makes it much faster while still confirming exact duplicates safely.

Output files
------------
The script writes two files to the Desktop by default:

- exact_duplicate_candidates_<timestamp>.csv
- exact_duplicate_missing_files_<timestamp>.txt

CSV columns
-----------
- group_id
- file_name
- full_path
- recommended_action
- approve
- file_size
- modified_time
- media_type
- sha256
- notes

Review workflow
---------------
- One file in each duplicate group is marked as "keep"
- All other files in that group are marked as "delete_candidate"
- Human reviewer fills the "approve" column
- A separate deletion script can later delete only approved rows

Notes
-----
- This finds exact duplicates only, not near-duplicates
- Missing files during the run are logged, not treated as fatal
- Output path is intentionally set to Desktop instead of the external drive root
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import csv
import hashlib
from collections import defaultdict


ROOT = Path("/Volumes/SeagateSSD")
SEARCH_ROOTS = [
    ROOT / "Pictures" / "_unsorted",
    ROOT / "Movies" / "_unsorted",
]

OUTPUT_DIR = Path.home() / "Desktop"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_CSV = OUTPUT_DIR / f"exact_duplicate_candidates_{STAMP}.csv"
MISSING_LOG = OUTPUT_DIR / f"exact_duplicate_missing_files_{STAMP}.txt"

image_exts = {
    ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".gif", ".bmp", ".webp", ".heic", ".heif",
    ".psd", ".psb",
    ".nef", ".nrw", ".cr2", ".cr3", ".crw", ".raf", ".arw", ".srf", ".sr2",
    ".orf", ".rw2", ".pef", ".dng", ".raw", ".3fr", ".fff", ".iiq", ".k25",
    ".kdc", ".mef", ".mos", ".mrw", ".ptx", ".r3d", ".srw", ".x3f", ".erf",
    ".xmp", ".aae", ".dop", ".pp3", ".cos", ".thm",
}

video_exts = {
    ".mp4", ".mov", ".m4v", ".avi", ".mkv", ".mts", ".m2ts", ".mpg", ".mpeg",
    ".wmv", ".flv", ".webm", ".3gp", ".3g2", ".mpv", ".mxf", ".lrv",
}

PARTIAL_CHUNK_SIZE = 1024 * 1024
FULL_HASH_CHUNK_SIZE = 8 * 1024 * 1024


def media_type_for_path(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in image_exts:
        return "picture"
    if ext in video_exts:
        return "movie"
    return "unknown"


def get_modified_time(path: Path) -> str:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")
    except Exception:
        return ""


def safe_exists(path: Path) -> bool:
    try:
        return path.exists() and path.is_file()
    except Exception:
        return False


def partial_hash(path: Path) -> str:
    """
    Compute a partial hash using:
    - file size
    - first chunk
    - last chunk

    This is used only to narrow candidate groups before full hashing.
    """
    h = hashlib.sha256()
    size = path.stat().st_size
    h.update(str(size).encode("utf-8"))

    with path.open("rb") as f:
        start = f.read(PARTIAL_CHUNK_SIZE)
        h.update(start)

        if size > PARTIAL_CHUNK_SIZE:
            f.seek(max(0, size - PARTIAL_CHUNK_SIZE))
            end = f.read(PARTIAL_CHUNK_SIZE)
            h.update(end)

    return h.hexdigest()


def full_hash(path: Path) -> str:
    """Compute full SHA-256 hash for a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(FULL_HASH_CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def recommended_keep_path(paths: list[Path]) -> Path:
    """
    Pick one file to keep using a deterministic rule:
    1. shorter full path
    2. alphabetical path
    """
    return sorted(paths, key=lambda p: (len(str(p)), str(p).lower()))[0]


def gather_all_files(search_roots: list[Path]) -> list[Path]:
    all_files: list[Path] = []
    for root in search_roots:
        if not root.exists():
            print(f"WARNING: missing search root: {root}")
            continue
        for p in root.rglob("*"):
            if p.is_file():
                all_files.append(p)
    return all_files


def main() -> None:
    missing_paths: list[str] = []

    all_files = gather_all_files(SEARCH_ROOTS)
    print(f"Scanned total files: {len(all_files)}")

    size_groups: dict[int, list[Path]] = defaultdict(list)
    for p in all_files:
        if not safe_exists(p):
            missing_paths.append(str(p))
            continue
        try:
            size_groups[p.stat().st_size].append(p)
        except Exception as e:
            print(f"SKIP unreadable file during size grouping: {p} :: {e}")

    candidate_size_groups = {size: paths for size, paths in size_groups.items() if len(paths) > 1}
    print(f"Same-size candidate groups: {len(candidate_size_groups)}")

    partial_groups: dict[tuple[int, str], list[Path]] = defaultdict(list)
    partial_hashed_files = 0

    for size, paths in candidate_size_groups.items():
        for p in paths:
            if not safe_exists(p):
                missing_paths.append(str(p))
                continue
            try:
                ph = partial_hash(p)
                partial_groups[(size, ph)].append(p)
                partial_hashed_files += 1
            except Exception as e:
                print(f"SKIP partial-hash failure: {p} :: {e}")

    candidate_partial_groups = {
        key: paths for key, paths in partial_groups.items() if len(paths) > 1
    }
    print(f"Partial-hash candidate groups: {len(candidate_partial_groups)}")
    print(f"Files partial-hashed: {partial_hashed_files}")

    full_groups: dict[str, list[Path]] = defaultdict(list)
    fully_hashed_files = 0

    for _, paths in candidate_partial_groups.items():
        for p in paths:
            if not safe_exists(p):
                missing_paths.append(str(p))
                continue
            try:
                fh = full_hash(p)
                full_groups[fh].append(p)
                fully_hashed_files += 1
            except Exception as e:
                print(f"SKIP full-hash failure: {p} :: {e}")

    duplicate_groups = {sha: paths for sha, paths in full_groups.items() if len(paths) > 1}
    print(f"Confirmed exact duplicate groups: {len(duplicate_groups)}")
    print(f"Files fully hashed: {fully_hashed_files}")

    rows_written = 0
    bytes_recoverable = 0
    group_index = 1

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "group_id",
            "file_name",
            "full_path",
            "recommended_action",
            "approve",
            "file_size",
            "modified_time",
            "media_type",
            "sha256",
            "notes",
        ])

        for sha, paths in sorted(duplicate_groups.items(), key=lambda item: (-len(item[1]), item[0])):
            live_paths = [p for p in paths if safe_exists(p)]
            if len(live_paths) < 2:
                continue

            keep_path = recommended_keep_path(live_paths)
            group_id = f"DUP-{group_index:05d}"
            group_index += 1

            try:
                file_size = keep_path.stat().st_size
                bytes_recoverable += (len(live_paths) - 1) * file_size
            except Exception:
                pass

            sorted_paths = sorted(
                live_paths,
                key=lambda x: (str(x).lower() != str(keep_path).lower(), str(x).lower()),
            )

            for p in sorted_paths:
                try:
                    size = p.stat().st_size
                except Exception:
                    size = ""

                writer.writerow([
                    group_id,
                    p.name,
                    str(p),
                    "keep" if p == keep_path else "delete_candidate",
                    "",
                    size,
                    get_modified_time(p),
                    media_type_for_path(p),
                    sha,
                    "",
                ])
                rows_written += 1

    with MISSING_LOG.open("w", encoding="utf-8") as f:
        for p in sorted(set(missing_paths)):
            f.write(p + "\n")

    print("\n=== SUMMARY ===")
    print(f"Output CSV: {OUTPUT_CSV}")
    print(f"Missing-file log: {MISSING_LOG}")
    print(f"Rows written: {rows_written}")
    print(f"Duplicate groups written: {group_index - 1}")
    print(f"Estimated recoverable bytes: {bytes_recoverable}")
    print(f"Missing/vanished paths logged: {len(set(missing_paths))}")


if __name__ == "__main__":
    main()
