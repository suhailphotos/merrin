# Merrin

Merrin is a lightweight project for preparing image metadata before import into Adobe Lightroom.

The goal is to make bulk organization faster and more consistent by keeping human input small and predictable. Instead of manually filling metadata inside Lightroom for large archives, Merrin uses generated CSV files plus YAML lookup files to write metadata to image files or XMP sidecars ahead of import.

## Project goal

Build and maintain a workflow that helps create a single master Lightroom catalog named `Lr_Master` with at least the following metadata applied to images before import:

- location metadata
- people keywords
- project identifier

The long-term workflow is:

1. scan image files and export year-based CSV files
2. copy generated CSVs into a working folder
3. fill lightweight codes in the working CSV
4. resolve those codes through YAML lookup files
5. write metadata to files or sidecars
6. import into Lightroom
7. later generate Lightroom Smart Collections through Lua scripts

## What metadata Merrin focuses on

### Location fields
These map to the Lightroom IPTC image location section:

- Scene (optional)
- Sublocation
- City
- State / Province
- Country / Region

`ISO Country Code` can be added and stored in `locations.yml`, but it is not required for the first version of the workflow.

### Project field
This maps to:

- Workflow → Job Identifier

### People in the image
People are stored as Lightroom keywords.

The CSV contains one or more person codes, and the script resolves each code through `config/people.yml` and writes the appropriate keyword(s).

### Asset type
Not every file is a normal photoshoot image.

Some files are:

- regular photos
- reference images for derivative work such as textures or 3D assets
- documents such as passport scans

To support this, the CSV includes an `asset_type` column.

Recommended values:

- `photo`
- `reference`
- `document`

This is better than filling non-applicable fields with placeholder values like `NA`.

## Design approach

The project is intentionally simple.

### Location lookup
All reusable location data lives in one YAML file:

- `config/locations.yml`

A location code resolves reusable location fields such as:

- sublocation
- city
- state
- country
- optional ISO country code

Scene is intentionally not part of the location lookup. It stays optional and is entered directly in the CSV only when needed.

Example:

- location code: `OBCA001`
- sublocation: `Ocean Beach`
- city: `San Francisco`
- state: `California`
- country: `USA`

Then the CSV can optionally add:

- scene: `Sunset`

### People lookup
All people data lives in one YAML file:

- `config/people.yml`

Each person record is intentionally minimal:

- code
- full name
- IG handle
- sex

Example:

- code: `theetr1n1ty`
- full name: `Trinity Woodward`
- IG handle: `@theetr1n1ty`
- sex: `Female`

The code is designed to be easy to type or paste into the CSV. Using a unique handle is acceptable and keeps the human workflow simple.

### CSV-driven editing
Human editing should happen mostly in CSV files inside the working folder.

Current columns:

```csv
filename,file_extension,parent_folder,full_path,asset_type,location_code,scene,person_codes,job_identifier
```

Field notes:

- `filename`: file name only
- `file_extension`: lower-case file extension
- `parent_folder`: immediate parent folder name
- `full_path`: full path to the image file
- `asset_type`: `photo`, `reference`, or `document`
- `location_code`: lookup into `config/locations.yml`
- `scene`: optional free-text scene name
- `person_codes`: comma-separated list of people codes
- `job_identifier`: project name or project code written to Lightroom Workflow → Job Identifier

Example:

```csv
_SUH3582.ARW,.arw,2025-03-18,/Volumes/dataLib/Pictures/Images/2025/2025-03/2025-03-18/_SUH3582.ARW,photo,OBCA001,Sunset,theetr1n1ty,beach_test_01
IMG_0001.ARW,.arw,scans,/Volumes/dataLib/Pictures/Images/2024/scans/IMG_0001.ARW,document,,,,passport_scan
MBP_001.ARW,.arw,assets,/Volumes/dataLib/Pictures/Images/2023/assets/MBP_001.ARW,reference,,,,mbp_texture_study
```

## Repository structure

Current project layout:

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
├── lua/
├── scripts/
│   └── generate_csvs.py
├── LICENSE
└── README.md
```

### Folder purpose

#### `config/`
Lookup files used by the scripts.

- `locations.yml`: reusable location definitions
- `people.yml`: reusable people definitions

#### `data/input/generated/`
Scanner output. Safe to regenerate.

Examples:
- `2017.csv`
- `2018.csv`
- `2025.csv`

#### `data/input/working/`
Your editable copies. These are the files you actually fill by hand.

Recommended workflow:
1. generate fresh CSVs into `generated/`
2. copy the year you want into `working/`
3. edit only the copy in `working/`

#### `data/output/`
Generated reports and logs.

Examples:
- metadata write logs
- validation reports
- duplicate reports later if needed

#### `scripts/`
Python scripts for the workflow.

Current script:
- `generate_csvs.py`

Likely scripts later:
- CSV validator
- metadata writer

#### `lua/`
Lightroom Lua scripts for later automation, such as Smart Collection helpers.

#### `docs/`
Reference notes for how to populate CSV and YAML files.

## Planned workflow

### Phase 1: scanning
Use `scripts/generate_csvs.py` to scan the archive and export one CSV per top-level year folder.

Current source root:

```text
/Volumes/dataLib/Pictures/Images
```

### Phase 2: copy to working
Copy generated CSVs into `data/input/working/` before editing.

Example:

```bash
cp data/input/generated/2025.csv data/input/working/2025.csv
```

### Phase 3: human tagging
Fill the working CSV using short codes.

Examples:
- location code like `OBCA001`
- people codes like `theetr1n1ty,janedoe`
- optional scene only when useful
- job identifier for project grouping
- asset type for deciding how the file should be treated later

### Phase 4: metadata writing
Create a script that:

1. reads the working CSV
2. looks up location codes from `locations.yml`
3. looks up person codes from `people.yml`
4. writes metadata to the file or to an XMP sidecar

Expected behavior:
- RAW files should use XMP sidecars
- non-RAW files can be updated directly where appropriate
- scene is written only when present
- people become keywords
- job identifier maps to Workflow → Job Identifier
- asset type can later be written as a keyword or used for Lightroom collection logic

### Phase 5: Lightroom import
Import everything into the master Lightroom catalog:

- `Lr_Master`

### Phase 6: Lightroom Lua automation
Later, add Lua scripts to help build Smart Collections such as:

- by location
- by model / person
- by project
- by asset type
- combinations such as location → person and person → location

## Why this project stays small

This repo is intentionally minimal because the goal is to reduce human editing time, not build a large metadata platform.

Key decisions:

- one `locations.yml`
- one `people.yml`
- no separate scene code system for now
- no separate project lookup file for now
- one CSV per top-level year folder
- generated and working CSVs are kept separate
- small set of required fields

That keeps the first version practical and easier to maintain.

## Reference docs

See the docs folder for detailed population guides:

- `docs/csv-guide.md`
- `docs/locations-guide.md`
- `docs/people-guide.md`

## Status

Repo initialized. Folder structure defined. CSV generator in place. YAML lookup files in place. Next step is building the metadata writing script.

