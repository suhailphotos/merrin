from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


RAW_EXTENSIONS = {
    ".arw",
    ".cr2",
    ".cr3",
    ".dng",
    ".nef",
    ".orf",
    ".raf",
    ".rw2",
}

DIRECT_WRITE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".png",
    ".psd",
}

ALLOWED_ASSET_TYPES = {"photo", "reference", "document"}


@dataclass
class RowContext:
    row_number: int
    full_path: Path
    target_path: Path
    is_raw: bool
    exiftool_args: list[str]


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a top-level mapping in {path}")
    return data


def split_codes(raw_value: str) -> list[str]:
    if not raw_value:
        return []
    return [part.strip() for part in raw_value.split(",") if part.strip()]


def unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def ensure_exiftool_available() -> None:
    if shutil.which("exiftool") is None:
        raise RuntimeError(
            "ExifTool was not found in PATH. Install exiftool first and make sure "
            "the `exiftool` command works in Terminal."
        )


def build_keywords(
    asset_type: str,
    person_codes: list[str],
    people_lookup: dict[str, Any],
) -> tuple[list[str], list[str]]:
    flat_keywords: list[str] = []
    hierarchical_keywords: list[str] = []

    if asset_type:
        flat_keywords.append(asset_type)
        hierarchical_keywords.append(f"asset_type|{asset_type}")

    for code in person_codes:
        person = people_lookup[code]
        full_name = str(person["full_name"]).strip()
        if full_name:
            flat_keywords.append(full_name)
            hierarchical_keywords.append(f"people|{full_name}")

    return unique_preserve_order(flat_keywords), unique_preserve_order(hierarchical_keywords)


def build_exiftool_command(
    row: dict[str, str],
    row_number: int,
    locations_lookup: dict[str, Any],
    people_lookup: dict[str, Any],
) -> RowContext:
    full_path = Path(row["full_path"]).expanduser()
    if not full_path.exists():
        raise FileNotFoundError(f"Row {row_number}: file does not exist: {full_path}")

    ext = full_path.suffix.lower()
    is_raw = ext in RAW_EXTENSIONS
    is_direct = ext in DIRECT_WRITE_EXTENSIONS

    if not is_raw and not is_direct:
        raise ValueError(
            f"Row {row_number}: unsupported extension for metadata writing: {ext}"
        )

    asset_type = row.get("asset_type", "").strip().lower()
    if asset_type and asset_type not in ALLOWED_ASSET_TYPES:
        raise ValueError(
            f"Row {row_number}: invalid asset_type '{asset_type}'. "
            f"Allowed values: {', '.join(sorted(ALLOWED_ASSET_TYPES))}"
        )

    location_code = row.get("location_code", "").strip()
    scene = row.get("scene", "").strip()
    person_codes = split_codes(row.get("person_codes", ""))
    job_identifier = row.get("job_identifier", "").strip()

    if location_code and location_code not in locations_lookup:
        raise KeyError(f"Row {row_number}: unknown location_code '{location_code}'")

    for code in person_codes:
        if code not in people_lookup:
            raise KeyError(f"Row {row_number}: unknown person code '{code}'")

    flat_keywords, hierarchical_keywords = build_keywords(
        asset_type=asset_type,
        person_codes=person_codes,
        people_lookup=people_lookup,
    )

    if is_raw:
        target_path = full_path.with_suffix(".xmp")
    else:
        target_path = full_path

    args: list[str] = [
        "exiftool",
        "-m",
        "-P",
        "-overwrite_original",
    ]

    # Clear and rewrite controlled keyword fields each run.
    args.extend(
        [
            "-XMP-dc:Subject=",
            "-XMP-lr:HierarchicalSubject=",
        ]
    )

    for kw in flat_keywords:
        args.append(f"-XMP-dc:Subject+={kw}")

    for kw in hierarchical_keywords:
        args.append(f"-XMP-lr:HierarchicalSubject+={kw}")

    if job_identifier:
        args.append(f"-XMP-photoshop:TransmissionReference={job_identifier}")
    else:
        args.append("-XMP-photoshop:TransmissionReference=")

    if scene:
        args.append(f"-XMP-iptcCore:Scene={scene}")
    else:
        args.append("-XMP-iptcCore:Scene=")

    if location_code:
        location = locations_lookup[location_code]
        sublocation = str(location.get("sublocation", "") or "").strip()
        city = str(location.get("city", "") or "").strip()
        state = str(location.get("state", "") or "").strip()
        country = str(location.get("country", "") or "").strip()
        iso_country_code = str(location.get("iso_country_code", "") or "").strip()

        args.append(f"-XMP-iptcCore:Location={sublocation}" if sublocation else "-XMP-iptcCore:Location=")
        args.append(
            f"-XMP-iptcExt:LocationShownSublocation={sublocation}"
            if sublocation else
            "-XMP-iptcExt:LocationShownSublocation="
        )
        args.append(
            f"-XMP-iptcExt:LocationShownCity={city}"
            if city else
            "-XMP-iptcExt:LocationShownCity="
        )
        args.append(
            f"-XMP-iptcExt:LocationShownProvinceState={state}"
            if state else
            "-XMP-iptcExt:LocationShownProvinceState="
        )
        args.append(
            f"-XMP-iptcExt:LocationShownCountryName={country}"
            if country else
            "-XMP-iptcExt:LocationShownCountryName="
        )
        args.append(
            f"-XMP-iptcExt:LocationShownCountryCode={iso_country_code}"
            if iso_country_code else
            "-XMP-iptcExt:LocationShownCountryCode="
        )
    else:
        args.extend(
            [
                "-XMP-iptcCore:Location=",
                "-XMP-iptcExt:LocationShownSublocation=",
                "-XMP-iptcExt:LocationShownCity=",
                "-XMP-iptcExt:LocationShownProvinceState=",
                "-XMP-iptcExt:LocationShownCountryName=",
                "-XMP-iptcExt:LocationShownCountryCode=",
            ]
        )

    args.append(str(target_path))

    return RowContext(
        row_number=row_number,
        full_path=full_path,
        target_path=target_path,
        is_raw=is_raw,
        exiftool_args=args,
    )


