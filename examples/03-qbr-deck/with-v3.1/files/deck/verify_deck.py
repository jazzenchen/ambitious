"""Tie every number in a deck to a figure computed from data/q3_metrics.csv.

Usage: python3 deck/verify_deck.py deck/customer_section.md [more.md ...]
Each number must match a figure for a segment and metric named on its own
line (e.g. "SMB churn"); a number on a line naming neither is untraced.
Percents must carry one decimal (54.6%, not 55%).
Exits 1 and lists each number that no CSV-derived figure explains.
"""
import csv
import itertools
import re
import sys
from pathlib import Path

CSV = Path(__file__).resolve().parent.parent / "data" / "q3_metrics.csv"
Q = {"Q2": ["2026-04", "2026-05", "2026-06"], "Q3": ["2026-07", "2026-08", "2026-09"]}
SUM_FIELDS = ["new_customers", "churned_customers", "support_tickets"]
FIELDS = SUM_FIELDS + ["mrr_usd", "nps", "avg_first_response_hours"]


SEG_WORDS = {"smb": ["smb"], "mid_market": ["mid-market", "mid market"],
             "enterprise": ["enterprise"], "all": ["total", "all segments", "company"]}
FIELD_WORDS = {"new_customers": ["new", "logos", "signed", "won"],
               "churned_customers": ["churn", "lost"],
               "net_adds": ["net"],
               "mrr_usd": ["mrr", "revenue", "growth"],
               "nps": ["nps"],
               "support_tickets": ["ticket"],
               "avg_first_response_hours": ["response", "reply"]}


def figures():
    """Return {(segment, field): (counts, percents)}: what a line may cite."""
    rows = list(csv.DictReader(open(CSV)))
    segs = sorted({r["segment"] for r in rows})
    series = {}  # (segment, field) -> {period: value}
    for r in rows:
        r["net_adds"] = int(r["new_customers"]) - int(r["churned_customers"])
        for f in FIELDS + ["net_adds"]:
            series.setdefault((r["segment"], f), {})[r["month"]] = float(r[f])
    for seg in segs:
        for f in SUM_FIELDS + ["net_adds"]:
            s = series[(seg, f)]
            for q, months in Q.items():
                s[q] = sum(s[m] for m in months)
    total = {m: sum(series[(s, "mrr_usd")][m] for s in segs) for m in series[(segs[0], "mrr_usd")]}
    series[("all", "mrr_usd")] = total

    pools = {}
    for key, s in series.items():
        counts, pcts = set(), set()
        vals = list(s.values())
        counts.update(vals)
        for a, b in itertools.permutations(vals, 2):
            counts.add(b - a)
            if a:
                pcts.add(100 * (b - a) / a)
        pools[key] = (counts, pcts)
    growth = total["2026-09"] - total["2026-06"]
    for seg in segs:
        s = series[(seg, "mrr_usd")]
        pools[(seg, "mrr_usd")][1].add(100 * (s["2026-09"] - s["2026-06"]) / growth)
        pools[(seg, "mrr_usd")][1].add(100 * s["2026-09"] / total["2026-09"])
        n, c = series[(seg, "new_customers")], series[(seg, "churned_customers")]
        for p in n:
            if n[p]:
                pools[(seg, "churned_customers")][1].add(100 * c[p] / n[p])
    return pools


def context(line, pools):
    """Pools for the segments and metrics this line names; None if it names neither."""
    low = line.lower()
    segs = [k for k, ws in SEG_WORDS.items() if any(w in low for w in ws)]
    flds = [k for k, ws in FIELD_WORDS.items() if any(w in low for w in ws)]
    if not segs or not flds:
        return None
    counts, pcts = set(), set()
    for k in itertools.product(segs, flds):
        if k in pools:
            counts |= pools[k][0]
            pcts |= pools[k][1]
    return counts, pcts


NUM = re.compile(r"(?<![\w.])([+\-−]?)\$?(\d[\d,]*(?:\.\d+)?)(k|%)?")
SKIP = re.compile(r"\b20\d\d-\d\d\b|\b20\d\d\b|\bQ[1-4]\b|^#+ |^---$|<!--.*?-->")


def matches(value, decimals, pool):
    return any(round(abs(c), decimals) == value for c in pool)


def check(path, pools):
    bad, n = [], 0
    for i, line in enumerate(Path(path).read_text().splitlines(), 1):
        if line.strip() in ("---",) or line.startswith("% "):
            continue
        text = SKIP.sub(" ", line)
        ctx = context(line, pools) or (set(), set())
        counts, pcts = ctx
        for m in NUM.finditer(text):
            raw, suffix = m.group(2).replace(",", ""), m.group(3)
            value = float(raw)
            decimals = len(raw.split(".")[1]) if "." in raw else 0
            n += 1
            if suffix == "%":
                # whole-number percents match too many pairs by luck; require 1 dp
                ok = decimals >= 1 and matches(value, decimals, pcts)
            elif suffix == "k":
                ok = matches(value, decimals, {c / 1000 for c in counts})
            else:
                ok = matches(value, decimals, counts)
            if not ok:
                bad.append(f"{path}:{i}: {m.group(0).strip()}  | {line.strip()[:70]}")
    return n, bad


if __name__ == "__main__":
    pools = figures()
    total_n, total_bad = 0, []
    for p in sys.argv[1:]:
        n, bad = check(p, pools)
        total_n += n
        total_bad += bad
    for b in total_bad:
        print("UNTRACED", b)
    print(f"{total_n - len(total_bad)}/{total_n} figures traced, {len(total_bad)} untraced")
    sys.exit(1 if total_bad or not total_n else 0)
