#!/usr/bin/env python3
"""
Build leaderboard/data/leaderboard.json — numbers taken VERBATIM from the
published arXiv paper, https://arxiv.org/abs/2606.12344 (HTML: arxiv.org/html/2606.12344).

This is the single source of truth. No local spreadsheets / working drafts are
used (those are older, pre-leak-fix, and disagree with the published paper).

Sources, by parsed HTML table index:
  - OpenClaw x 9 models : Table "idx 3"  (Model | Pass@1 | Cost | Dur | Turns | Cache)
                          Table "idx 16" (Model | per-language Pass@1 | Total)
  - 5 claws x 2 models  : Table "idx 4"  (Claw | Model | Pass@1 | Cost | Dur | Cache)
                          Table "idx 17" (Claw | Model | per-language Pass@1 | Total)

Cost is TOTAL USD over the 350-instance run, exactly as printed in the paper.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "leaderboard.json")
LANGS = ["Java", "Go", "Rust", "JS/TS", "C/C++", "Ruby", "PHP", "Python"]

# model -> (org, open_weights, tier)  [open/prop best-effort, editable]
MODEL_META = {
    "GPT 5.5":           ("OpenAI",      False, "Flagship"),
    "Claude Opus 4.7":   ("Anthropic",   False, "Flagship"),
    "GLM 5.1":           ("Z.ai",        True,  "Flagship"),
    "DeepSeek-V4 Pro":   ("DeepSeek",    True,  "Flagship"),
    "DeepSeek-V4 Flash": ("DeepSeek",    True,  "Flash"),
    "Kimi K2.6":         ("Moonshot AI", True,  "Flagship"),
    "Qwen 3.6-flash":    ("Alibaba",     True,  "Flash"),
    "MiniMax M2.7":      ("MiniMax",     True,  "Flagship"),
    "Seed 2.0-mini":     ("ByteDance",   False, "Flash"),
}

# claw display -> (org, runtime)   (all open-source harnesses)
HARNESS_META = {
    "OpenClaw":     ("Steinberger",   "Node.js"),
    "Hermes-Agent": ("Nous Research", "Python"),
    "ZeroClaw":     ("ZeroClaw Labs", "Rust"),
    "GenericAgent": ("lsdefine",      "Python"),
    "NanoBot":      ("HKUDS",         "Python"),
}

# ── OpenClaw × 9 models ────────────────────────────────────────────────────
# model: [Java,Go,Rust,JS/TS,C/C++,Ruby,PHP,Python], total, resolved, cost_usd, dur_s, turns, cache%
OPENCLAW = [
    ("GPT 5.5",           [86.0,61.9,93.0,79.1,81.0,70.5,74.4,78.0], 78.0, 273, 1399.1, 603.7, 67.0, 97.3),
    ("Claude Opus 4.7",   [86.0,61.9,88.4,81.4,71.4,68.2,76.7,82.0], 77.1, 270, 1082.0, 424.6, 61.6, 97.0),
    ("GLM 5.1",           [76.7,57.1,86.0,74.4,81.0,68.2,72.1,72.0], 73.4, 257,  277.0, 586.8, 80.6, 96.5),
    ("DeepSeek-V4 Pro",   [79.1,50.0,79.1,74.4,73.8,72.7,76.7,68.0], 71.7, 251,   81.3, 662.3, 47.1, 97.4),
    ("DeepSeek-V4 Flash", [81.4,50.0,79.1,74.4,73.8,63.6,69.8,70.0], 70.3, 246,    8.2, 430.0, 51.2, 98.5),
    ("Kimi K2.6",         [69.8,50.0,74.4,65.1,71.4,68.2,69.8,66.0], 66.9, 234,  633.7,1235.3, 78.7, 92.1),
    ("Qwen 3.6-flash",    [83.7,54.8,74.4,58.1,66.7,59.1,62.8,68.0], 66.0, 231,   71.5, 636.0, 87.9, 97.6),
    ("MiniMax M2.7",      [65.1,47.6,76.7,55.8,61.9,61.4,55.8,66.0], 61.4, 215,  196.7,1165.6, 94.8, 96.2),
    ("Seed 2.0-mini",     [60.5,33.3,55.8,44.2,54.8,36.4,48.8,54.0], 48.6, 170,   19.4,1153.0, 44.4, 79.4),
]

# ── 5 claws × 2 models ─────────────────────────────────────────────────────
# model -> list of (claw, [per-lang], total, resolved, cost_usd, dur_s, cache%)  (Table 3 has no Turns)
CLAWS = {
    "GLM 5.1": [
        ("OpenClaw",     [76.7,57.1,86.0,74.4,81.0,68.2,72.1,72.0], 73.4, 257, 277.0, 586.8, 96.5),
        ("Hermes-Agent", [72.1,54.8,81.4,72.1,73.8,72.7,72.1,70.0], 71.1, 249, 330.6, 675.1, 91.3),
        ("ZeroClaw",     [83.7,50.0,86.0,69.8,69.0,65.9,69.8,68.0], 70.3, 246, 383.4, 538.2, 90.4),
        ("GenericAgent", [65.1,47.6,69.8,55.8,66.7,63.6,65.1,70.0], 63.1, 221,  85.8, 576.4, 66.8),
        ("NanoBot",      [65.1,38.1,67.4,58.1,61.9,61.4,67.4,66.0], 60.9, 213, 768.8,1166.3, 77.2),
    ],
    "Qwen 3.6-flash": [
        ("OpenClaw",     [83.7,54.8,74.4,58.1,66.7,59.1,62.8,68.0], 66.0, 231,  71.5, 636.0, 97.6),
        ("Hermes-Agent", [65.1,42.9,74.4,58.1,61.9,65.9,65.1,66.0], 62.6, 219, 103.3, 638.6, 97.4),
        ("ZeroClaw",     [62.8,47.6,72.1,55.8,47.6,56.8,55.8,66.0], 58.3, 204,  49.3, 428.9, 96.9),
        ("NanoBot",      [41.9,42.9,58.1,37.2,45.2,45.5,48.8,58.0], 47.4, 166, 133.1, 562.7, 63.9),
        ("GenericAgent", [44.2,19.0,55.8,32.6,38.1,25.0,48.8,44.0], 38.6, 135,  14.5, 321.4, 74.7),
    ],
}


def lang_map(arr):
    return {L: arr[i] for i, L in enumerate(LANGS)}


def build_openclaw_rows():
    rows = []
    for name, perlang, total, resolved, cost, dur, turns, cache in OPENCLAW:
        org, openw, tier = MODEL_META[name]
        rows.append(dict(
            system=name, org=org, open_weights=openw, tier=tier,
            total_pass1=total, resolved=resolved, instances=350,
            per_language=lang_map(perlang),
            cost_usd=cost, avg_duration_s=dur, avg_turns=turns, cache_hit=cache,
        ))
    rows.sort(key=lambda r: r["total_pass1"], reverse=True)
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return rows


def build_claws_groups():
    groups = []
    for model, cells in CLAWS.items():
        rows = []
        for claw, perlang, total, resolved, cost, dur, cache in cells:
            org, runtime = HARNESS_META[claw]
            rows.append(dict(
                system=claw, org=org, runtime=runtime, open_weights=True,
                total_pass1=total, resolved=resolved, instances=350,
                per_language=lang_map(perlang),
                cost_usd=cost, avg_duration_s=dur, avg_turns=None, cache_hit=cache,
            ))
        rows.sort(key=lambda r: r["total_pass1"], reverse=True)
        for i, r in enumerate(rows, 1):
            r["rank"] = i
        groups.append(dict(model=model, rows=rows))
    return groups


def main():
    data = dict(
        meta=dict(
            name="Claw-SWE-Bench",
            split="Full-350",
            instances=350,
            languages=LANGS,
            primary_metric="Total Pass@1",
            paper="https://arxiv.org/abs/2606.12344",
            github="https://github.com/opensquilla/claw-swe-bench",
            cost_note="Cost is total USD over the 350-instance run, as reported in the paper.",
            description=("Claw-SWE-Bench elevates the agent harness (a \"claw\") to a "
                         "controlled variable: model, task set, Docker runtime and the "
                         "official SWE-bench evaluator are held fixed; only the harness "
                         "(or the model under a fixed harness) varies. 350 real GitHub "
                         "issue-resolution tasks across 8 languages and 43 repositories."),
        ),
        sections=dict(
            openclaw=dict(
                id="openclaw",
                title="OpenClaw × Models",
                subtitle="Fixed harness (OpenClaw), varying the LLM — isolates the model effect (paper Table 2).",
                fixed="OpenClaw harness",
                rows=build_openclaw_rows(),
            ),
            claws=dict(
                id="claws",
                title="Same Model × Different Claws",
                subtitle="Fixed model, varying the harness across 5 claws — isolates the harness effect (paper Table 3).",
                fixed="Model",
                groups=build_claws_groups(),
            ),
        ),
    )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    nopen = len(data["sections"]["openclaw"]["rows"])
    nclaw = sum(len(g["rows"]) for g in data["sections"]["claws"]["groups"])
    print(f"wrote {OUT}")
    print(f"  openclaw section: {nopen} models")
    print(f"  claws section:    {nclaw} cells across {len(data['sections']['claws']['groups'])} models (5 claws each)")


if __name__ == "__main__":
    main()
