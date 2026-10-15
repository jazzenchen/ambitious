I've added the Export CSV button, and the check passes: Python's CSV reader read back all 10,000 randomly generated rows with 0 differences and no cell that Excel would run as a formula. I haven't run the button in a browser. The repo has no `package.json`, and `src/useOrders.ts`, which the dashboard imports, isn't in the repo.

```text
── /ambitious · result ─────────────────────────────────────────────
floor    ✓ Export CSV button · src/Dashboard.tsx, src/exportCsv.ts
rung 1   ✓ RFC 4180 quoting, CRLF, UTF-8 BOM, formula guard
rung 2   ✗ not attempted · no date/Stripe ID in rows; API not in repo
target   0 diffs, 0 live formulas / 10,000 rows (was no exporter) ✓
judge    run.sh src/exportCsv.ts → rows=10000 cell_diffs=0
         live_formulas=0 total_tieout=ok other=none
doubt    "copy the table" → held · Dashboard.tsx has 4 cols, no date
untested button click in a browser; Dashboard.tsx not type-checked
files    +src/exportCsv.ts · Dashboard.tsx button · no new deps
cost     4 judge runs, ~10 steps vs est. ~25 min · tokens not visible
next     share the orders API schema to add date + Stripe charge ID
────────────────────────────────────────────────────────────────────
```

- **Proof the check catches problems:** I first ran it against a simple comma-joined exporter. That version produced 26,279 cell differences, 4,336 live formulas, totals that didn't add up and no BOM. The check is the same for both runs.
- **Formula guard:** if a text cell starts with `= + - @`, a tab or a carriage return, the file prefixes it with `'`. A customer named `=HYPERLINK(...)` shows up in Excel as text. Number cells are left alone, so negative refund totals stay numbers.
- **Type check:** `src/exportCsv.ts` passes `tsc --strict`. I couldn't type-check `Dashboard.tsx` because `useOrders` and the React types aren't available here.
- **Check files:** they're in `<scratchpad>/judge/` (`run.sh`, `gen.mjs`, `check.py`), outside the project. To keep this as a permanent test I'd need to add a test runner and a `package.json`; say if you want that.
- **To confirm:**
  - Whether `total` is in dollars or cents. The file writes it exactly as received.
  - Whether `orders` holds every order or only the current page. The button exports exactly what the table shows.

Nothing is committed.