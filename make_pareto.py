#!/usr/bin/env python3
"""
Render assets/pareto.svg — a THEME-ADAPTIVE cost-vs-resolve Pareto figure
(5 claws x 2 models), drawn from the same data in data/leaderboard.json.

X = total API cost (USD, log scale); Y = Pass@1 (%). GLM 5.1 = brand orange,
Qwen 3.6-flash = teal (both theme-independent). Everything else (text, ticks,
axes, frontier line, marker outlines, grid) is emitted with sentinel colors and
post-processed to CSS-driven values so it follows the page's dark/light theme:
  - ink elements  -> currentColor   (the figure card sets `color` per theme)
  - grid lines    -> var(--fig-grid) (defined per theme in build.py CSS)
"""
import json, os, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "leaderboard.json")
OUT = os.path.join(HERE, "assets", "pareto.svg")

BRAND = "#f07010"     # GLM 5.1   (theme-independent)
TEAL  = "#2dd4bf"     # Qwen 3.6-flash (theme-independent)
INK   = "#ff00ff"     # sentinel -> currentColor   (text / line / axes / outlines)
GRIDC = "#00ff00"     # sentinel -> var(--fig-grid) (grid lines)

MODEL_COLOR = {"GLM 5.1": BRAND, "Qwen 3.6-flash": TEAL}
CLAW_MARK = {  # system -> (matplotlib marker, short label)
    "OpenClaw": ("o", "OpenClaw"),
    "Hermes-Agent": ("s", "Hermes"),
    "NanoBot": ("^", "NanoBot"),
    "ZeroClaw": ("D", "ZeroClaw"),
    "GenericAgent": ("P", "Generic"),
}
# per-point label nudges in offset-points: (model, system) -> (dx, dy, ha)
LABEL = {
    ("GLM 5.1", "OpenClaw"):     (12,  3, "left"),
    ("GLM 5.1", "Hermes-Agent"): (12,  4, "left"),
    ("GLM 5.1", "ZeroClaw"):     (12, -12, "left"),
    ("GLM 5.1", "GenericAgent"): (-12, -14, "right"),
    ("GLM 5.1", "NanoBot"):      (-12,  2, "right"),
    ("Qwen 3.6-flash", "OpenClaw"):     (12,  3, "left"),
    ("Qwen 3.6-flash", "Hermes-Agent"): (12,  5, "left"),
    ("Qwen 3.6-flash", "ZeroClaw"):     (12, -11, "left"),
    ("Qwen 3.6-flash", "NanoBot"):      (12,  2, "left"),
    ("Qwen 3.6-flash", "GenericAgent"): (-2, -16, "center"),
}


def load_points():
    d = json.load(open(DATA, encoding="utf-8"))
    pts = []
    for g in d["sections"]["claws"]["groups"]:
        for r in g["rows"]:
            pts.append(dict(model=g["model"], claw=r["system"],
                            cost=r["cost_usd"], y=r["total_pass1"]))
    return pts


def pareto_front(pts):
    front = []
    for p in pts:
        if not any((q["cost"] <= p["cost"] and q["y"] >= p["y"] and q is not p
                    and (q["cost"] < p["cost"] or q["y"] > p["y"])) for q in pts):
            front.append(p)
    return sorted(front, key=lambda p: p["cost"])


def main():
    pts = load_points()
    front = pareto_front(pts)

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Inter", "Helvetica", "Arial", "DejaVu Sans"],
        "svg.fonttype": "none",
        "text.color": INK, "axes.labelcolor": INK,
        "xtick.color": INK, "ytick.color": INK,
        "axes.edgecolor": GRIDC,
    })
    fig, ax = plt.subplots(figsize=(9.2, 5.2), dpi=100)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")

    ax.plot([p["cost"] for p in front], [p["y"] for p in front],
            "-", color=INK, lw=2.2, zorder=1, solid_capstyle="round", alpha=.85)

    frontset = {id(p) for p in front}
    for p in pts:
        mk, _ = CLAW_MARK[p["claw"]]
        col = MODEL_COLOR[p["model"]]
        on = id(p) in frontset
        ax.scatter(p["cost"], p["y"], marker=mk, s=200 if on else 96,
                   facecolor=col, edgecolor=(INK if on else "none"),
                   linewidth=1.6 if on else 0, zorder=4 if on else 3,
                   alpha=1.0 if on else .92)
        dx, dy, ha = LABEL[(p["model"], p["claw"])]
        ax.annotate(CLAW_MARK[p["claw"]][1], (p["cost"], p["y"]),
                    textcoords="offset points", xytext=(dx, dy), ha=ha,
                    va="center", fontsize=11, color=INK, zorder=5)

    ax.set_xscale("log")
    ax.set_xticks([20, 50, 100, 200, 500])
    ax.set_xticklabels([f"${v}" for v in (20, 50, 100, 200, 500)])
    ax.set_xlabel("Total API cost for full 350-instance run  (USD, log scale)", fontsize=12.5)
    ax.set_ylabel("Resolved rate / Pass@1  (%)", fontsize=12.5)
    ax.grid(True, which="major", color=GRIDC, lw=.8, alpha=.6)
    ax.grid(True, which="minor", color=GRIDC, lw=.5, alpha=.3)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=11)

    handles = [
        Line2D([0], [0], color=INK, lw=2.2, label="Pareto frontier"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=BRAND,
               markersize=10, label="GLM 5.1"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=TEAL,
               markersize=10, label="Qwen 3.6-flash"),
    ]
    ax.legend(handles=handles, loc="upper left", frameon=False,
              fontsize=11, labelcolor=INK, handletextpad=.6, borderaxespad=.8)

    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, format="svg", transparent=True, bbox_inches="tight")
    plt.close(fig)

    # post-process: swap sentinels for CSS-driven colors so the figure follows the theme
    s = open(OUT, encoding="utf-8").read()
    s = re.sub(re.escape(INK), "currentColor", s, flags=re.I)
    s = re.sub(re.escape(GRIDC), "var(--fig-grid)", s, flags=re.I)
    open(OUT, "w", encoding="utf-8").write(s)

    print(f"wrote {OUT}")
    print("  frontier:", " → ".join(f'{p["claw"]}({p["model"].split()[0]},${p["cost"]:.0f},{p["y"]}%)' for p in front))


if __name__ == "__main__":
    main()
