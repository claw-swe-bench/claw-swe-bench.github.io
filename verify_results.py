#!/usr/bin/env python3
"""Check the published data against the PDF tables and an optional prior snapshot."""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALIASES = {"Hermes-Agent": "Hermes Agent", "NanoBot": "nanobot", "LongCat 2.0": "LongCat-2.0"}


def canonical(name):
    return ALIASES.get(name, name)


def check(data, source, baseline=None):
    errors = []
    checks = 0
    oc = {r["system"]: r for r in data["sections"]["openclaw"]["rows"]}
    claws = {(g["model"], r["system"]): r for g in data["sections"]["claws"]["groups"] for r in g["rows"]}
    for table, expected_rows, actual in (
        ("Table 2", source["table_2"], claws),
        ("Table F.1", source["table_f1"], oc),
        ("Table F.2", source["table_f2"], oc),
    ):
        for expected in expected_rows:
            key = (expected["model"], expected["system"]) if table == "Table 2" else expected["system"]
            row = actual.get(key)
            if row is None:
                errors.append(f"{table}: missing {key}")
                continue
            for field, value in expected.items():
                if field in ("model", "system"):
                    continue
                checks += len(value) if isinstance(value, dict) else 1
                if row.get(field) != value:
                    errors.append(f"{table}, {key}, {field}: {row.get(field)!r} != {value!r}")
            if table != "Table F.2" and row.get("runs") != (3 if table == "Table 2" else 1):
                errors.append(f"{table}: incorrect run count for {key}")
    for rows in [list(oc.values())] + [g["rows"] for g in data["sections"]["claws"]["groups"]]:
        if len({r["system"] for r in rows}) != len(rows):
            errors.append("Duplicate model or harness rows")
        if [r["total_pass1"] for r in rows] != sorted((r["total_pass1"] for r in rows), reverse=True):
            errors.append("Default ranking does not follow Pass@1")
        if [r["rank"] for r in rows] != list(range(1, len(rows) + 1)):
            errors.append("Incorrect rank numbers")
    if baseline:
        paper_oc = {r["system"] for r in source["table_f1"]}
        paper_claws = {(r["model"], r["system"]) for r in source["table_2"]}
        allowed_oc = set(source["table_f1"][0]) | {"per_language", "new", "rank"}
        allowed_claws = set(source["table_2"][0]) | {"rank"}
        for old in baseline["sections"]["openclaw"]["rows"]:
            name = canonical(old["system"])
            new = oc.get(name, {})
            allowed = allowed_oc if name in paper_oc else {"rank"}
            for field, value in old.items():
                if field not in allowed and new.get(field) != value:
                    errors.append(f"Unreported OpenClaw field changed: {name}.{field}")
        for group in baseline["sections"]["claws"]["groups"]:
            for old in group["rows"]:
                key = (group["model"], canonical(old["system"]))
                new = claws.get(key, {})
                allowed = allowed_claws if key in paper_claws else {"rank"}
                for field, value in old.items():
                    if field not in allowed and new.get(field) != value:
                        errors.append(f"Unreported cross-harness field changed: {key}.{field}")
    return checks, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, help="Check that fields absent from the PDF are preserved")
    args = parser.parse_args()
    data = json.loads((HERE / "data/leaderboard.json").read_text())
    source = json.loads((HERE / "data/sources/iclr2027_tables.json").read_text())
    baseline = json.loads(args.baseline.read_text()) if args.baseline else None
    checks, errors = check(data, source, baseline)
    html = (HERE / "index.html").read_text()
    match = re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S)
    if not match or json.loads(match[1]) != data:
        errors.append("index.html contains stale or missing leaderboard data")
    if errors:
        print("\n".join(errors))
        raise SystemExit(f"FAIL: {len(errors)} discrepancies")
    print(f"PASS: {checks} paper values, run counts, rankings, embedded data" + (", and preservation of unreported fields" if baseline else ""))


if __name__ == "__main__":
    main()
