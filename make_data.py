#!/usr/bin/env python3
"""Apply the final manuscript's tables without replacing unreported results.

Table 2: seven harnesses x three models, mean of three full-350 runs.
Tables F.1/F.2: eleven OpenClaw models, one full-350 run per model.
The checked-in leaderboard is the baseline for fields absent from these tables.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'data/leaderboard.json'
SOURCE = HERE / 'data/sources/iclr2027_tables.json'
ALIASES = {'Hermes-Agent': 'Hermes Agent', 'NanoBot': 'nanobot', 'LongCat 2.0': 'LongCat-2.0'}


def find_or_add(rows, name, defaults):
    for row in rows:
        if ALIASES.get(row['system'], row['system']) == name:
            row['system'] = name
            return row
    row = dict(defaults, system=name, instances=350, per_language={})
    rows.append(row)
    return row


def rank(rows):
    rows.sort(key=lambda row: row['total_pass1'], reverse=True)
    for i, row in enumerate(rows, 1):
        row['rank'] = i


def sync(data, source):
    oc = data['sections']['openclaw']
    for expected in source['table_f1']:
        row = find_or_add(oc['rows'], expected['system'], {'org': '', 'open_weights': None})
        row.update(expected)
        row.update(runs=1, source_table='Table F.1', new=False)
    for expected in source['table_f2']:
        row = next(row for row in oc['rows'] if row['system'] == expected['system'])
        row.update(expected)
        row['per_language_source'] = 'Table F.2 (same single run as Table F.1)'
    rank(oc['rows'])
    oc['subtitle'] = 'Fixed OpenClaw harness, varying the LLM. Tables F.1 and F.2 report one run per model; additional existing results are retained.'

    claws = data['sections']['claws']
    harness_meta = {}
    for group in claws['groups']:
        for row in group['rows']:
            name = ALIASES.get(row['system'], row['system'])
            if row.get('org'):
                harness_meta[name] = {key: row[key] for key in ('org', 'runtime', 'open_weights') if key in row}
    for expected in source['table_2']:
        model = expected['model']
        group = next((g for g in claws['groups'] if g['model'] == model), None)
        if group is None:
            group = {'model': model, 'rows': []}
            claws['groups'].append(group)
        defaults = {'org': '', 'runtime': '', 'avg_turns': None, **harness_meta.get(expected['system'], {})}
        row = find_or_add(group['rows'], expected['system'], defaults)
        # Table 2 contains no per-language values: retain the historical values,
        # explicitly marked as coming from earlier runs rather than these means.
        if row.get('per_language'):
            row['per_language_source'] = 'Earlier technical report (historical single-run results, not the Table 2 means)'
        row.update({key: value for key, value in expected.items() if key != 'model'})
        row.update(runs=3, source_table='Table 2')
        if row['system'] == 'Meta-Harness':
            row['base_harness'] = 'GenericAgent'
    for group in claws['groups']:
        rank(group['rows'])
    claws['subtitle'] = 'Seven harnesses × three models (Table 2). Each result is the mean of three separate full-350 runs.'
    data['meta']['updated'] = source['source']['synced']
    data['meta']['paper_sync'] = source['source']
    data['meta']['cost_note'] = 'Cost is total USD for 350 instances; Table 2 reports the mean of three full-run totals.'
    return data


def main():
    data = sync(json.loads(OUT.read_text()), json.loads(SOURCE.read_text()))
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(f"wrote {OUT}")
    print(f"  OpenClaw: {len(data['sections']['openclaw']['rows'])} models")
    print(f"  Cross-harness: {sum(len(g['rows']) for g in data['sections']['claws']['groups'])} pairs")


if __name__ == '__main__':
    main()
