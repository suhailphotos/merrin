#!/usr/bin/env python3
"""
delete_approved_duplicates.py

Purpose
-------
Delete files that were previously identified as exact duplicate candidates and
then manually reviewed in a CSV.

Expected workflow
-----------------
1. Generate a duplicate-review CSV.
2. Manually review it.
3. Mark rows for deletion by setting:
   - recommended_action = delete_candidate
   - approve = yes
4. Run this script in dry-run mode first.
5. If the output looks correct, set DO_DELETE = True and run it again.

Safety behavior
---------------
- Only deletes rows where:
  - recommended_action == "delete_candidate"
  - approve is one of: yes, y, true, 1
- Does not touch rows marked "keep"
- Skips missing files safely
- Skips non-file paths safely
- Prints a summary at the end

Notes
-----
- This script is intentionally simple and explicit.
- The CSV path is set near the top for easy editing.
"""

from pathlib import Path
import csv


CSV_PATH = Path.home() / "Desktop" / "exact_duplicate_confirm_20260409_070421.csv"
DO_DELETE = False  # change to True after dry run


def main() -> None:
    delete_rows: list[tuple[int, Path]] = []
    invalid_rows: list[tuple[int, str]] = []

    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        required_cols = {
            "full_path",
            "recommended_action",
            "approve",
        }

        missing = required_cols - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

        for i, row in enumerate(reader, start=2):
            full_path = (row.get("full_path") or "").strip()
            action = (row.get("recommended_action") or "").strip().lower()
            approve = (row.get("approve") or "").strip().lower()

            if not full_path:
                invalid_rows.append((i, "missing full_path"))
                continue

            if action == "delete_candidate" and approve in {"yes", "y", "true", "1"}:
                delete_rows.append((i, Path(full_path)))

    print(f"CSV: {CSV_PATH}")
    print(f"Mode: {'DELETE' if DO_DELETE else 'DRY RUN'}")
    print(f"Approved delete rows: {len(delete_rows)}")
    print(f"Invalid rows skipped: {len(invalid_rows)}\n")

    for line_no, path in delete_rows[:100]:
        print(f"DELETE row {line_no}: {path}")
    if len(delete_rows) > 100:
        print(f"... and {len(delete_rows) - 100} more")

    if invalid_rows:
        print("\nInvalid rows:")
        for line_no, reason in invalid_rows[:20]:
            print(f"row {line_no}: {reason}")
        if len(invalid_rows) > 20:
            print(f"... and {len(invalid_rows) - 20} more")

    deleted = 0
    missing = 0
    failed = 0

    if DO_DELETE:
        print("\nExecuting deletions...\n")
        for line_no, path in delete_rows:
            try:
                if not path.exists():
                    print(f"MISSING row {line_no}: {path}")
                    missing += 1
                    continue

                if not path.is_file():
                    print(f"SKIP NOT FILE row {line_no}: {path}")
                    failed += 1
                    continue

                path.unlink()
                print(f"DELETED row {line_no}: {path}")
                deleted += 1

            except Exception as e:
                print(f"FAILED row {line_no}: {path} :: {e}")
                failed += 1

    print("\n=== SUMMARY ===")
    print(f"Deleted: {deleted}")
    print(f"Missing: {missing}")
    print(f"Failed: {failed}")

    if not DO_DELETE:
        print("\nDry run only. Set DO_DELETE = True to actually delete approved files.")


if __name__ == "__main__":
    main()
