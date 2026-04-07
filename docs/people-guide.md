# People Guide

This document explains how to populate `config/people.yml`.

This file is the reusable lookup table for people metadata. The CSV should reference people only by code through the `person_codes` column.

## File purpose

Each top-level key in `people.yml` is a person code.

Example:

```yaml
theetr1n1ty:
  full_name: Trinity Woodward
  ig_handle: "@theetr1n1ty"
  sex: Female
```

When the CSV row contains:

```text
person_codes = theetr1n1ty
```

the metadata-writing script should resolve that code and write the appropriate keyword metadata.

## Recommended structure

Use the code as the YAML key.

Example:

```yaml
theetr1n1ty:
  full_name: Trinity Woodward
  ig_handle: "@theetr1n1ty"
  sex: Female
```

## Supported fields

### `full_name`
The canonical human-readable name.

Examples:

- Trinity Woodward
- Jane Doe
- John Doe

This should be the main value used when writing person keywords unless you later decide otherwise.

### `ig_handle`
Optional but useful as a reference.

Examples:

- "@theetr1n1ty"
- "@janedoe"

Because handles begin with `@`, keep them quoted in YAML.

### `sex`
Optional reference field.

Examples:

- Female
- Male

This can stay simple for now.

## Why use the handle-like code

Using a memorable unique code like `theetr1n1ty` works well because:

- it is easy to type or paste into the CSV
- it is already unique for you
- it avoids ambiguous short names

## Example file

```yaml
theetr1n1ty:
  full_name: Trinity Woodward
  ig_handle: "@theetr1n1ty"
  sex: Female

janedoe:
  full_name: Jane Doe
  ig_handle: "@janedoe"
  sex: Female

johndoe:
  full_name: John Doe
  ig_handle: "@johndoe"
  sex: Male
```

## Multiple people in one CSV row

Use comma-separated codes in `person_codes`.

Example:

```text
theetr1n1ty,janedoe
```

Rules:
- separate with commas
- no spaces needed
- every code must exist in `people.yml`

## Good practices

- keep one canonical code per person
- do not invent new codes directly in the CSV
- add the person to `people.yml` first
- keep `full_name` human-readable
- keep codes stable over time

## Example workflow

1. add a new person block to `config/people.yml`
2. choose a stable unique code
3. fill full name, handle, and optional sex
4. use that code in the CSV `person_codes` column
