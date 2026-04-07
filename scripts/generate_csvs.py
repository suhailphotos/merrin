from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

IMAGE_ROOT = Path("/Volumes/dataLib/Pictures/Images")
OUTPUT_DIR = Path("data/input/generated")

SUPPORTED_EXTENSIONS = {
    ".arw",
    ".cr2",
    ".cr3",
    ".nef",
    ".orf",
    ".raf",
    ".rw2",
    ".dng",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".png",
    ".psd",
}

CSV_HEADERS = [
    "filename",
    "file_extension",
    "parent_folder",
    "full_path",
    "asset_type",
    "location_code",
    "scene",
    "person_codes",
    "job_identifier",
]


def iter_image_files(folder: Path) -> Iterable[Path]:
    for path in sorted(folder.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def write_csv_for_folder(root_folder: Path, output_csv: Path) -> int:
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with output_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_HEADERS)
        writer.writeheader()

        for image_path in iter_image_files(root_folder):
            writer.writerow(
                {
                    "filename": image_path.name,
                    "file_extension": image_path.suffix.lower(),
                    "parent_folder": image_path.parent.name,
                    "full_path": str(image_path),
                    "asset_type": "",
                    "location_code": "",
                    "scene": "",
                    "person_codes": "",
                    "job_identifier": "",
                }
            )
            count += 1

    return count


def main() -> None:
    if not IMAGE_ROOT.exists():
        raise FileNotFoundError(f"Image root does not exist: {IMAGE_ROOT}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    top_level_dirs = sorted([p for p in IMAGE_ROOT.iterdir() if p.is_dir()])

    if not top_level_dirs:
        print(f"No top-level folders found under: {IMAGE_ROOT}")
        return

    for folder in top_level_dirs:
        output_csv = OUTPUT_DIR / f"{folder.name}.csv"
        count = write_csv_for_folder(folder, output_csv)
        print(f"Wrote {output_csv} with {count} rows")


if __name__ == "__main__":
    main()
