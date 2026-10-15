`[tool] Bash: {"command": "git ls-files | head -100; echo ---; git log --stat -3 | head -60", "description": "List tracked files and recent history"}`

`[tool] Read: {"file_path": "<project>/src/Dashboard.tsx"}`

`[tool] Read: {"file_path": "<project>/FEEDBACK.md"}`

`[tool] Bash: {"command": "command -v node npm npx tsc python3 duckdb sqlite3 gh git; gh auth status 2>&1 | head -5; python3 -c \"import os,re;print(*sorted(k for k in os.environ if re.search('token|key|secret|dsn',k,re.I)))\"; ls -la; ls .claude", "description": "Inventory CLIs, gh auth, credential names, layout`

Users are already rebuilding this table by hand every week (37 support tickets this month), and the CSV will be opened in Excel by an accountant. Rung 1 builds the button so customer names containing commas, quotes or a leading "=" can't break the file or run as formulas, and a script that tries to break it checks the result.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    add CSV export button to orders dashboard (Dashboard.tsx)
found    37 export tickets this month; 3 quotes: Excel, Stripe, Sheets
doubt    "a button is enough" → rows have no date or charge ID
stakes   weekly hand-copying; Excel runs a name starting with "="
           as a formula

  3 ▲    end the Monday copy: weekly CSV auto-sent; tickets 37→<5
  2 │    reconcile-ready: date-range export + Stripe charge ID/row
  1 │    safe on bad input: quotes, newlines, =formulas, UTF-8 BOM ◀
  0 ┷    floor: button saves visible rows; re-parses to same cells

deeper   RFC 4180 quoting + OWASP CSV-injection guard, fuzzed rows
wider    accounting: file the books import · security: injection
           · fuzzing: hostile customer names
target   0 bad cells, 0 live formulas in 500 fuzzed rows (no export)
judge    node writes CSV, python csv re-parses + diffs; tier 1
access   ✓ node tsc python3 gh · ~ useOrders.ts (you add) → 2
           · ✗ Stripe, mail/Sheets → 3
cost     floor ~10 min · rung 1 ~25 min, ~2× tokens · you ~5 min
── reply: go (rung 1) · go 2 · go 0 (floor only) ───────────────────
```

```text
Add an "Export CSV" button to src/Dashboard.tsx that downloads the orders currently shown in the table (columns ID, Customer, Total, Status), with the CSV-building logic in its own pure module, e.g. src/ordersCsv.ts. The users asking for this (37 support tickets this month) paste the file into Excel for an accountant, reconcile it against Stripe payouts, or rebuild it in Google Sheets. So the file must survive hostile customer names. Quote fields per RFC 4180 (commas, double quotes, CR/LF), neutralise cells that start with =, +, -, @, tab or CR per OWASP CSV-injection guidance, and prefix a UTF-8 BOM so Excel shows accented names correctly. Before writing the exporter, write a judge script: generate 500 fuzzed order rows, build the CSV, re-parse it with Python's csv module, and report the count of cells that don't match the input and the count of cells Excel would run as formulas. Prove the judge fails on a naive rows.join(",") implementation, then deliver the plain button first and harden it until both counts are 0. Note that src/useOrders.ts is missing from the repo and that orders have no date or payment ID field, so date-range and Stripe-reconciliation exports aren't possible yet. Report any remaining failures with the judge's actual numbers.
```