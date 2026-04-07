# merrin

A metadata-first workflow for preparing large photo archives for Lightroom.

## overview

merrin is a lightweight project for scanning image archives, managing controlled vocabularies for people and locations, and applying consistent metadata before importing into a master Lightroom catalog.

The long-term goal is to support a repeatable workflow that can:

- inventory large image collections
- track stable file identifiers and hashes
- manage canonical people and location codes
- write XMP sidecars for RAW files
- write embedded metadata for supported non-RAW files
- prepare clean inputs for a single master Lightroom catalog
- support later Lightroom Smart Collection generation through Lua

## planned workflow

### 1. inventory

Scan an image archive and produce a structured inventory of files, formats, basic EXIF, and stable IDs.

### 2. metadata mapping

Maintain controlled vocabularies for people, locations, projects, and shortcut codes using human-editable config files.

### 3. metadata application

Apply reviewed metadata assignments back to files using sidecars or embedded metadata, depending on format safety.

### 4. Lightroom ingestion

Import prepared files into `Lr_Master` with consistent metadata already in place.

## repository goals

- keep the workflow scriptable and repeatable
- avoid direct modification of proprietary RAW internals
- separate inventory from tagging rules and metadata writing
- make the system friendly to large archives and future automation

## initial structure

```text
merrin/
├── README.md
├── data/
├── configs/
├── scripts/
├── src/
└── outputs/
```

## notes

This repository is intended to grow into a practical archive-ingest toolchain for Lightroom-based photo management.

