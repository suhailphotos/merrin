# Merrin

Merrin is a metadata-first workflow for preparing image archives before import into Adobe Lightroom Classic.

The goal is to reduce manual tagging inside Lightroom by doing the heavy lifting beforehand:

1. generate CSV inventory files
2. fill metadata codes in a working CSV
3. write metadata to image files or XMP sidecars
4. import into Lightroom
5. generate Smart Collection hierarchy from the written metadata

## Core idea

The CSV is only a staging tool.

The long-term source of truth becomes the written metadata itself:

- RAW files get XMP sidecars
- non-RAW files are updated directly
- Lightroom imports the already-tagged assets
- Smart Collection config is generated from the metadata already present on disk

## Repository structure

```text
merrin/
├── config/
│   ├── locations.yml
│   └── people.yml
├── data/
│   ├── input/
│   │   ├── generated/
│   │   └── working/
│   └── output/
├── docs/
│   ├── csv-guide.md
│   ├── locations-guide.md
│   ├── people-guide.md
│   └── workflow.md
├── lua/
│   └── merrin.lrplugin/
│       ├── Config.lua
│       ├── Info.lua
│       ├── Main.lua
│       ├── Smart.lua
│       └── Util.lua
├── scripts/
│   ├── generate_config.py
│   ├── generate_csvs.py
│   └── write_metadata.py
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```

## Main workflow

### 1. Generate CSV inventory
`generate_csvs.py` scans the image archive and writes one CSV per top-level folder into:

```text
data/input/generated/
```

### 2. Create a working CSV
Copy the generated CSV into:

```text
data/input/working/
```

Then fill the metadata columns by hand.

### 3. Write metadata
`write_metadata.py` reads the working CSV plus:

- `config/locations.yml`
- `config/people.yml`

It then writes:

- XMP sidecars for RAW files
- direct metadata updates for non-RAW files

### 4. Import into Lightroom
Import the files into your Lightroom catalog after metadata has been written.

### 5. Generate Smart Collection config
`generate_config.py` scans written metadata from the files and sidecars and builds:

```text
lua/merrin.lrplugin/Config.lua
```

This makes metadata, not the CSV, the source of truth for Smart Collection generation.

### 6. Run the Lightroom plug-in
The Merrin Lightroom plug-in reads `Config.lua` and creates the Collection Set and Smart Collection hierarchy.

## Metadata Merrin uses

### Location
Mapped into Lightroom IPTC location fields:

- Scene
- Sublocation
- City
- State / Province
- Country / Region
- optional ISO Country Code

### People
Stored as keywords and hierarchical keywords.

Examples:
- flat keyword: `Valentina Reneff-Olson`
- hierarchical keyword: `people|Valentina Reneff-Olson`
- hierarchical keyword: `ig|@vallady`

### Project
Mapped to:

- Workflow → Job Identifier

### Asset type
Supported values:

- `photo`
- `reference`
- `document`

`photo` is treated as the default case.
`reference` and `document` can be written into hierarchical keywords.

## Why the workflow is split this way

- CSV is fast for human entry
- YAML files keep repeated names and locations reusable
- XMP / file metadata survives outside Lightroom
- Python is better for config generation
- Lightroom Lua stays focused on building the catalog hierarchy

## Reference docs

See:

- `docs/workflow.md`
- `docs/csv-guide.md`
- `docs/locations-guide.md`
- `docs/people-guide.md`
