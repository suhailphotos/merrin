#!/usr/bin/env python3
"""
organize_media.py

Purpose
-------
Organize a media library into two top-level branches:

- Pictures/_unsorted
- Movies/_unsorted

This script is intended for staged cleanup before metadata extraction and
Lightroom import. It preserves breadcrumb paths so the original folder structure
can still be inferred later.

What this script supports
-------------------------
This is a generalized replacement for earlier one-off scripts. It supports:

1. copy mode
   - copy files from a source tree into a destination tree
   - useful when importing from another drive without changing the source

2. move mode
   - move files or folders in place
   - useful when reorganizing an existing staging drive

3. file-level classification
   - classify each file by extension
   - image-family files go to Pictures/_unsorted
   - video files go to Movies/_unsorted

4. folder-level reclassification
   - intended for a Mixed/_unsorted tree
   - finds topmost pure subfolders and moves them out
   - leaves truly mixed folders in place

Recommended usage patterns
--------------------------
A. Copy from one drive into a staging tree:
   MODE = "copy"
   CLASSIFY_LEVEL = "file"

B. Empty a Mixed/_unsorted tree completely:
   MODE = "move"
   CLASSIFY_LEVEL = "file"

C. First pass on a Mixed/_unsorted tree:
   MODE = "move"
   CLASSIFY_LEVEL = "folder"

Key knobs
---------
- MODE:
    "copy" or "move"
- CLASSIFY_LEVEL:
    "file" or "folder"
- SOURCE_ROOT:
    where files are read from
- DEST_ROOT:
    destination root that contains Pictures/_unsorted and Movies/_unsorted
- SOURCE_SUBTREE:
    optional subtree under SOURCE_ROOT to operate on
    example: Path("Mixed/_unsorted")
- DRY_RUN:
    True for preview only
    False to actually perform copy/move operations
- DELETE_EMPTY_DIRS_AFTER_MOVE:
    remove empty directories after file-level move operations

Breadcrumb behavior
-------------------
Breadcrumbs are preserved relative to the chosen working root.

Examples:
- In copy/file mode:
    SOURCE_ROOT=/source_drive
    file=/source_drive/2019/AVERY/CLIP/C0001.MP4
    -> /dest_root/Movies/_unsorted/2019/AVERY/CLIP/C0001.MP4

- In move/file mode with SOURCE_SUBTREE=Mixed/_unsorted:
    /dest_root/Mixed/_unsorted/2019/AVERY/ENG05445.jpg
    -> /dest_root/Pictures/_unsorted/2019/AVERY/ENG05445.jpg

Notes
-----
- This script never deletes files.
- Conflicts are skipped, not overwritten.
- Same-size existing files can optionally be treated as already handled.
- Sidecars like .xmp are treated as picture-family files.
- This script is configured by editing values near the top.
  Later these can become CLI flags.
"""

from __future__ import annotations

from pathlib import Path
import shutil


# ============================================================================
# CONFIGURATION
# ============================================================================

# "copy" or "move"
MODE = "copy"

# "file" or "folder"
CLASSIFY_LEVEL = "file"

# Root to read from.
SOURCE_ROOT = Path("/Volumes/Seagate Backup Plus Drive")

# Root that contains / will contain Pictures/_unsorted and Movies/_unsorted.
DEST_ROOT = Path("/Volumes/SeagateSSD")

# Optional subtree under SOURCE_ROOT to operate on.
# Examples:
#   None
#   Path("Mixed/_unsorted")
SOURCE_SUBTREE: Path | None = None

# Dry run first. Set to False to perform changes.
DRY_RUN = True

# Only relevant in move + file mode. Removes empty dirs after moving files.
DELETE_EMPTY_DIRS_AFTER_MOVE = True

# Treat an existing destination file with the same size as already handled.
SKIP_EXISTING_SAME_SIZE = True

# Directory names to ignore anywhere in the scanned path.
SKIP_DIR_NAMES = {"$RECYCLE.BIN", ".Trashes", ".Spotlight-V100"}

# Buffer size for plain streamed copy.
COPY_BUFFER_SIZE = 8 * 1024 * 1024


# ============================================================================
# EXTENSIONS
# ============================================================================

IMAGE_EXTS = {
    ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".gif", ".bmp", ".webp", ".heic", ".heif",
    ".psd", ".psb",
    ".nef", ".nrw", ".cr2", ".cr3", ".crw", ".raf", ".arw", ".srf", ".sr2",
    ".orf", ".rw2", ".pef", ".dng", ".raw", ".3fr", ".fff", ".iiq", ".k25",
    ".kdc", ".mef", ".mos", ".mrw", ".ptx", ".r3d", ".srw", ".x3f", ".erf",
    ".xmp", ".aae", ".dop", ".pp3", ".cos", ".thm",
}

