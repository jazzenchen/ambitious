# Example 2 — Add a CSV export button

**Both runs produced the same CSV file (byte for byte, apart from one final line break) and left no cell that a spreadsheet would run as a formula in a 500-row stress test; /ambitious also put the logic in its own file with 3 passing tests, which 2 of 3 blind judges preferred, at about 2.8 times the cost.**

## The starting point

The project is a small stand-in for the orders page of a web app. It has two files:

- [`src/Dashboard.tsx`](../../evals/fixtures/csv-export/src/Dashboard.tsx) is an 18-line React component: one piece of a web page, written in TypeScript (JavaScript with type labels). It shows a table of orders with four columns: ID, Customer, Total and Status. It loads the orders from a file called `useOrders`, which is **not** in the repo, so neither run could build or open the page.
- [`FEEDBACK.md`](../../evals/fixtures/csv-export/FEEDBACK.md) holds support notes: 37 tickets this month mentioned export. It has three sample quotes, for example "I copy the table into Excel every Monday to send to our accountant".

The request was to add a button that downloads the table as a CSV file.

**Words used on this page.**
- A **CSV** file (comma-separated values) is plain text, one line per row, with commas between the values. Excel and Google Sheets open it as a spreadsheet.
- **RFC 4180** is the written standard for CSV. A value that contains a comma, a quote or a line break goes inside double quotes, and any quote inside it is doubled. Skip this, and "Acme, Inc." lands in two columns.
- A **BOM** (byte order mark) is an invisible character at the start of the file. It tells Excel the text is UTF-8 (the common way to store text in any alphabet), so names like "Zoë Müller" display correctly.
- **CRLF** is the two-character line ending that the standard asks for: a carriage return followed by a line feed, written `\r\n`. It is the line ending Windows uses.

**The trap in this task is CSV formula injection.** A spreadsheet treats a cell that starts with `=` as a formula, and `+`, `-` and `@` can start one too. Customers type their own names. Say someone signs up as `=HYPERLINK("http://x","y")`, one of the test rows below. A naive export copies that text into the file. When the accountant opens it in Excel, the cell becomes a live link to an address the customer chose, with a label the customer chose. Other formulas can fetch data from the web.

The usual defence comes from OWASP, a non-profit that publishes web security guidance. It puts an apostrophe `'` in front of such cells so the spreadsheet shows them as plain text. The catch is that a negative total like `-12.5` also starts with `-`. A careless guard turns real numbers into text and breaks the accountant's sums.

## What was typed

Plain Claude:

```text
add a CSV export button to the orders dashboard
```

With the skill:

```text
/ambitious --go add a CSV export button to the orders dashboard
```

`--go` tells the skill to print its card and then start right away on the option it recommends, with nobody there to answer. Both runs used the same model (`claude-opus-5-5`) on a fresh copy of the same repo, with permission to edit files ([how the runs were set up](../../evals/outcomes/OUTCOMES.md)).

## Without /ambitious

Plain Claude read the two files and rewrote `Dashboard.tsx`. It added an **Export CSV** button that is greyed out when there are no orders, plus two small helper functions inside the same file. The download is named with the day's date (`orders-2026-10-15.csv` in the hidden checks below). It also made the table headers come from the same column list as the export, so the headers and the file's columns can't drift apart. The table's cells are still written out by hand, so that part could still drift, as one judge pointed out. It added no tests. It said it hadn't compiled or run the code, because the repo has no `package.json` (the file that sets up a JavaScript project) and no `useOrders` file. The run took 35.6 seconds and cost $0.21.

This is the part that handles quoting and formulas ([full file](without/files/src/Dashboard.tsx)):

```ts
// Quote fields per RFC 4180, and neutralize leading =+-@ so Excel/Sheets
// don't evaluate customer-supplied text as a formula.
function csvField(value: unknown): string {
  let s = value == null ? "" : String(value);
  if (/^[=+\-@\t\r]/.test(s) && typeof value !== "number") s = "'" + s;
  return /[",\r\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}
```

