# CSV Guide

This document explains how to populate the working CSV files in `data/input/working/`.

## CSV columns

Current column order:

```csv
filename,file_extension,parent_folder,full_path,asset_type,location_code,scene,person_codes,job_identifier
```

## Column reference

### `filename`
File name only.

### `file_extension`
Lower-case file extension.

### `parent_folder`
Immediate parent folder name.

### `full_path`
Full absolute path to the asset.

### `asset_type`
Recommended values:

- `photo`
- `reference`
- `document`

Use:
- `photo` for normal photography
- `reference` for derivative-asset reference images
- `document` for scans and paperwork

### `location_code`
Short code that maps to `config/locations.yml`.

Example:

```text
WADC001
```

### `scene`
Optional free text.

Examples:
- `portrait`
- `sunset`
- `studio`

### `person_codes`
Comma-separated list of codes from `config/people.yml`.

Examples:
- `vallady`
- `vallady,theetr1n1ty`

### `job_identifier`
Maps to Lightroom Workflow → Job Identifier.

Examples:
- `Catwoman`
- `PassportScan`
- `MacBookPro`

## Practical rules

- do not edit files inside `data/input/generated/`
- always copy to `data/input/working/`
- leave non-applicable fields blank
- do not use placeholder values like `NA`
- only use location codes that exist in `locations.yml`
- only use person codes that exist in `people.yml`

## Example rows

```csv
_SUH3603.ARW,.arw,2025-05-15,/Volumes/dataLib/Pictures/Images/2025/2025-05/2025-05-15/_SUH3603.ARW,photo,WADC001,portrait,vallady,Catwoman
IMG_0001.ARW,.arw,scans,/Volumes/dataLib/Pictures/Images/2025/scans/IMG_0001.ARW,document,,,,PassportScan
MBP_001.ARW,.arw,assets,/Volumes/dataLib/Pictures/Images/2025/assets/MBP_001.ARW,reference,,,,MacBookPro
```