VIDEO_EXTS = {
    ".mp4", ".mov", ".m4v", ".avi", ".mkv", ".mts", ".m2ts", ".mpg", ".mpeg",
    ".wmv", ".flv", ".webm", ".3gp", ".3g2", ".mpv", ".mxf", ".lrv",
}


# ============================================================================
# PATH SETUP
# ============================================================================

PICTURES_ROOT = DEST_ROOT / "Pictures" / "_unsorted"
MOVIES_ROOT = DEST_ROOT / "Movies" / "_unsorted"


def working_source_root() -> Path:
    """Return the effective source root after applying SOURCE_SUBTREE if present."""
    return SOURCE_ROOT / SOURCE_SUBTREE if SOURCE_SUBTREE is not None else SOURCE_ROOT


# ============================================================================
# HELPERS
# ============================================================================

def should_skip(path: Path) -> bool:
    """Return True if any path component is in the skip list."""
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def classify_file(path: Path) -> str | None:
    """
    Classify a single file.

    Returns:
        "pictures" for image-family files
        "movies" for video files
        None for unknown files
    """
    ext = path.suffix.lower()
    if ext in IMAGE_EXTS:
        return "pictures"
    if ext in VIDEO_EXTS:
        return "movies"
    return None


def classify_tree(folder: Path) -> str | None:
    """
    Classify an entire folder tree.

    Returns:
        "pictures" if only picture-family files are found
        "movies" if only video files are found
        "mixed" if both are found
        None if no recognized media are found
    """
    has_images = False
    has_videos = False

    for p in folder.rglob("*"):
        if not p.is_file():
            continue
        if should_skip(p):
            continue

        kind = classify_file(p)
        if kind == "pictures":
            has_images = True
        elif kind == "movies":
            has_videos = True

        if has_images and has_videos:
            return "mixed"

    if has_images:
        return "pictures"
    if has_videos:
        return "movies"
    return None


def topmost_reclassifiable_dirs(root: Path) -> list[tuple[Path, str]]:
    """
    Find topmost subfolders that can be cleanly reclassified.

    Used for folder-level mode. If a folder is mixed, recurse into it.
    If a folder is pure pictures or pure movies, include that folder and stop
    descending further below it.
    """
    candidates: list[tuple[Path, str]] = []

    def walk(folder: Path) -> None:
        for child in folder.iterdir():
            if not child.is_dir():
                continue
            if should_skip(child):
                continue

            kind = classify_tree(child)
            if kind is None:
                continue

            if kind == "mixed":
                walk(child)
            else:
                candidates.append((child, kind))

    walk(root)
    return candidates


def ensure_dest_roots() -> None:
    """Create destination branches if needed."""
    PICTURES_ROOT.mkdir(parents=True, exist_ok=True)
    MOVIES_ROOT.mkdir(parents=True, exist_ok=True)