Line by line:
- A missing value becomes an empty cell.
- If the text starts with `=`, `+`, `-`, `@`, a tab or a carriage return, and the value is not a real number, it gets an apostrophe in front.
- If the text contains a quote, comma or line break, it is wrapped in quotes and any inner quotes are doubled.

Its final reply explained this in plain words ([response.md](without/response.md)):

> **Text that looks like a formula isn't run as one.** Excel and Sheets would otherwise treat a customer name starting with `=`, `+`, `-` or `@` as a formula, so I put a `'` in front of it. That `'` shows up in the cell; it doesn't touch the numbers in the Total column.

It also raised a point the /ambitious run did not:

> The export only includes the orders currently loaded on the page. If `useOrders` loads one page at a time, the export would need its own server endpoint to cover everything, which matters for the people reconciling against Stripe payouts.

In other words, the button can only save what the browser already has. If the app loads orders one page at a time, the file would hold only the current page, and a complete export would need the server to build the file itself. Nothing in the repo shows how `useOrders` loads data, so this stays an open question.

## With /ambitious

The skill first printed one plain-English lead and a card. The card is the skill's one-screen plan. Its core is a ladder of "rungs", each a more ambitious version of the task. The bottom rung, the "floor", is the request itself done properly, and each rung above it needs a check that could prove it worked. `response.md` keeps only the final message, so the lead and the card below are copied from the run's transcript, which isn't published because it contains local file paths. The lead:

> The real ask behind this button is the weekly hand-copy into Excel and Stripe. A plain comma-join would break on a name like "Acme, Inc." and would run any cell starting with "=" as a formula in Excel. Rung 1 makes the export safe to open in Excel and proves it with a test that a naive version fails.

The card:

```text
── /ambitious ──────────────────────────────────────────────────────
asked    add a CSV export button to the orders dashboard
found    37 export tickets/mo; all 3 quotes are manual weekly copies
doubt    "export the table" → Stripe tie-out needs date + ID; none shown
stakes   naive CSV splits "Acme, Inc." and runs "=..." cells in Excel

  3 ▲    retire the Monday copy: weekly CSV mailed to the accountant
  2 │    reconciliation-ready: order date + Stripe charge ID columns
  1 │    Excel-safe CSV: RFC 4180 quoting, formula guard, BOM, CRLF ◀
  0 ┷    floor: button downloads the 4 visible columns as orders.csv

deeper   RFC 4180 + OWASP CSV-injection rules, hostile-row fixtures
wider    accounting: tie-out vs Stripe payouts · security: inject =cmd
target   0 altered cells in 12 hostile rows round-tripped (not measured)
judge    node --test src/toCsv.test.ts, tier 1, must fail naive join
access   ✓ node tsc gh · ~ useOrders.ts (you) → 2 · ✗ Stripe, mail → 3
cost     floor ~10 min · rung 1 ~25 min, ~2× tokens · you ~3 min
── reply: go (rung 1) · go 2 · go 0 (floor only) ───────────────────
```

**What the card is saying**

