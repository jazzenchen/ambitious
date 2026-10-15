# The card /ambitious printed before doing any work (verbatim from the run)

People want this export so they can send orders to an accountant and match them against Stripe payouts. The table has no date or Stripe ID, though, and a plain CSV can make a customer name run as a live Excel formula. Rung 1 adds the button with safe quoting, and Python's own CSV reader checks it by reading back 10,000 random rows.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    CSV export button on the orders dashboard
found    37 export tickets/mo (FEEDBACK.md:1); useOrders.ts missing
doubt    "copy the table" → no date or Stripe ID (Dashboard.tsx:9)
stakes   staff re-key it weekly; a naive CSV runs "=..." names in Excel

  3 ▲    Monday export reaches the accountant, tied out to Stripe
  2 │    add date, currency, Stripe charge ID columns from the API
  1 │    Excel-safe: RFC 4180 quoting, formula guard, fuzz-tested    ◀
  0 ┷    floor: button saves the shown rows; totals match on re-read

deeper   Python csv as outside parser; OWASP CSV-injection payloads
wider    ETL: round-trip · books: sum tie-out · attacker: =cmd cells
target   0 diffs in 10k fuzzed rows, 0 live formulas (not measured)
judge    node writes, python3 csv re-reads + diffs; tier 1; fails now
access   ✓ node python3 · ~ API schema (you) → rung 2 · ✗ Stripe → 3
cost     floor ~10 min · rung 1 ~25 min, ~2× tokens · you ~5 min
── reply: go (rung 1) · go 2 · go 0 (floor only) ───────────────────
```

```text
Add a CSV export button to src/Dashboard.tsx that downloads the orders it shows (ID, Customer, Total, Status). Support has logged 37 export tickets this month (FEEDBACK.md), and users say they open the file in Excel for an accountant or check it against Stripe payouts. So the file must open cleanly in Excel: RFC 4180 quoting with CRLF line endings, a UTF-8 BOM, and OWASP CSV-injection protection, meaning any text cell that starts with = + - @ tab or CR gets a leading apostrophe. Put the CSV logic in a pure function. Before writing it, write a check: node generates 10,000 random rows full of commas, quotes, newlines, unicode and formula payloads, Python's csv module reads the output back, and the check reports cell differences, live formulas and whether the totals still add up. Show that it fails against a naive comma-join version. The goal is 0 differences and 0 live formulas. Get the button working first, and report every miss with its numbers. Also note that the rows have no order date or Stripe ID, which the accountant and reconciliation workflows both need.
```

Taking rung 1 (`--go`).
