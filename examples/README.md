# Synthetic normalized sample outputs

These JSON Lines files show the public ingestion schemas using only the invented CSV fixtures in `tests/fixtures/`:

- [`outputs/pwd.jsonl`](outputs/pwd.jsonl) contains the PWD record that passes the ingestion filters.
- [`outputs/perm.jsonl`](outputs/perm.jsonl) contains both PERM fixture records.

From the repository root, install the package in editable mode and regenerate both files with:

```bash
python -m pip install -e .
jollux-immigration-data pwd tests/fixtures/pwd.csv --output examples/outputs/pwd.jsonl
jollux-immigration-data perm tests/fixtures/perm.csv --output examples/outputs/perm.jsonl
```

The sample data is synthetic and is not copied from Department of Labor disclosure records. Regenerating the files with the commands above produces the checked-in JSON Lines content.
