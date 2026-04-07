# CSV Guide

This document explains how to populate the working CSV files in `data/input/working/`.

The generated CSVs are created by `scripts/generate_csvs.py`. Do not edit the files in `data/input/generated/` directly. Copy the year you want to work on into `data/input/working/` and edit that copy.

## CSV columns

Current column order:

```csv
filename,file_extension,parent_folder,full_path,asset_type,location_code,scene,person_codes,job_identifier
```

## Column reference

### `filename`
The file name only.

Example:

```text
_SUH3582.ARW
```

This is for quick visual review.

### `file_extension`
The lower-case extension.

Examples:

```text
.arw
.jpg
.tif
```

This is useful for filtering or sorting.

### `parent_folder`
The immediate parent folder of the file.

Example path:

```text
/Volumes/dataLib/Pictures/Images/2025/2025-03/2025-03-18/_SUH3582.ARW
```

For this file, `parent_folder` is:

```text
2025-03-18
```

This helps when filling rows in batches.

### `full_path`
The full absolute path to the file.

This is the source-of-truth path and should not be edited unless the file really moved.

### `asset_type`
Classifies what kind of file the row represents.

Recommended values:

- `photo`
- `reference`
- `document`

Use:

- `photo` for regular photoshoot or personal photography images
- `reference` for derivative asset reference, texture source, object photos, material captures, and similar source images
- `document` for passport scans, receipts, IDs, forms, and similar files

Leave other metadata fields blank when they do not apply. Do not use placeholder values like `NA`.

### `location_code`
A code that maps to an entry in `config/locations.yml`.

Examples:

```text
OBCA001
GGCA001
DTLA001
```

This should match a real key in `locations.yml`.

Leave blank if location is not relevant, such as many `reference` or `document` rows.

### `scene`
Optional free-text field.

Examples:

```text
Sunset
Blue hour
Studio setup
```

Use this only when helpful. For many files it can stay blank.

### `person_codes`
Comma-separated list of person codes from `config/people.yml`.

Examples:

```text
theetr1n1ty
theetr1n1ty,janedoe
```

Rules:
- use commas to separate multiple people
- do not invent new codes here
- every code must exist in `people.yml`

Leave blank if no person tagging is needed.

### `job_identifier`
Maps to Lightroom Workflow → Job Identifier.

Examples:

```text
beach_test_01
passport_scan
mbp_texture_study
client_portrait_march
```

This is very important for grouping, filtering, and later collection logic.

For `reference` and `document` assets, `job_identifier` is usually the most important populated field.

## Recommended population rules

## Regular photo rows
Use for normal photography:

- `asset_type = photo`
- `location_code` usually filled
- `scene` optional
- `person_codes` optional or filled when relevant
- `job_identifier` recommended

Example:

```csv
_SUH3582.ARW,.arw,2025-03-18,/Volumes/dataLib/Pictures/Images/2025/2025-03/2025-03-18/_SUH3582.ARW,photo,OBCA001,Sunset,theetr1n1ty,beach_test_01
```

## Reference rows
Use for asset reference such as product shots, texture captures, object photos, and similar materials.

Recommended:
- `asset_type = reference`
- leave non-applicable fields blank
- fill `job_identifier`

Example:

```csv
MBP_001.ARW,.arw,assets,/Volumes/dataLib/Pictures/Images/2023/assets/MBP_001.ARW,reference,,,,mbp_texture_study
```

## Document rows
Use for scans, IDs, receipts, and paperwork.

Recommended:
- `asset_type = document`
- leave non-applicable fields blank
- fill `job_identifier`

Example:

```csv
IMG_0001.ARW,.arw,scans,/Volumes/dataLib/Pictures/Images/2024/scans/IMG_0001.ARW,document,,,,passport_scan
```

## Rules to keep the CSV clean

- do not use `NA`
- use blanks for fields that do not apply
- use only location codes that exist in `locations.yml`
- use only person codes that exist in `people.yml`
- keep `job_identifier` consistent
- avoid free-typing alternate spellings in code fields

## Workflow reminder

1. generate fresh CSVs into `data/input/generated/`
2. copy one into `data/input/working/`
3. edit the working copy
4. use the working copy for metadata writing later
