# The card /ambitious printed before doing any work (verbatim from the run)

The SMB segment isn't fine. Sign-ups hit a record, but customers leaving grew faster, so SMB's net gain stayed at exactly 450 in both quarters while support reply times more than doubled. Rung 2 turns the section into two decisions for the room, each argued both ways, with every number checked by a script against your data.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    Q3 QBR customer section, ~8 slides (as .pptx, inferred)
found    SMB net adds flat: +450 in Q2, +450 in Q3 (q3_metrics.csv)
doubt    "SMB is fine, more logos" → new +16% but churned +55%
stakes   SMB reply 6.1→13.9 h, NPS 41→29; last deck forgotten

  2 │    the 2 calls the room must make, each argued both ways     ◀
  1 │    why Q3 moved: SMB losses track support slowdown + actions
  0 ┷    floor: 8 slides, every figure recomputed from the CSV

deeper   monthly rows not averages; logo bridge new→churned→net
wider    finance: logo bridge · ops: queue load · skeptic: causation
target   0 deck figures off the CSV; both calls decided Thursday
judge    check_figures.py rederives every number, tier 1; rubric
         proxy (fresh subagent), tier 4; the meeting itself, tier 2
access   ✓ python3 python-pptx soffice · ✗ customer base, exit reasons
cost     floor ~25 min · rung 2 ~45 min, ~3× tokens · you ~15 min
── reply: go (rung 2) · go 1 · go 0 (floor only) ───────────────────
```

```text
Build the Customer section (~8 slides, .pptx) of Acme's Q3 2026 QBR from data/q3_metrics.csv (monthly new, churned, MRR, NPS, tickets and first-response hours for smb, mid_market and enterprise, Apr–Sep). The headline is that SMB added a record 733 logos in Q3 (+16% vs Q2) but churned 283 (+55%), so net adds were flat at 450, while first response rose from 6.1 h to 13.9 h and NPS fell from 41 to 29. Sales believes SMB is "fine". Present that as a trend and not a proven cause, since there are only 6 months and no customer-base totals, so no churn rate. Structure the section around two decisions the execs must make, each argued for and against using only this data. Before building, write a script that independently recomputes every number in the deck text and chart data from the CSV, show that it fails on a planted wrong figure, and get it to report 0 mismatches. Deliver the plain, finished slides first, render them to PDF and check every page, and list anything you couldn't confirm, with numbers, instead of guessing.
```

Taking rung 2 (`--go`).