def simple_copy(src: Path, dst: Path, buffer_size: int = COPY_BUFFER_SIZE) -> None:
    """Copy file contents without attempting to preserve metadata."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    with src.open("rb") as fsrc, dst.open("wb") as fdst:
        shutil.copyfileobj(fsrc, fdst, length=buffer_size)


def safe_same_size(src: Path, dst: Path) -> bool:
    """Return True if src and dst both exist and have the same size."""
    try:
        return src.stat().st_size == dst.stat().st_size
    except Exception:
        return False


def destination_for_file(src_file: Path, base_root: Path) -> tuple[Path, str] | None:
    """
    Return destination path and kind for a recognized file.

    base_root is the root relative to which breadcrumb paths are preserved.
    """
    kind = classify_file(src_file)
    if kind is None:
        return None

    rel = src_file.relative_to(base_root)
    if kind == "pictures":
        return PICTURES_ROOT / rel, kind
    return MOVIES_ROOT / rel, kind


def remove_empty_dirs(root: Path) -> int:
    """Remove empty directories under root, deepest first."""
    deleted = 0
    for d in sorted((p for p in root.rglob("*") if p.is_dir()), key=lambda x: len(x.parts), reverse=True):
        try:
            next(d.iterdir())
        except StopIteration:
            try:
                d.rmdir()
                deleted += 1
            except Exception:
                pass
        except Exception:
            pass
    return deleted


# ============================================================================
# OPERATIONS
# ============================================================================

def run_file_level() -> None:
    """
    File-level organization.

    Works for:
    - copy from one tree to another
    - move from Mixed/_unsorted into Pictures/Movies
    - move any source tree into Pictures/Movies while preserving breadcrumbs
    """
    src_root = working_source_root()
    ensure_dest_roots()

    actions: list[tuple[Path, Path, str]] = []
    unknown: list[Path] = []

    for p in src_root.rglob("*"):
        if not p.is_file():
            continue
        if should_skip(p):
            continue

        classified = destination_for_file(p, src_root)
        if classified is None:
            unknown.append(p)
            continue

        dst, kind = classified
        actions.append((p, dst, kind))

    print(f"Mode: {MODE.upper()}")
    print(f"Classify level: FILE")
    print(f"Dry run: {DRY_RUN}")
    print(f"Source working root: {src_root}")
    print(f"Destination root: {DEST_ROOT}")
    print(f"Recognized files: {len(actions)}")
    print(f"Unknown files skipped: {len(unknown)}\n")

    changed = 0
    skipped_same_size = 0
    skipped_conflict = 0
    failed = 0

    for src, dst, kind in actions:
        try:
            if dst.exists():
                if SKIP_EXISTING_SAME_SIZE and safe_same_size(src, dst):
                    print(f"SKIP SAME SIZE: {dst}")
                    skipped_same_size += 1
                    continue

                print(f"SKIP CONFLICT DIFFERENT SIZE: {dst}")
                skipped_conflict += 1
                continue

            if DRY_RUN:
                print(f"WOULD {MODE.upper()} [{kind.upper():8}] {src} -> {dst}")
                changed += 1
                continue

            if MODE == "copy":
                simple_copy(src, dst)
                print(f"COPIED [{kind.upper():8}] {src} -> {dst}")
            elif MODE == "move":
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                print(f"MOVED  [{kind.upper():8}] {src} -> {dst}")
            else:
                raise ValueError(f"Unsupported MODE: {MODE}")

            changed += 1

        except Exception as e:
            print(f"FAILED: {src} -> {dst} :: {e}")
            failed += 1

    deleted_dirs = 0
    if MODE == "move" and not DRY_RUN and DELETE_EMPTY_DIRS_AFTER_MOVE:
        # Remove empty dirs under the working source root.
        deleted_dirs = remove_empty_dirs(src_root)

    print("\n=== SUMMARY ===")
    print(f"Changed ({'would change' if DRY_RUN else 'changed'}): {changed}")
    print(f"Skipped existing same size: {skipped_same_size}")
    print(f"Skipped conflicts different size: {skipped_conflict}")
    print(f"Failed: {failed}")
    print(f"Unknown files skipped: {len(unknown)}")
    if MODE == "move":
        print(f"Deleted empty dirs: {deleted_dirs}")


def run_folder_level() -> None:
    """
    Folder-level reclassification.

    Intended for a Mixed/_unsorted tree. Finds topmost pure subfolders and moves
    them into Pictures/_unsorted or Movies/_unsorted while preserving breadcrumbs.
    """
    if MODE != "move":
        raise ValueError("Folder-level mode only supports MODE='move'.")

    src_root = working_source_root()
    ensure_dest_roots()

    moves = topmost_reclassifiable_dirs(src_root)

    print(f"Mode: {MODE.upper()}")
    print(f"Classify level: FOLDER")
    print(f"Dry run: {DRY_RUN}")
    print(f"Source working root: {src_root}")
    print(f"Destination root: {DEST_ROOT}")
    print(f"Found reclassifiable folders: {len(moves)}\n")

    for src, kind in moves:
        rel = src.relative_to(src_root)
        dst = (PICTURES_ROOT if kind == "pictures" else MOVIES_ROOT) / rel
        print(f"[{kind.upper():8}] {src} -> {dst}")

    if DRY_RUN:
        print("\nDry run complete. Set DRY_RUN = False to perform moves.")
        return

    moved = 0
    skipped_conflict = 0
    failed = 0

    print("\nExecuting moves...\n")
    for src, kind in moves:
        rel = src.relative_to(src_root)
        dst = (PICTURES_ROOT if kind == "pictures" else MOVIES_ROOT) / rel

        try:
            if dst.exists():
                print(f"SKIP CONFLICT: {dst}")
                skipped_conflict += 1
                continue

            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            print(f"MOVED: {src} -> {dst}")
            moved += 1

        except Exception as e:
            print(f"FAILED: {src} -> {dst} :: {e}")
            failed += 1

    deleted_dirs = 0
    if DELETE_EMPTY_DIRS_AFTER_MOVE:
        deleted_dirs = remove_empty_dirs(src_root)

    print("\n=== SUMMARY ===")
    print(f"Moved: {moved}")
    print(f"Skipped conflicts: {skipped_conflict}")
    print(f"Failed: {failed}")
    print(f"Deleted empty dirs: {deleted_dirs}")


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    if MODE not in {"copy", "move"}:
        raise ValueError("MODE must be 'copy' or 'move'.")

    if CLASSIFY_LEVEL not in {"file", "folder"}:
        raise ValueError("CLASSIFY_LEVEL must be 'file' or 'folder'.")

    if not working_source_root().exists():
        raise FileNotFoundError(f"Working source root does not exist: {working_source_root()}")

    if CLASSIFY_LEVEL == "file":
        run_file_level()
    else:
        run_folder_level()


if __name__ == "__main__":
    main()
