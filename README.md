# Claw-SWE-Bench Leaderboard

A self-contained static leaderboard. Open `index.html` in any browser or visit
[claw-swe-bench.github.io](https://claw-swe-bench.github.io/).

## Results and sources

The September 28, 2026 update follows the final `Claw_SWE_Bench_iclr2027.pdf`:

- **Same Model × Different Claws:** Table 2 (page 7), seven harnesses × three
  models. Every metric is the mean of three separate full-350 runs.
- **OpenClaw × Models:** Tables F.1 (page 18) and F.2 (page 19), eleven models,
  one full-350 run per model. Five additional existing model rows are retained.
- The paper's tables are transcribed in `data/sources/iclr2027_tables.json`,
  including the source PDF's SHA-256 hash and page numbers. The PDF itself is
  not hosted here. The site's Paper link still points to the original technical
  report, whose table numbering and results differ from the final manuscript.

Only fields covered by the final tables are updated. Existing results and
metadata absent from the PDF are preserved. In particular, Table 2 has no
per-language results, so the old cross-harness language values remain available
with an explicit historical-results note. They are not the language breakdown
of the new three-run means. Unreported fields for new rows display as `—`;
missing model license metadata is not inferred.

The OpenClaw rows in Table 2 and Table F.1 represent different statistics. For
example, GLM 5.1 is **71.2%** in the three-run harness comparison and **72.0%** in
the single-run model comparison. Neither section overwrites the other.

## Metrics

- **Resolved / Pass@1 (%):** solved-instance count / rate. Fractional counts in
  Table 2 are three-run means.
- **Cost (USD):** total for 350 instances, averaged across full runs in Table 2.
- **Dur (s):** mean duration per instance.
- **In / Out (M):** total input / output tokens in millions for 350 instances;
  In excludes cache-read tokens. Table 2 reports means of full-run totals.
- **Turns:** mean agent turns per instance, reported in Table F.1.
- **Cache (%):** token-weighted input cache hit rate.

The tables retain sorting, per-language toggles, the Open / Proprietary filter,
and dark / light themes. The Pareto figure uses all 21 Table 2 pairs.
Meta-Harness is based on GenericAgent.

## Update and build

`data/leaderboard.json` is the complete editable leaderboard. To reapply the
paper's values while keeping unreported fields:

```sh
python3 make_data.py
python3 make_pareto.py  # requires matplotlib
python3 build.py
python3 verify_results.py
```

`make_data.py` merges the source tables into the existing data; it does not
recreate an old baseline or discard later additions. Do not hand-edit the
generated `assets/pareto.svg` or `index.html`.

To additionally verify preservation against a previous data snapshot:

```sh
python3 verify_results.py --baseline /path/to/previous-leaderboard.json
```

The verification checks all 345 reported values (including model types), run
counts, rankings, and equality of the JSON embedded in `index.html`. The
optional baseline check verifies that unreported fields remain unchanged.

## Deploy

The repository is served by GitHub Pages. Commit the source data, scripts,
generated figure, and rebuilt `index.html` together, then publish to the
configured Pages branch.
