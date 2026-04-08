# Merrin Workflow

This document explains the full end-to-end Merrin workflow and the main commands to run.

## 1. Generate inventory CSV files

Run from repo root:

```bash
python scripts/generate_csvs.py
```

This scans the configured image root and writes one CSV per top-level folder into:

```text
data/input/generated/
```

Example output:

```text
data/input/generated/2025.csv
```

## 2. Copy a generated CSV into the working folder

Never edit files in `generated/` directly.

Copy the file you want to work on:

```bash
cp data/input/generated/2025.csv data/input/working/2025.csv
```

Then edit:

```text
data/input/working/2025.csv
```

## 3. Fill metadata in the working CSV

Each row can contain:

- `asset_type`
- `location_code`
- `scene`
- `person_codes`
- `job_identifier`

See `csv-guide.md` for field-by-field guidance.

## 4. Write metadata to files and sidecars

Run:

```bash
python scripts/write_metadata.py --csv data/input/working/2025.csv
```

That is a dry run.

To actually write metadata:

```bash
python scripts/write_metadata.py --csv data/input/working/2025.csv --apply
```

Behavior:

- RAW files write to same-name `.xmp` sidecars
- non-RAW files are updated directly
- location codes are resolved through `config/locations.yml`
- person codes are resolved through `config/people.yml`

## 5. Import into Lightroom Classic

After metadata is written, import the files into Lightroom Classic.

Recommended catalog name:

```text
Lr_Master
```

## 6. Generate Smart Collection config from metadata

Once metadata exists on disk, generate the Lightroom config from the metadata itself:

```bash
python scripts/generate_config.py \
  --root /Volumes/dataLib/Pictures/Images/2025 \
  --output lua/merrin.lrplugin/Config.lua
```

This reads metadata from:

- RAW sidecars when present
- image files directly for non-RAW assets

And then builds a Lightroom plug-in config.

## 7. Install the Lightroom plug-in

In Lightroom Classic:

1. Open **File > Plug-in Manager**
2. Click **Add**
3. Select:

```text
/Users/suhail/Library/CloudStorage/Dropbox/matrix/merrin/lua/merrin.lrplugin
```

If the plug-in is already installed and you changed files:

- try **Reload Plug-in**
- if Lightroom behaves oddly, remove and re-add the plug-in

## 8. Run the plug-in

In Lightroom Classic:

- go to **Library > Plug-in Extras > Run Merrin**

This reads `Config.lua` and builds the Collection Set / Smart Collection hierarchy.

## Current Smart Collection structure pattern

The generator currently builds root sets like:

- `Models`
- `Locations`
- `Projects`

Under those, Merrin builds nested collection sets and leaf Smart Collections such as:

- `RAWs`
- `Rated`
- `Five Star`

## Notes

### Why generated config is based on written metadata
This is intentional.

The CSV is a staging format for human editing, but once metadata has been written, the metadata on disk is the durable truth.

That means Smart Collection config can be regenerated directly from the files without depending on the old working CSV.

### When Lightroom seems to cache stale plug-in state
If changes do not seem to apply:

1. Reload the plug-in
2. Remove and re-add it if needed

This is more reliable than assuming Lightroom always reloads internal Lua state cleanly.
