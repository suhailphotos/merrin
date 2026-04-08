from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


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

SUPPORTED_ASSET_EXTENSIONS = {
    ".arw",
    ".cr2",
    ".cr3",
    ".dng",
    ".nef",
    ".orf",
    ".raf",
    ".rw2",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".png",
    ".psd",
    ".psb",
}

LEAF_SMART_COLLECTIONS = [
    {
        "name": "RAWs",
        "rules": [
            {"field": "fileFormat", "op": "==", "value": "RAW"},
        ],
    },
    {
        "name": "Rated",
        "rules": [
            {"field": "rating", "op": ">=", "value": 1},
        ],
    },
    {
        "name": "Five Star",
        "rules": [
            {"field": "rating", "op": "==", "value": 5},
        ],
    },
]

EXIFTOOL_TAGS = [
    "-XMP-lr:HierarchicalSubject",
    "-XMP-iptcCore:Location",
    "-XMP-photoshop:TransmissionReference",
]

CHUNK_SIZE = 200


def ensure_exiftool_available() -> None:
    if shutil.which("exiftool") is None:
        raise RuntimeError(
            "ExifTool was not found in PATH. Install exiftool first and make sure "
            "the `exiftool` command works in Terminal."
        )


def iter_asset_files(root: Path) -> list[Path]:
    assets: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_ASSET_EXTENSIONS:
            continue
        assets.append(path)
    return assets


def metadata_source_for_asset(asset_path: Path) -> Path:
    ext = asset_path.suffix.lower()
    if ext in RAW_EXTENSIONS:
        xmp_path = asset_path.with_suffix(".xmp")
        if xmp_path.exists():
            return xmp_path
    return asset_path


