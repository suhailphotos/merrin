# People Guide

This document explains how to populate `config/people.yml`.

## Purpose

Each top-level key is a reusable person code used by the CSV.

Example:

```yaml
vallady:
  full_name: Valentina Reneff-Olson
  ig_handle: "@vallady"
  sex: Female
```

When the CSV contains:

```text
person_codes = vallady
```

the metadata writer resolves the person into:

- flat keyword for full name
- hierarchical keyword under `people|`
- hierarchical keyword under `ig|`

## Supported fields

- `full_name`
- `ig_handle`
- `sex`

## Notes

- use a stable code
- the code does not need to match the IG handle, but it often can
- the IG handle should stay quoted in YAML because of `@`

## Example

```yaml
vallady:
  full_name: Valentina Reneff-Olson
  ig_handle: "@vallady"
  sex: Female

theetr1n1ty:
  full_name: Trinity Woodward
  ig_handle: "@theetr1n1ty"
  sex: Female
```
