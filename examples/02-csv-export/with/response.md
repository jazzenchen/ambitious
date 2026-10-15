I added a "Download CSV" button to the orders dashboard. The file it produces opens cleanly in Excel: names with commas, quotes, line breaks or accents stay intact, and cells that start with "=" are stored as text instead of running as formulas. The check passes 3 of 3 tests on the new code and failed all 3 on a naive comma-join. I haven't type-checked or run `Dashboard.tsx` itself, because the file it imports (`useOrders.ts`) isn't in the repo.

```text
── /ambitious · result ─────────────────────────────────────────────
floor    ✓ Download CSV button, 4 columns · src/Dashboard.tsx
rung 1   ✓ quoting, formula guard, BOM, CRLF · src/toCsv.ts
target   0 altered cells in 12 hostile rows (was: parser crash)    ✓
judge    cd src && node --test toCsv.test.ts → ℹ fail 0
doubt    "export the table" → untested · Stripe needs date + charge ID
untested button not run in a browser; Dashboard.tsx not type-checked
files    + src/toCsv.ts · + src/toCsv.test.ts · ~ Dashboard.tsx
cost     ~8 steps vs est. · ~10 min · tokens not visible
next     add useOrders.ts / Order type to see if date + Stripe ID exist
────────────────────────────────────────────────────────────────────
```

- **The check:** it parses the output back and compares all 48 cells with the input. Cells that start with `= + - @`, a tab or a carriage return must come back with a leading `'`. Numbers skip that prefix, so a negative total like `-12.5` stays a number.
- **Type check:** `toCsv.ts` passes a strict `tsc` check.
- **No commits:** nothing is committed and no dependencies were added.
- **To go further:** reconciling with Stripe needs an order date and a Stripe charge ID in each row, and the table shows neither. If the `Order` type has those fields, adding them as columns is a short follow-up.