def process_csv(
    csv_path: Path,
    locations_path: Path,
    people_path: Path,
    apply_changes: bool,
) -> int:
    ensure_exiftool_available()

    locations_lookup = load_yaml(locations_path)
    people_lookup = load_yaml(people_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    success_count = 0

    with csv_path.open("r", newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)

        required_columns = {
            "filename",
            "file_extension",
            "parent_folder",
            "full_path",
            "asset_type",
            "location_code",
            "scene",
            "person_codes",
            "job_identifier",
        }

        missing = required_columns - set(reader.fieldnames or [])
        if missing:
            raise ValueError(
                f"CSV is missing required columns: {', '.join(sorted(missing))}"
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                ctx = build_exiftool_command(
                    row=row,
                    row_number=row_number,
                    locations_lookup=locations_lookup,
                    people_lookup=people_lookup,
                )

                mode = "RAW->XMP" if ctx.is_raw else "DIRECT"
                print(f"[row {ctx.row_number}] {mode} {ctx.full_path}")
                print("  target:", ctx.target_path)

                if apply_changes:
                    result = subprocess.run(
                        ctx.exiftool_args,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if result.returncode != 0:
                        print("  ERROR:", result.stderr.strip() or result.stdout.strip())
                        continue

                    if result.stdout.strip():
                        print("  ", result.stdout.strip())

                else:
                    print("  DRY RUN:", " ".join(ctx.exiftool_args))

                success_count += 1

            except Exception as exc:
                print(f"[row {row_number}] ERROR: {exc}")

    return success_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write metadata from Merrin CSV into files or XMP sidecars."
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="Path to working CSV file, for example data/input/working/2025.csv",
    )
    parser.add_argument(
        "--locations",
        default="config/locations.yml",
        help="Path to locations YAML file",
    )
    parser.add_argument(
        "--people",
        default="config/people.yml",
        help="Path to people YAML file",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write metadata. Without this flag, the script runs in dry-run mode.",
    )

    args = parser.parse_args()

    processed = process_csv(
        csv_path=Path(args.csv),
        locations_path=Path(args.locations),
        people_path=Path(args.people),
        apply_changes=args.apply,
    )

    mode_text = "APPLY" if args.apply else "DRY RUN"
    print(f"\nDone. Mode: {mode_text}. Rows processed successfully: {processed}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Fatal error: {exc}", file=sys.stderr)
        sys.exit(1)
