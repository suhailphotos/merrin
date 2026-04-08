# Locations Guide

This document explains how to populate `config/locations.yml`.

## Purpose

Each top-level key is a reusable location code used by the CSV.

Example:

```yaml
WADC001:
  sublocation: Walt Disney Concert Hall
  city: Los Angeles
  state: California
  country: USA
  iso_country_code: US
```

If a CSV row uses:

```text
location_code = WADC001
```

the metadata writer resolves the location fields from this file.

## Supported fields

- `sublocation`
- `city`
- `state`
- `country`
- `iso_country_code`

## Notes

- keep codes short and stable
- use one canonical code per reusable location
- `scene` is not stored here
- `scene` stays in the CSV because it varies per shoot

## Example

```yaml
WADC001:
  sublocation: Walt Disney Concert Hall
  city: Los Angeles
  state: California
  country: USA
  iso_country_code: US

OBCA001:
  sublocation: Ocean Beach
  city: San Francisco
  state: California
  country: USA
  iso_country_code: US
```
