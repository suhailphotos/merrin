# Merrin

Merrin is a lightweight project for preparing image metadata before import into Adobe Lightroom.

The goal is to make bulk organization faster and more consistent by keeping human input small and predictable. Instead of manually filling metadata inside Lightroom for large archives, Merrin uses a simple CSV plus XML lookup files to write metadata to image files or XMP sidecars ahead of import.

## Project goal

Build and maintain a workflow that helps create a single master Lightroom catalog named `Lr_Master` with at least the following metadata applied to images before import:

- location metadata
- people keywords
- project identifier

The long-term workflow is:

1. scan image files and export a CSV
2. fill lightweight codes in the CSV
3. resolve those codes through XML lookup files
4. write metadata to files or sidecars
5. import into Lightroom
6. later generate Lightroom Smart Collections through Lua scripts

## What metadata Merrin focuses on

### Location fields
These map to the Lightroom IPTC image location section:

- Scene (optional)
- Sublocation
- City
- State
- Country / Region

`ISO Country Code` can be added later, but it is not required for the first version.

### Project field
This maps to:

- Workflow → Job Identifier

### People in the image
People are stored as Lightroom keywords.

The CSV will contain one or more person codes, and the script will resolve each code through `people.xml` and write the appropriate keyword(s).

## Design approach

The project is intentionally simple.

### Location lookup
All reusable location data lives in one XML file:

- `config/locations.xml`

A location code should resolve reusable location fields such as:

- sublocation
- city
- state
- country
- optional ISO country code

Scene is intentionally not part of the location lookup for now. It stays optional and is entered directly in the CSV only when needed.

Example idea:

- location code: `OBCA001`
- sublocation: `Ocean Beach`
- city: `San Francisco`
- state: `California`
- country: `USA`

Then the CSV can optionally add:

- scene: `Sunset`

This keeps the system fast for large archives while still allowing extra detail when useful.

### People lookup
All people data lives in one XML file:

- `config/people.xml`

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
Human editing should happen mostly in a CSV file.

Suggested version-one columns:

```csv
full_path,location_code,scene,person_codes,job_identifier
```

Field notes:

- `full_path`: full path to the image file
- `location_code`: lookup into `locations.xml`
- `scene`: optional free-text scene name
- `person_codes`: comma-separated list of people codes
- `job_identifier`: project name or project code written to Lightroom Workflow → Job Identifier

Example:

```csv
/full/path/IMG_0001.ARW,OBCA001,Sunset,theetr1n1ty,beach_test_01
/full/path/IMG_0002.ARW,OBCA001,,theetr1n1ty,beach_test_01
```

## Repository structure

Current project layout:

```text
merrin/
├── LICENSE
├── README.md
├── .gitignore
├── config/
│   ├── locations.xml
│   ├── people.xml
│   └── .keep
├── data/
│   ├── input/
│   ├── output/
│   └── .keep
├── scripts/
│   └── .keep
├── lua/
│   └── .keep
└── docs/
    └── .keep
```

### Folder purpose

#### `config/`
Lookup files used by the scripts.

- `locations.xml`: reusable location definitions
- `people.xml`: reusable people definitions

#### `data/input/`
Working CSV files and source input.

Examples:
- scanned inventory CSV
- human-edited metadata CSV
- sample input files for testing

#### `data/output/`
Generated reports and logs.

Examples:
- metadata write logs
- validation reports
- duplicate reports later if needed

#### `scripts/`
Python scripts for the workflow.

Likely scripts later:
- archive scanner
- CSV validator
- metadata writer

#### `lua/`
Lightroom Lua scripts for later automation, such as Smart Collection helpers.

#### `docs/`
Short design notes and workflow notes when needed.

## Planned workflow

### Phase 1: scanning
Create a script that scans an image archive and exports a CSV containing file paths and basic details.

Initial focus:
- find supported image files
- classify RAW vs non-RAW if needed later
- export rows for human review

### Phase 2: human tagging
Fill the CSV using short codes.

Examples:
- location code like `OBCA001`
- people codes like `theetr1n1ty,janedoe`
- optional scene only when useful
- job identifier for project grouping

### Phase 3: metadata writing
Create a script that:

1. reads the CSV
2. looks up location codes from `locations.xml`
3. looks up person codes from `people.xml`
4. writes metadata to the file or to an XMP sidecar

Expected behavior:
- RAW files should use XMP sidecars
- non-RAW files can be updated directly where appropriate
- scene is written only when present
- people become keywords
- job identifier maps to Workflow → Job Identifier

### Phase 4: Lightroom import
Import everything into the master Lightroom catalog:

- `Lr_Master`

### Phase 5: Lightroom Lua automation
Later, add Lua scripts to help build Smart Collections such as:

- by location
- by model / person
- by project
- combinations such as location → person and person → location

## Why this project stays small

This repo is intentionally minimal because the goal is to reduce human editing time, not build a large metadata platform.

Key decisions:

- one `locations.xml`
- one `people.xml`
- no separate scene code system for now
- no separate project XML for now
- small CSV with only the fields that matter most

That keeps the first version practical and easier to maintain.

## Initial implementation notes

- keep Scene optional
- use location codes for reusable location metadata
- use person codes for reusable keyword metadata
- use `job_identifier` directly from CSV
- prefer safety when writing metadata
- treat RAW files conservatively and use sidecars where appropriate

## Next steps

1. define the XML schema for `locations.xml`
2. define the XML schema for `people.xml`
3. create a sample CSV template
4. build the first archive scanning script
5. build the metadata writing script

## Status

Repo initialized. Folder structure defined. README created. XML schema and CSV template are next.