- **asked:** the request, copied as typed.
- **found:** from `FEEDBACK.md`, the 37 export tickets, read as people copying the table by hand every week. Strictly, only two of the three quotes describe a weekly copy. The third asks how to reconcile with Stripe, the payment service.
- **doubt:** the request assumes "export the table" is enough. Matching orders against Stripe payouts (the batches of money Stripe sends to the company's bank) is a "tie-out", accounting's word for checking two records line by line. It needs an order date and an ID that Stripe also knows, such as the charge ID Stripe gives each payment. The table shows neither. The skill flagged this but couldn't check it, because the order data file is missing.
- **stakes:** a naive CSV (values just joined with commas) splits "Acme, Inc." into two columns and lets `=...` cells run in Excel. This is a risk, not damage already done, because there was no export before.
- **rung 3:** stop the Monday copy altogether by mailing a weekly CSV to the accountant. That needs Stripe and email access the run didn't have.
- **rung 2:** add order date and Stripe charge ID columns so the file can be matched against payouts. That needs the order data file, which the user would have to supply.
- **rung 1 ◀ (recommended):** a CSV that is safe to open in Excel: standard quoting, the formula guard, the BOM and CRLF line endings.
- **floor:** what was asked, done properly: a button that downloads the four visible columns as `orders.csv`. The skill's rules say to deliver the floor first, so the worst case is what was asked. In this run the floor was not built on its own; it arrived together with rung 1.
- **deeper:** the instruments a careful practitioner would use here: the CSV standard, OWASP's injection rules, and a set of deliberately nasty test rows.
- **wider:** methods from two other fields. From accounting, matching against Stripe payouts. From security, attacking the file with an `=cmd` name.
- **target:** read the file back and get 0 changed cells across 12 hostile rows. "Not measured" means no number existed yet, because no export existed.
- **judge:** the outside check is a test run with `node --test`, Node.js's built-in test runner. "Tier 1" is the strongest of the skill's four kinds of judge, a check that runs and returns a number. "Must fail naive join" means the test has to catch a naive export before anyone trusts it to approve this one.
- **access:** ✓ means reachable now: `node` runs JavaScript, `tsc` checks TypeScript, and `gh` is GitHub's command-line tool. ~ means one step away: the user could supply `useOrders.ts`, which would make rung 2 possible. ✗ means out of reach: Stripe and email, so no rung 3.
- **cost:** its own estimate: about 10 minutes for the floor, about 25 minutes and twice the tokens (units of model text) for rung 1, and about 3 minutes of the user's time.

Under the card, the skill also printed a reusable prompt. The skill writes it to work when pasted into any model or tool that hasn't seen this conversation:

<details><summary>The prompt block, verbatim</summary>

```text
Add a "Download CSV" button to src/Dashboard.tsx that exports the orders table (ID, Customer, Total, Status) as orders.csv. Support has logged 37 export tickets this month, and users paste this table into Excel or Google Sheets every week. Put the serialisation in a pure function, src/toCsv.ts, that follows RFC 4180: quote fields containing commas, quotes or newlines; double any embedded quotes; use CRLF line endings; and start the file with a UTF-8 BOM so Excel reads non-ASCII names correctly. Apply the OWASP CSV-injection guard to string cells that start with = + - @ tab or CR, but leave numbers alone so negative totals stay numeric. Before writing the function, write a node --test file with at least 12 hostile rows that parses the output back and asserts every cell round-trips. Run it against a naive comma-join first to prove it fails. Ship the plain button first, then the hardening, and report any cell that still fails with its input.
```

</details>

**What it did after `--go`.** It wrote "Taking rung 1 (`--go`): it's the recommended rung, and node can run its check now." Then:

1. **Wrote the judge first.** [`toCsv.test.ts`](with/files/src/toCsv.test.ts) holds 12 hostile rows (test data built to break a CSV export) and a small CSV reader of its own. Four of the rows:
   ```ts
     { id: 1, customer: "Acme, Inc.", total: 120.5, status: "paid" },
     { id: 5, customer: "=HYPERLINK(\"http://x\",\"y\")", total: 1, status: "paid" },
     { id: 7, customer: "-2+3", total: 3, status: "refunded" },
     { id: 10, customer: "Zoë Müller 東京", total: -12.5, status: "refunded" },
   ```
2. **Proved the judge can fail.** It ran the test against a naive comma-join version first. The test's reader crashed on a line break outside quotes, which the result card records as "was: parser crash".
3. **Wrote the real code** in [`toCsv.ts`](with/files/src/toCsv.ts). Its main function, `toCsv`, is pure: it only turns rows into text and never clicks or downloads anything, so a test can call it directly. The same file holds a separate `downloadCsv` helper that does the download. The test then passed 3 of 3. The formula rule is the same as plain Claude's, except it guards only values that are text, where plain Claude guards anything that isn't a number. The hidden tester found this difference "only in theory".
4. **Added the button** ("Download CSV", greyed out with no orders) to [`Dashboard.tsx`](with/files/src/Dashboard.tsx). The download is always named `orders.csv`.
5. **Type-checked `toCsv.ts`** with `tsc`, the TypeScript compiler. It did not check `Dashboard.tsx`, which can't compile without `useOrders.ts`.

The run took 136.7 seconds and cost $0.57. Its final reply ([response.md](with/response.md)) says: "The check passes 3 of 3 tests on the new code and failed all 3 on a naive comma-join." Then it printed this result card:

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

In short, the floor and rung 1 are done, the target was hit on its own 12 rows, and the Stripe doubt was left untested. It also lists what nothing checked. Two of its own figures were off:
- The card estimated about 25 minutes and the result card says about 10. The measured time was 136.7 seconds.
- The card estimated about 2× the tokens of the floor. The floor was never run on its own, but against plain Claude's run it used 592,065 tokens to 192,077, about 3.1×.

## What the hidden checks found

Neither run saw these checks. A separate tester (also a model) took each run's code and added the same stand-in for the missing `useOrders` file. It then generated 500 order rows from a fixed random seed (a set starting number for the random generator, so the same rows come out every time), so both runs got identical input. The rows were full of awkward values:
- 219 customer names starting with formula characters (including `=HYPERLINK`, `=IMPORTXML` and `=cmd|...`)
- 160 names with commas, 143 with quotes and 138 with line breaks
- emoji, Chinese/Japanese/Korean and Arabic text, and empty and missing names
- awkward IDs and totals as well

The tester pressed each button in a simulated page and captured the exact file it downloaded. It read the file back with Python's strict CSV reader and compared all 2,000 cells (500 rows × 4 columns) with what was intended.

| What was checked | Plain Claude | With /ambitious |
|---|---|---|
| Button works, greyed out with 0 orders | yes ("Export CSV") | yes ("Download CSV") |
| Cells with the wrong value, after removing the added `'` | 0 of 2,000 | 0 of 2,000 |
| Cells that would run as a formula (208 input values would have) | 0 | 0 |
| Rows lost, split or with the wrong number of columns | 0 of 500 | 0 of 500 |
| Negative numeric totals turned into text | 0 of 201 | 0 of 201 |
| Totals sent as text, like `"-12.50"` or `"+5.00"`, that got a `'` | 49 | 49 |
| Cells with a space or line break before `=`, left as they were | 19 | 19 |
| BOM present | yes | yes |
| Final line ending | no | yes |
| Tests added | 0 | 3 (3 pass, 0 fail) |
| Files changed, lines added | 1 file, +36 / −1 | 3 files, +125 |
| Cost · time · tokens | $0.21 · 35.6 s · 192,077 | $0.57 · 136.7 s · 592,065 |

What the numbers mean:
- **Wrong values: 0 and 0.** Every name, ID and total came back exactly as intended, commas, quotes, line breaks and foreign scripts included.
- **Live formulas: 0 and 0.** Of the 2,000 intended values, 208 would have run as formulas if written unchanged. Both runs neutralised all of them.
- **Negative totals: 0 of 201.** Real negative numbers stayed numbers, so the accountant's sums still work.
- **49 text totals.** When a total arrives as text rather than a number (for example the text `"-12.50"` instead of the number -12.5), both runs added the apostrophe, so Excel sees text, not a number, and leaves it out of sums. This is a weakness both share.
- **19 cells.** A name with a space or line break before `=` was left alone in both. It is only dangerous if the spreadsheet strips leading spaces when it imports.
- **Final line ending.** This is the only difference between the two files: the /ambitious file ends with one more CRLF, two extra bytes (28,022 bytes against 28,020). The tester's verdict on plain Claude's file was "byte-identical to run B's output except that B adds a final CRLF" (run B is /ambitious). The standard allows either.

The tester also ran the /ambitious run's own test file: 3 pass, 0 fail.

## What the blind judges said

Three model judges each saw both finished repos labelled A and B, with the skill's files removed. Here plain Claude was A and /ambitious was B. Each judge read the work through a different lens. Confidence runs from 0 to 1.

| Judge | Preferred | Confidence | Their reason, paraphrased |
|---|---|---|---|
| Busy requester | /ambitious | 0.6 | The files are identical apart from B's final line break, so the deciding factor is how quickly you can trust each one. B comes with a passing test you can rerun, while A needs a hand check, such as exporting a `=HYPERLINK` customer and opening it in Excel. |
| Senior practitioner | /ambitious | 0.7 | With identical behaviour, B wins on engineering. It separates the tricky escaping logic from the download code and is the only one with tests that prove its claims. The judge docked it for the fixed filename and for a test file that assumes setup the repo doesn't have. |
| Skeptic | plain Claude | 0.68 | A gives the same result in one file and about 35 lines. B adds machinery for a single use and an 82-line test, about 3 times the 29-line code. That test could break a typical project's type check, and part of it checks the code against a copy of the code's own rule. |

Two judges liked plain Claude's dated filename better for a weekly export. Keep in mind that this is one run per side, with model judges rather than people.

## Takeaway

Plain Claude already knew the pitfalls here: it handled quoting, the BOM and formula injection without being asked, so /ambitious did not make the file more correct. The extra cost ($0.57 instead of $0.21, and 137 seconds instead of 36) bought proof: a test that fails on a naive export and passes on this one, plus the logic in a file that test can reach.

Use /ambitious on code that people will change later, or when you need to trust the result without reading it line by line. For a one-off button in a well-known pattern, plain Claude gave the same file, minus one final line break, for about a third of the price.

## Files

- Without /ambitious: [prompt.txt](without/prompt.txt) · [response.md](without/response.md) · [files/src/Dashboard.tsx](without/files/src/Dashboard.tsx)
- With /ambitious: [prompt.txt](with/prompt.txt) · [response.md](with/response.md) · [files/src/Dashboard.tsx](with/files/src/Dashboard.tsx) · [files/src/toCsv.ts](with/files/src/toCsv.ts) · [files/src/toCsv.test.ts](with/files/src/toCsv.test.ts)
- Starting repo: [FEEDBACK.md](../../evals/fixtures/csv-export/FEEDBACK.md) · [src/Dashboard.tsx](../../evals/fixtures/csv-export/src/Dashboard.tsx)
- Raw eval, plain Claude: [prompt.txt](../../evals/outcomes/results/csv-export/without_skill/prompt.txt) · [response.md](../../evals/outcomes/results/csv-export/without_skill/response.md) · [diff.patch](../../evals/outcomes/results/csv-export/without_skill/diff.patch) · [diffstat.txt](../../evals/outcomes/results/csv-export/without_skill/diffstat.txt) · [timing.json](../../evals/outcomes/results/csv-export/without_skill/timing.json)
- Raw eval, /ambitious: [prompt.txt](../../evals/outcomes/results/csv-export/with_skill/prompt.txt) · [response.md](../../evals/outcomes/results/csv-export/with_skill/response.md) · [diff.patch](../../evals/outcomes/results/csv-export/with_skill/diff.patch) · [diffstat.txt](../../evals/outcomes/results/csv-export/with_skill/diffstat.txt) · [timing.json](../../evals/outcomes/results/csv-export/with_skill/timing.json)
- Measurements and blind verdicts (task `csv-export`): [measurements-and-judgments.json](../../evals/outcomes/results/measurements-and-judgments.json)
- How the comparison was run: [OUTCOMES.md](../../evals/outcomes/OUTCOMES.md) · [run_outcomes.sh](../../evals/outcomes/run_outcomes.sh)
- The skill itself: [SKILL.md](../../skills/ambitious/SKILL.md)
