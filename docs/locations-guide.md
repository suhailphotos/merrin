# Locations Guide

This document explains how to populate `config/locations.yml`.

This file is the reusable lookup table for location metadata. The CSV should reference location entries only by code through the `location_code` column.

## File purpose

Each top-level key in `locations.yml` is a location code.

Example:

```yaml
OBCA001:
  sublocation: Ocean Beach
  city: San Francisco
  state: California
  country: USA
  iso_country_code: US
```

When the CSV row contains:

```text
location_code = OBCA001
```

the metadata-writing script should resolve that code into the mapped location fields.

## Recommended structure

Use the code as the YAML key.

Example:

```yaml
OBCA001:
  sublocation: Ocean Beach
  city: San Francisco
  state: California
  country: USA
  iso_country_code: US
```

## Supported fields

### `sublocation`
The most specific reusable place name for the location.

Examples:

- Ocean Beach
- Golden Gate Park
- Griffith Observatory
- Downtown

### `city`
Examples:

- San Francisco
- Los Angeles
- Burbank

### `state`
Examples:

- California
- New York

### `country`
Examples:

- USA
- India
- Japan

### `iso_country_code`
Optional but useful.

Examples:

- `US`
- `IN`
- `JP`

## Scene is not stored here

Do not store `scene` in `locations.yml`.

Reason:
- scene is optional
- scene may vary even within the same reusable location
- scene is better stored directly in the CSV row

Example:
- `location_code = OBCA001`
- `scene = Sunset`

This lets the same location code be reused with different scene values.

## Example file

```yaml
OBCA001:
  sublocation: Ocean Beach
  city: San Francisco
  state: California
  country: USA
  iso_country_code: US

GGCA001:
  sublocation: Golden Gate Park
  city: San Francisco
  state: California
  country: USA
  iso_country_code: US

DTLA001:
  sublocation: Downtown
  city: Los Angeles
  state: California
  country: USA
  iso_country_code: US
```

## Naming advice for codes

Pick a consistent style and stick with it.

Your current examples are compact and readable:

- `OBCA001`
- `GGCA001`
- `DTLA001`

That is good enough.

Try to keep:
- one canonical code per reusable location
- no duplicates
- no alternate spellings for the same place

## Good practices

- keep one reusable code per location
- reuse codes instead of inventing near-duplicates
- keep field spelling consistent
- update `locations.yml` first, then use the code in CSV
- prefer the real reusable place name in `sublocation`

## Example workflow

1. add a new location block to `config/locations.yml`
2. choose a unique code
3. fill sublocation, city, state, country, and optional ISO code
4. use that code in the CSV `location_code` column