def chunked(items: list[Path], size: int) -> list[list[Path]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def run_exiftool_json(paths: list[Path]) -> list[dict[str, Any]]:
    if not paths:
        return []

    cmd = [
        "exiftool",
        "-json",
        "-m",
        *EXIFTOOL_TAGS,
        *[str(p) for p in paths],
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse ExifTool JSON output: {exc}") from exc

    if not isinstance(data, list):
        raise RuntimeError("ExifTool JSON output was not a list.")

    return data


def load_metadata_for_sources(sources: list[Path]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}

    for batch in chunked(sources, CHUNK_SIZE):
        rows = run_exiftool_json(batch)
        for row in rows:
            source_file = str(row.get("SourceFile", "")).strip()
            if source_file:
                out[source_file] = row

    return out


def ensure_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    return [text] if text else []


def first_text(*values: Any) -> str:
    for value in values:
        text = str(value).strip() if value is not None else ""
        if text:
            return text
    return ""


def parse_people_from_hierarchical_subject(
    hierarchical_subjects: list[str],
) -> list[tuple[str, str]]:
    """
    Returns list of (display_name, keyword_value_for_rule).

    Preferred mapping:
    - display_name from people|...
    - rule value from ig|...

    Since your metadata writer emits these in paired order, we zip them when counts match.
    Fallbacks:
    - if only a name exists, use the name as both display and rule value
    - if only an ig handle exists, use the handle as both display and rule value
    """
    people_names: list[str] = []
    ig_handles: list[str] = []

    for item in hierarchical_subjects:
        if item.startswith("people|"):
            people_names.append(item.split("|", 1)[1].strip())
        elif item.startswith("ig|"):
            ig_handles.append(item.split("|", 1)[1].strip())

    pairs: list[tuple[str, str]] = []

    if people_names and ig_handles and len(people_names) == len(ig_handles):
        for name, handle in zip(people_names, ig_handles):
            if name and handle:
                pairs.append((name, handle))
        return dedupe_pairs(pairs)

    if people_names and not ig_handles:
        for name in people_names:
            pairs.append((name, name))
        return dedupe_pairs(pairs)

    if ig_handles and not people_names:
        for handle in ig_handles:
            pairs.append((handle, handle))
        return dedupe_pairs(pairs)

    # Mixed-count fallback
    max_len = max(len(people_names), len(ig_handles), 0)
    for i in range(max_len):
        name = people_names[i] if i < len(people_names) else ""
        handle = ig_handles[i] if i < len(ig_handles) else ""

        display = name or handle
        rule_value = handle or name

        if display and rule_value:
            pairs.append((display, rule_value))

    return dedupe_pairs(pairs)


def dedupe_pairs(values: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    out: list[tuple[str, str]] = []

    for pair in values:
        if pair not in seen:
            seen.add(pair)
            out.append(pair)

    return out


def build_config_structure(asset_root: Path) -> dict[str, Any]:
    assets = iter_asset_files(asset_root)
    if not assets:
        raise RuntimeError(f"No supported assets found under: {asset_root}")

    metadata_sources = sorted({metadata_source_for_asset(asset) for asset in assets})
    metadata_by_source = load_metadata_for_sources(metadata_sources)

    models_map: dict[str, dict[str, set[str]]] = {}
    locations_map: dict[str, set[str]] = {}
    projects_set: set[str] = set()

    for asset_path in assets:
        meta_source = metadata_source_for_asset(asset_path)
        row = metadata_by_source.get(str(meta_source), {})

        hierarchical_subjects = ensure_list(row.get("HierarchicalSubject"))
        location = first_text(row.get("Location"))
        project = first_text(
            row.get("TransmissionReference"),
            row.get("JobIdentifier"),
        )

        people = parse_people_from_hierarchical_subject(hierarchical_subjects)

        if project:
            projects_set.add(project)

        if location and project:
            locations_map.setdefault(location, set()).add(project)

        if project and people:
            for display_name, rule_value in people:
                model_entry = models_map.setdefault(display_name, {})
                model_entry.setdefault(rule_value, set()).add(project)

    groups: list[dict[str, Any]] = []

    model_children: list[dict[str, Any]] = []
    for display_name in sorted(models_map):
        rule_map = models_map[display_name]

        # In practice there should usually be one rule value per display name.
        # If there are multiple, create separate sibling nodes with the same display name.
        for rule_value in sorted(rule_map):
            projects = sorted(rule_map[rule_value])

            project_children = [
                make_project_node(project_name)
                for project_name in projects
            ]

            model_children.append(
                {
                    "name": display_name,
                    "rules": [
                        {"field": "keywords", "op": "any", "value": rule_value},
                    ],
                    "children": project_children,
                }
            )

    groups.append(
        {
            "name": "Models",
            "children": model_children,
        }
    )

    location_children: list[dict[str, Any]] = []
    for location_name in sorted(locations_map):
        projects = sorted(locations_map[location_name])

        location_children.append(
            {
                "name": location_name,
                "rules": [
                    {"field": "location", "op": "==", "value": location_name},
                ],
                "children": [make_project_node(project_name) for project_name in projects],
            }
        )

    groups.append(
        {
            "name": "Locations",
            "children": location_children,
        }
    )

    project_children = [make_project_leaf_node(project_name) for project_name in sorted(projects_set)]

    groups.append(
        {
            "name": "Projects",
            "children": project_children,
        }
    )

    return {"groups": groups}


def make_project_node(project_name: str) -> dict[str, Any]:
    return {
        "name": project_name,
        "rules": [
            {"field": "jobIdentifier", "op": "==", "value": project_name},
        ],
        "smart": copy_leaf_smart_collections(),
    }


def make_project_leaf_node(project_name: str) -> dict[str, Any]:
    return {
        "name": project_name,
        "rules": [
            {"field": "jobIdentifier", "op": "==", "value": project_name},
        ],
        "smart": copy_leaf_smart_collections(),
    }


def copy_leaf_smart_collections() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in LEAF_SMART_COLLECTIONS:
        out.append(
            {
                "name": item["name"],
                "rules": [
                    {
                        "field": rule["field"],
                        "op": rule["op"],
                        "value": rule["value"],
                    }
                    for rule in item["rules"]
                ],
            }
        )
    return out


def lua_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
    )


def to_lua(value: Any, indent: int = 0) -> str:
    space = "    " * indent
    next_space = "    " * (indent + 1)

    if value is None:
        return "nil"

    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, (int, float)):
        return str(value)

    if isinstance(value, str):
        return f'"{lua_escape(value)}"'

    if isinstance(value, list):
        if not value:
            return "{}"

        parts = ["{"]  # noqa: PIE790
        for item in value:
            parts.append(f"{next_space}{to_lua(item, indent + 1)},")
        parts.append(f"{space}}}")
        return "\n".join(parts)

    if isinstance(value, dict):
        if not value:
            return "{}"

        parts = ["{"]  # noqa: PIE790
        for key, item in value.items():
            parts.append(f"{next_space}{key} = {to_lua(item, indent + 1)},")
        parts.append(f"{space}}}")
        return "\n".join(parts)

    raise TypeError(f"Unsupported type for Lua serialization: {type(value)!r}")


def render_config_lua(config: dict[str, Any]) -> str:
    return "return " + to_lua(config, indent=0) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Merrin Config.lua from file metadata."
    )
    parser.add_argument(
        "--root",
        required=True,
        help="Root folder containing image assets, for example /Volumes/dataLib/Pictures/Images/2025",
    )
    parser.add_argument(
        "--output",
        default="lua/merrin.lrplugin/Config.lua",
        help="Output path for generated Config.lua",
    )

    args = parser.parse_args()

    ensure_exiftool_available()

    asset_root = Path(args.root).expanduser()
    if not asset_root.exists():
        raise FileNotFoundError(f"Root path does not exist: {asset_root}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    config = build_config_structure(asset_root)
    lua_text = render_config_lua(config)

    output_path.write_text(lua_text, encoding="utf-8")

    model_count = len(config["groups"][0]["children"])
    location_count = len(config["groups"][1]["children"])
    project_count = len(config["groups"][2]["children"])

    print(f"Wrote {output_path}")
    print(f"Models: {model_count}")
    print(f"Locations: {location_count}")
    print(f"Projects: {project_count}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Fatal error: {exc}", file=sys.stderr)
        sys.exit(1)
