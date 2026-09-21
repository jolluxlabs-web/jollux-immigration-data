"""Minimal command-line interface for local conversion."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .perm import ingest_perm
from .pwd import ingest_pwd


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize DOL PWD or PERM disclosure data")
    parser.add_argument("dataset", choices=("pwd", "perm"))
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--format", choices=("jsonl", "csv"), default="jsonl")
    args = parser.parse_args()
    records = list(ingest_pwd(args.input) if args.dataset == "pwd" else ingest_perm(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "jsonl":
        with args.output.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    else:
        with args.output.open("w", encoding="utf-8", newline="") as handle:
            if records:
                writer = csv.DictWriter(handle, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
