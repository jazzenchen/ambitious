"""Recompute every number shown in the customer-section deck from the raw CSV.

Usage: python3 qbr/check_figures.py [deck.pptx] [metrics.csv]

Each number in slide text, tables and notes must equal, at the precision
shown, a value derived here straight from the CSV rows: a raw cell, a
quarter sum, a quarter-over-quarter difference, a percent change, a ratio,
or a "per 100" rate. Chart series must equal a CSV column exactly.
Exits 1 on any mismatch.
"""
import csv
import re
import sys
from itertools import combinations
from pathlib import Path

from pptx import Presentation

ROOT = Path(__file__).resolve().parent.parent
deck_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "qbr/customer_section_q3.pptx"
csv_path = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "data/q3_metrics.csv"

rows = list(csv.DictReader(open(csv_path)))
METRICS = [c for c in rows[0] if c not in ("month", "segment")]
months = sorted({r["month"] for r in rows})
segments = sorted({r["segment"] for r in rows})
Q2, Q3 = months[:3], months[3:]


def series(seg, col):
    return [float(r[col]) for m in months for r in rows if r["month"] == m and r["segment"] == seg]


# ---- allowed values, derived independently of the deck builder ----
plain, pct, ratio = set(), set(), set()
plain.add(len(months))
for seg in segments + ["all"]:
    segs = segments if seg == "all" else [seg]
    for col in METRICS:
        s = [sum(x) for x in zip(*(series(g, col) for g in segs))]
        plain.update(s)
        q2, q3 = s[:3], s[3:]
        sums = {"q2": sum(q2), "q3": sum(q3)}
        plain.update(sums.values())
        pairs = [(sums["q2"], sums["q3"]), (s[0], s[-1]), (s[2], s[5])]
        for a, b in pairs:
            plain.add(abs(b - a))
            if a:
                pct.add(abs(b - a) / a * 100)
                ratio.add(b / a)
    new = [sum(x) for x in zip(*(series(g, "new_customers") for g in segs))]
    churn = [sum(x) for x in zip(*(series(g, "churned_customers") for g in segs))]
    net = [n - c for n, c in zip(new, churn)]
    plain.update(net)
    plain.update([sum(net[:3]), sum(net[3:])])
    for n, c in list(zip(new, churn)) + [(sum(new[:3]), sum(churn[:3])), (sum(new[3:]), sum(churn[3:]))]:
        if n:
            plain.add(c / n * 100)  # churned per 100 new
    tix = [sum(x) for x in zip(*(series(g, "support_tickets") for g in segs))]
    plain.update([sum(tix[:3]) / 3, sum(tix[3:]) / 3])
# share of total MRR by segment, first and last month
for i in (0, 2, 5):
    tot = sum(series(g, "mrr_usd")[i] for g in segments)
    for g in segments:
        pct.add(series(g, "mrr_usd")[i] / tot * 100)
# share of Q2->Q3-end MRR growth by segment
tot_growth = sum(series(g, "mrr_usd")[5] - series(g, "mrr_usd")[2] for g in segments)
for g in segments:
    pct.add((series(g, "mrr_usd")[5] - series(g, "mrr_usd")[2]) / tot_growth * 100)

# Labels, not figures: years, quarter names, call numbers, month counts in words.
EXEMPT = re.compile(r"\b(?:20\d\d|Q[1-4]|Call\s+\d)\b")
NUM = re.compile(r"(\$)?([+\-−]?\d[\d,]*(?:\.\d+)?)\s*(k|K|M|%|×|x\b| ?h\b| pts?\b)?")


def matches(token_val, decimals, pool, scale=1.0):
    return any(round(abs(v) / scale, decimals) == token_val for v in pool)


def check_text(text, where, problems, count):
    clean = EXEMPT.sub(" ", text)
    for m in NUM.finditer(clean):
        dollar, raw, unit = m.group(1), m.group(2), (m.group(3) or "").strip()
        val_s = raw.replace(",", "").lstrip("+-−")
        decimals = len(val_s.split(".")[1]) if "." in val_s else 0
        val = round(float(val_s), decimals)
        if unit == "%":
            ok = matches(val, decimals, pct)
        elif unit in ("×", "x"):
            ok = matches(val, decimals, ratio)
        elif unit in ("k", "K"):
            ok = matches(val, decimals, plain, 1000)
        elif unit == "M":
            ok = matches(val, decimals, plain, 1_000_000)
        else:
            ok = matches(val, decimals, plain)
        count[0] += 1
        if not ok:
            problems.append(f"{where}: '{m.group(0).strip()}' not derivable from CSV")


if not deck_path.exists():
    print(f"FAIL: deck not found at {deck_path}")
    sys.exit(1)

columns = {(g, c): series(g, c) for g in segments for c in METRICS}
month_labels = set(months)
problems, count, charts = [], [0], 0
prs = Presentation(deck_path)
for i, slide in enumerate(prs.slides, 1):
    texts = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            texts.append(shape.text_frame.text)
        if shape.has_table:
            texts += [c.text for r in shape.table.rows for c in r.cells]
        if shape.has_chart:
            charts += 1
            plot = shape.chart.plots[0]
            for s in plot.series:
                vals = [float(v) for v in s.values]
                if vals not in columns.values():
                    problems.append(f"slide {i} chart series '{s.name}' != any CSV column")
    if slide.has_notes_slide:
        texts.append(slide.notes_slide.notes_text_frame.text)
    for t in texts:
        check_text(t, f"slide {i}", problems, count)

for p in problems:
    print(p)
status = "PASS" if not problems else "FAIL"
print(f"{status}: {count[0]} numbers and {charts} charts checked across "
      f"{len(prs.slides)} slides, {len(problems)} mismatches")
sys.exit(1 if problems else 0)
