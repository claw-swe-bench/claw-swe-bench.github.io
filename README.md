# Claw-SWE-Bench Leaderboard

A self-contained static leaderboard site, styled after [opensquilla.ai](https://opensquilla.ai/)
and built on the same pattern as the [SWE-bench leaderboard](https://github.com/SWE-bench/swe-bench.github.io)
(`build.py` renders a static `index.html` from a JSON data file).

## View it
Just **double-click `index.html`** — it opens in any browser, no server needed
(the data is baked inline).

## Two sections (Full-350 split)
- **OpenClaw × Models** — fix the OpenClaw harness, vary the LLM (9 models). Paper Table 2.
- **Same Model × Different Claws** — fix the model (GLM 5.1, Qwen 3.6-flash), vary the
  harness across **5 claws** (OpenClaw / Hermes-Agent / ZeroClaw / GenericAgent / NanoBot).
  Paper Table 3.

Columns: Pass@1 (primary), per-language Pass@1 (toggle), Cost (USD), Dur (s).
Tables are click-to-sort; OpenClaw has an Open / Proprietary filter.

## Files
| File | What it is |
|---|---|
| `index.html` | The site. **Generated — don't hand-edit.** |
| `data/leaderboard.json` | The data source of truth. Edit numbers/tags here. |
| `make_data.py` | Builds `leaderboard.json` from the arXiv paper numbers (hardcoded verbatim). |
| `build.py` | Renders `data/leaderboard.json` → `index.html`. |

## Edit the data
1. Edit `data/leaderboard.json` (or re-run `python3 make_data.py` to regenerate from source).
2. Run `python3 build.py` to rebuild `index.html`.

## Data provenance & caveats
- **All numbers come straight from the published paper, https://arxiv.org/abs/2606.12344**
  (HTML: `arxiv.org/html/2606.12344`), Tables 2 & 3. `make_data.py` holds them verbatim
  with the source table indices noted. No local spreadsheets / working drafts are used
  (those are older, pre-leak-fix, and disagree with the published paper).
- **Cost** is the total USD over the full 350-instance run, exactly as printed in the paper.
- **open-weights / org tags** are best-effort — verify and edit in `leaderboard.json`.

## Deploy (optional)
It's a static site. Push the folder to **GitHub Pages** (or Netlify/Vercel) and it works as-is.
Update the `Paper` and `GitHub` links in `data/leaderboard.json` (`meta.paper`) and in
`build.py` (the GitHub button URL) before publishing.
