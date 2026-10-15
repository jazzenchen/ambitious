# Example 2 — Add a CSV export button

**Plain Claude and /ambitious v3.2 wrote equally correct CSV files: in a hidden 500-row stress test, both had 0 wrong cells and 0 cells that would run as a formula, out of 2,000. All 3 blind judges still preferred v3.2, by small margins and mostly for reasons other than correctness: the export logic sits in its own small file, the existing table is left alone, and two small edge cases are handled a little more carefully. v3.2 cost about 3 times as much ($0.64 against $0.21) and took about 4 times as long (147 seconds against 36).**

## The starting point

The project is a small stand-in for the orders page of a web app. Its "repo" (short for repository, the project's folder of code) has two files:

- [`src/Dashboard.tsx`](../../evals/fixtures/csv-export/src/Dashboard.tsx) is an 18-line React component: one piece of a web page, written in TypeScript (JavaScript with type labels). It shows a table of orders with four columns: ID, Customer, Total and Status. It loads the orders from a file called `useOrders`, which is **not** in the repo, so neither run could build or open the page.
- [`FEEDBACK.md`](../../evals/fixtures/csv-export/FEEDBACK.md) holds support notes: 37 tickets this month mentioned export. It has three sample quotes, for example "I copy the table into Excel every Monday to send to our accountant".

The request was to add a button that downloads the table as a CSV file.

**Words used on this page.**
- A **CSV** file (comma-separated values) is plain text, one line per row, with commas between the values. Excel and Google Sheets open it as a spreadsheet.
- **RFC 4180** is the written standard for CSV. A value that contains a comma, a quote or a line break goes inside double quotes, and any quote inside it is doubled. Skip this, and "Acme, Inc." lands in two columns.
- A **BOM** (byte order mark) is an invisible character at the start of the file. It tells Excel the text is UTF-8 (the common way to store text in any alphabet), so names like "Zoë Müller" display correctly.
- **CRLF** is the two-character line ending that the standard asks for: a carriage return followed by a line feed, written `\r\n`. It is the line ending Windows uses.
- A **pure function** only turns input into output (here, rows into CSV text). It doesn't click, download or change anything, so a test can call it directly.
- A **fuzz test** throws large amounts of random, awkward input at code to find the cases that break it.

**The trap in this task is CSV formula injection.** A spreadsheet treats a cell that starts with `=` as a formula, and `+`, `-` and `@` can start one too. Customers type their own names. Say someone signs up as `=HYPERLINK("http://x","y")`. A naive export copies that text into the file. When the accountant opens it in Excel, the cell becomes a live link to an address the customer chose, with a label the customer chose. Other formulas can fetch data from the web.

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

This page compares the current skill, v3.2, with plain Claude. The plain-Claude run is the same one that the earlier version, v3.1, was compared with. Only the skill run was redone, and the hidden checks and blind judges were then run again on the new pair. The v3.1 result is summarised in [Earlier version (v3.1)](#earlier-version-v31) at the end.

## Without /ambitious (plain Claude)

Plain Claude read the two files and rewrote `Dashboard.tsx`. It added an **Export CSV** button that is greyed out when there are no orders, plus two small helper functions inside the same file. The download is named with the day's date (`orders-2026-10-15.csv` in the hidden checks below). It also made the table headers come from the same column list as the export, so the headers and the file's columns can't drift apart. The table's cells are still written out by hand, so that part could still drift, as all three judges pointed out. It added no tests. It said it hadn't compiled or run the code, because the repo has no `package.json` (the file that sets up a JavaScript project) and no `useOrders` file. The run took 35.6 seconds and cost $0.21.

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

It also raised a point about what the file covers:

> The export only includes the orders currently loaded on the page. If `useOrders` loads one page at a time, the export would need its own server endpoint to cover everything, which matters for the people reconciling against Stripe payouts.

In other words, the button can only save what the browser already has. If the app loads orders one page at a time, the file would hold only the current page, and a complete export would need the server to build the file itself. Nothing in the repo shows how `useOrders` loads data, so this stays an open question. The v3.2 run listed the same question in its "to confirm" notes, more briefly. The v3.1 run didn't raise it.

## With /ambitious v3.2

The skill first printed one plain-English lead and a card. The card is the skill's one-screen plan. Its core is a ladder of "rungs", each a more ambitious version of the task. The bottom rung, the "floor", is the request itself done properly, and each rung above it needs a check that could prove it worked. Both the lead and the card are in [card.md](with/card.md), copied verbatim from the run (its full transcript isn't published because it contains local file paths). The lead:

> People want this export so they can send orders to an accountant and match them against Stripe payouts. The table has no date or Stripe ID, though, and a plain CSV can make a customer name run as a live Excel formula. Rung 1 adds the button with safe quoting, and Python's own CSV reader checks it by reading back 10,000 random rows.

The card:

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

**What the card is saying**

- **asked:** the request, slightly shortened.
- **found:** 37 export tickets a month, from line 1 of `FEEDBACK.md`, and the fact that `useOrders.ts`, which the page needs, is missing.
- **doubt:** the request assumes copying the table is enough. Line 9 of `Dashboard.tsx` is the table's header row: four columns, with no order date and no Stripe ID. Stripe is the payment service. Matching orders against Stripe payouts (the batches of money Stripe sends to the company's bank) is a "tie-out", accounting's word for checking two records line by line. It needs an order date and an ID that Stripe also knows, such as the charge ID Stripe gives each payment.
- **stakes:** people redo this table by hand every week. Two of the three quotes say so: one copies it into Excel every Monday, one rebuilds it in Google Sheets weekly. A naive CSV (values just joined with commas) lets a name that starts with `=` run in Excel. This is a risk, not damage already done, because there was no export before.
- **rung 3:** the Monday export reaches the accountant already matched against Stripe. That needs Stripe access the run didn't have.
- **rung 2:** add date, currency and Stripe charge ID columns from the orders API (the server the page gets its data from). That needs a description of what the API returns, which the user would have to supply.
- **rung 1 ◀ (recommended):** a CSV that is safe to open in Excel: standard quoting and the formula guard, proved with a fuzz test.
- **floor:** what was asked, done properly: a button that saves the rows shown, with totals that still match when the file is read back. The skill's rules say to deliver the floor first, so the worst case is what was asked. In this run the floor was not built on its own; it arrived together with rung 1.
- **deeper:** the instruments a careful practitioner would use. Python's built-in CSV reader acts as an "outside" reader: other people wrote it, so a mistake in the new code can't hide by being repeated in the check. OWASP's list of injection attacks supplies the nasty test values.
- **wider:** methods from other trades. From ETL (extract, transform, load: the trade of moving data between systems), check that data survives a round trip. From bookkeeping, check that the totals still add up. From an attacker, try names like `=cmd|...` that try to make Excel start a program.
- **target:** read the file back and get 0 differences across 10,000 random rows, with 0 live formulas. "Not measured" means no number existed yet, because no export existed.
- **judge:** Node.js (which runs JavaScript) writes the file, and Python's CSV reader reads it back and lists the differences. "Tier 1" is the strongest of the skill's four kinds of judge, a check that runs and returns a number. "Fails now" means the check has to fail on the repo as it is, before anyone trusts it to pass the new code.
- **access:** ✓ means reachable now: `node` and `python3`. ~ means one step away: the user could share the API's description, which would make rung 2 possible. ✗ means out of reach: Stripe, so no rung 3.
- **cost:** its own estimate: about 10 minutes for the floor, about 25 minutes and twice the tokens (units of model text) for rung 1, and about 5 minutes of the user's time.

Under the card, the skill also printed a reusable prompt. The skill writes it to work when pasted into any model or tool that hasn't seen this conversation:

<details><summary>The prompt block, verbatim</summary>

```text
Add a CSV export button to src/Dashboard.tsx that downloads the orders it shows (ID, Customer, Total, Status). Support has logged 37 export tickets this month (FEEDBACK.md), and users say they open the file in Excel for an accountant or check it against Stripe payouts. So the file must open cleanly in Excel: RFC 4180 quoting with CRLF line endings, a UTF-8 BOM, and OWASP CSV-injection protection, meaning any text cell that starts with = + - @ tab or CR gets a leading apostrophe. Put the CSV logic in a pure function. Before writing it, write a check: node generates 10,000 random rows full of commas, quotes, newlines, unicode and formula payloads, Python's csv module reads the output back, and the check reports cell differences, live formulas and whether the totals still add up. Show that it fails against a naive comma-join version. The goal is 0 differences and 0 live formulas. Get the button working first, and report every miss with its numbers. Also note that the rows have no order date or Stripe ID, which the accountant and reconciliation workflows both need.
```

</details>

**What it did after `--go`.** It wrote "Taking rung 1 (`--go`)." Its final reply ([response.md](with/response.md)) describes the rest:

1. **Built the check outside the project.** Three files (`run.sh`, `gen.mjs` and `check.py`) went into the run's scratch directory (a temporary working folder), not the repo, so they aren't published here. Following the prompt above, Node generates 10,000 random rows, and Python reads the file back and reports differences, live formulas and whether the totals still add up.
2. **Proved the check can fail.** In the reply's words: "I first ran it against a simple comma-joined exporter. That version produced 26,279 cell differences, 4,336 live formulas, totals that didn't add up and no BOM."
3. **Wrote the export logic** in a new 26-line file, [`exportCsv.ts`](with/files/src/exportCsv.ts). Its main function, `toCsv`, is pure. A separate `downloadCsv` helper does the download. The formula rule is the same as plain Claude's, except that it guards only values that are text, where plain Claude guards anything that isn't a number. With order data made of text and numbers, the two rules act the same. One addition: it also quotes any value that starts or ends with a space, which plain Claude's code doesn't.
4. **Added the button** to [`Dashboard.tsx`](with/files/src/Dashboard.tsx): 13 added lines and no other changes. It has the same label as plain Claude's ("Export CSV"), is greyed out when there are no orders, and uses the same dated filename. The existing table is untouched.
5. **Ran the check** (4 runs in all, by its own count). The result card quotes its output: `rows=10000 cell_diffs=0 live_formulas=0 total_tieout=ok other=none`.
6. **Type-checked `exportCsv.ts`** with `tsc --strict`, the TypeScript compiler in its strictest mode. It could not check `Dashboard.tsx`, because `useOrders` and React's type definitions weren't available.

The reply opens: "I've added the Export CSV button, and the check passes: Python's CSV reader read back all 10,000 randomly generated rows with 0 differences and no cell that Excel would run as a formula." Then it printed this result card:

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

In short, the floor and rung 1 are done and the target was hit on its own 10,000 rows. Rung 2 is marked ✗ with the reason, and the card lists what nothing checked.

A few things to read with care:
- **The check is not in the repo.** v3.2 has a new rule: "Keep judge scripts, floor copies and other scaffolding out of the deliverable". The repo has no test runner (the tool that runs a project's saved tests), and the run kept its check in a scratch directory. It offered: "To keep this as a permanent test I'd need to add a test runner and a `package.json`; say if you want that." The upside is a small, clean change. The downside is that anyone who edits this code later has nothing to rerun unless they say yes.
- **The doubt line says "held", which is hard to read.** Its evidence (four columns, no date) is the same fact the card started from. Nobody checked whether the accountant or the Stripe match actually needs a date. v3.1 marked the same doubt "untested", which was more accurate.
- **It listed two facts it couldn't check, under "To confirm":** "Whether `total` is in dollars or cents. The file writes it exactly as received." and "Whether `orders` holds every order or only the current page. The button exports exactly what the table shows."
- **Its own estimates were off.** The card estimated about 25 minutes for rung 1, and the run took 147.3 seconds. It estimated about 2× the tokens of the floor. The floor was never run on its own, but against plain Claude's run it used 466,917 tokens to 192,077, about 2.4×.

## What the hidden checks found

Neither run saw these checks. A separate tester (also a model) applied one method to both runs' code, working on copies. It added the same stand-in for the missing `useOrders` file and a minimal stand-in for React, and both runs passed a strict type check. It then generated 500 order rows from a fixed random seed (a set starting number for the random generator, so the same rows come out every time), so both runs got identical input. The rows were full of awkward values:
- customer names with commas, quotes, line breaks, tabs, accents, Chinese/Japanese/Korean, Cyrillic, Arabic and Devanagari text, and emoji
- names starting with formula characters, including `=HYPERLINK` and DDE attacks (formulas that try to make Excel start another program), plus 27 with a space or line break before the `=`, `+` or `@`
- IDs that all contain spaces: at the start, at the end, doubled, or non-breaking spaces
- totals including 272 negative numbers, very small and very large numbers, and zero

The tester loaded each page in a simulation, checked that the button was greyed out with 0 orders and active with 500, then pressed it and captured the exact file it downloaded. It read the file back with Python's strict CSV reader and compared all 2,000 cells (500 rows × 4 columns) with what the table shows. To make sure this check could tell good from bad, it also ran it on two deliberately broken exports. A CSV with no quoting gave 1,980 wrong cells, 114 extra rows and 162 live formulas. A correctly quoted CSV with no formula guard gave 165 live formulas.

| What was checked | Plain Claude | /ambitious v3.2 |
|---|---|---|
| Button works, greyed out with 0 orders | yes | yes |
| Label and file name | "Export CSV", `orders-2026-10-15.csv` | the same |
| Passes a strict type check (with the stand-ins) | yes | yes |
| Cells with the wrong value, after removing the added `'` | 0 of 2,000 | 0 of 2,000 |
| Cells given a `'` (none of them needlessly) | 229 | 229 |
| Cells that would run as a formula | 0 | 0 |
| Rows lost, split or with the wrong number of columns | 0 of 500 | 0 of 500 |
| BOM present | yes | yes |
| Negative numeric totals turned into text | 0 of 272 | 0 of 272 |
| If totals arrive as text: negative ones turned into text | 261 of 261 | 261 of 261 |
| Cells with a space or line break before a formula character, left as they were | 27 | 27 |
| Values with a space at the start or end, left unquoted | 223 | 0 |
| Final line ending | no | yes |
| File size | 26,291 bytes | 26,739 bytes |
| Tests added to the repo | 0 | 0 |
| Files changed, lines | 1 file, +36 / −1 | 2 files, +39 |
| Cost · time · tokens | $0.21 · 35.6 s · 192,077 | $0.64 · 147.3 s · 466,917 |

What the numbers mean:
- **Wrong values: 0 and 0.** Every name, ID and total came back exactly as intended, commas, quotes, line breaks and foreign scripts included.
- **Live formulas: 0 and 0.** Without a formula guard, 165 cells would have run. Both runs neutralised all of them, and neither added a `'` where it wasn't needed.
- **Negative totals: 0 of 272.** Real negative numbers stayed numbers, so the accountant's sums still work.
- **261 text totals.** The tester also tried totals that arrive as text rather than numbers (for example the text `"-12.50"` instead of the number -12.5). Both runs then add the apostrophe, so Excel sees text and leaves those totals out of sums. Nothing in the repo shows which form `useOrders` delivers, so this is a weakness both share.
- **27 cells.** A name with a space or line break before `=`, `+` or `@` was left alone in both. It is only dangerous if the spreadsheet strips leading spaces when it imports.
- **223 unquoted values.** These are mostly IDs, which the tester padded with spaces on purpose. Python's reader keeps the spaces either way, but a program that trims unquoted values would lose them from plain Claude's file. v3.2 quotes them.
- **Final line ending.** The standard allows the file to end with or without one.
- **File size.** The 448-byte difference matches the quote marks around those 223 values (446 bytes) plus the final line ending (2 bytes).
- **Tests: 0 and 0.** Neither run left a test in the repo. v3.2's 10,000-row check stayed outside the repo; only its results appear in the run's reply.

The tester repeated the run with five other seeds and reached the same conclusions each time.

## What the blind judges said

Three model judges each saw both finished repos and their diffs (line-by-line lists of what changed), labelled A and B, with the skill's files removed. Here plain Claude was A and v3.2 was B. They didn't see either run's final reply, so they never saw v3.2's 10,000-row check or plain Claude's note about pages. Each judge read the work through a different lens. Confidence runs from 0 to 1.

| Judge | Preferred | Confidence | Their reason, paraphrased |
|---|---|---|---|
| Busy requester | v3.2 | 0.6 | The two produce almost the same CSV, and either would take about two minutes to review. B quotes padded values, ends the file with a line break, keeps the logic in a separate file that is easy to test and reuse, and leaves the existing table alone. A rewrote the table's header row, which nobody asked for, and only half-way, since the body cells are still written by hand. |
| Senior practitioner | v3.2 | 0.62 | Same behaviour, so it comes down to engineering. B has a pure, general `toCsv` whose column names are checked when the code compiles, a separate download helper and a thin page component. The judge docked B because its column list repeats the table headers, and gave A credit that its header change at least keeps header labels in step with the file. |
| Skeptic | v3.2 | 0.6 | The two are about the same size. A's header change means the header row and the body cells now come from different places, so editing the column list for the export could silently misalign the table on screen. B only adds code. The judge docked B for a general-purpose set of exported functions built for a single use, plus one extra file. |

In their own words:
- Busy requester: "I'd ship B because it is slightly more correct, easier to test and leaves existing markup alone, but the gap is small."
- Senior practitioner: "Behaviour is effectively the same. B wins modestly on structure, testability, reuse and slightly more careful quoting."
- Skeptic: "B carries less risk to code that already existed and is easier to trust without re-checking, so it wins narrowly."

**Why v3.2 won, honestly.**
- **Not on the main correctness measures.** The hidden checks found the same zeros for both, and every judge said the output was the same or nearly so.
- **Not on its extra checking.** The judges never saw the 10,000-row check, so it played no part in the vote.
- **On the shape of the change and two small details in the file.** The logic sits in a separate, testable file, and the existing table is left alone. Plain Claude's half-finished header change was flagged by all three judges and counted against it. v3.2 also quotes padded values and ends the file with a line break.
- **By small margins.** Confidence was 0.6 to 0.62 for each judge. With one run per side and model judges rather than people, 3–0 here is a mild preference, not a clear win.

## Takeaway

Plain Claude already knew the pitfalls here. It handled quoting, the BOM and formula injection without being asked, so v3.2 did not make the file more correct on any of the hidden checks' main measures. The extra cost (about $0.43) and time (about 112 seconds) bought:
- a tidier change, which the judges preferred by small margins
- two small extras the judges counted in its favour: padded values quoted, and a final line ending
- a 10,000-row check by an outside reader, reported with numbers, plus an offer to keep it as a permanent test
- a short "to confirm" list naming the two facts nobody could check

For a one-off button in a well-known pattern, plain Claude gave almost the same file for about a third of the price. Use /ambitious when you want measured evidence before you trust the result, and say yes to keeping the check if the code will change later.

## Earlier version (v3.1)

This task was first run with v3.1, against the same plain-Claude run. v3.2 exists because v3.1 lost on polish elsewhere. A human reviewer found its deck looked worse than plain Claude's, blind judges preferred plain Claude's deck 3–0 and its launch post 2–1, and v3.1 had left `[TK]` placeholders in both. On this task v3.1 had already won, 2–1.

What v3.1 did differently ([response.md](with-v3.1/response.md)):
- It put a test file in the repo, [`toCsv.test.ts`](with-v3.1/files/src/toCsv.test.ts): 82 lines with 3 tests over 12 hostile rows and its own small CSV reader. It ran the test on a naive version first to show it could fail, and the test passed 3 of 3 on the new code.
- Its export logic, [`toCsv.ts`](with-v3.1/files/src/toCsv.ts), was 29 lines and did not quote padded values.
- Its button said "Download CSV" and always saved `orders.csv`.
- It changed 3 files, adding 125 lines, and cost $0.57 for 136.7 seconds and 592,065 tokens.

Its hidden checks used a different tester and a different set of 500 rows. Both runs again had 0 wrong cells and 0 live formulas. The tester's verdict on plain Claude's file was "byte-identical to run B's output except that B adds a final CRLF" (run B was v3.1).

Two judges preferred v3.1. The busy requester (0.6) liked having a passing test to rerun instead of checking by hand, and the senior practitioner (0.7) liked the separate logic and that it was the only run with tests. The skeptic (0.68) preferred plain Claude. It said v3.1 added machinery for a single use and an 82-line test, about 3 times the size of the 29-line code. It added that the test assumes setup the repo doesn't have and partly checks the code against a copy of its own rule. The busy requester and the senior practitioner both still rated plain Claude's dated filename as better for a weekly export.

v3.2 is different on most of those points. It left no test in the repo, used the dated filename and the same label as plain Claude, and kept the change to 39 lines. It also quotes padded values. This time the skeptic lens chose the skill's run too, and the vote went from 2–1 to 3–0. The trade-off: in v3.1, two judges valued a test they could rerun. v3.2 left none, and its judges chose it mainly for its structure instead. v3.2 was written after seeing v3.1's results on these same tasks, so this rerun is not an unseen test.

## Files

- Plain Claude: [prompt.txt](without/prompt.txt) · [response.md](without/response.md) · [files/src/Dashboard.tsx](without/files/src/Dashboard.tsx)
- /ambitious v3.2: [prompt.txt](with/prompt.txt) · [card.md](with/card.md) · [response.md](with/response.md) · [files/src/Dashboard.tsx](with/files/src/Dashboard.tsx) · [files/src/exportCsv.ts](with/files/src/exportCsv.ts)
- /ambitious v3.1: [prompt.txt](with-v3.1/prompt.txt) · [response.md](with-v3.1/response.md) · [files/src/Dashboard.tsx](with-v3.1/files/src/Dashboard.tsx) · [files/src/toCsv.ts](with-v3.1/files/src/toCsv.ts) · [files/src/toCsv.test.ts](with-v3.1/files/src/toCsv.test.ts)
- Starting repo: [FEEDBACK.md](../../evals/fixtures/csv-export/FEEDBACK.md) · [src/Dashboard.tsx](../../evals/fixtures/csv-export/src/Dashboard.tsx)
- Raw eval, plain Claude: [prompt.txt](../../evals/outcomes/results/csv-export/without_skill/prompt.txt) · [response.md](../../evals/outcomes/results/csv-export/without_skill/response.md) · [diff.patch](../../evals/outcomes/results/csv-export/without_skill/diff.patch) · [diffstat.txt](../../evals/outcomes/results/csv-export/without_skill/diffstat.txt) · [timing.json](../../evals/outcomes/results/csv-export/without_skill/timing.json)
- Raw eval, v3.2: [prompt.txt](../../evals/outcomes/results/csv-export/with_skill/prompt.txt) · [response.md](../../evals/outcomes/results/csv-export/with_skill/response.md) · [diff.patch](../../evals/outcomes/results/csv-export/with_skill/diff.patch) · [diffstat.txt](../../evals/outcomes/results/csv-export/with_skill/diffstat.txt) · [timing.json](../../evals/outcomes/results/csv-export/with_skill/timing.json)
- Raw eval, v3.1: [prompt.txt](../../evals/outcomes/results-v3.1/csv-export/with_skill/prompt.txt) · [response.md](../../evals/outcomes/results-v3.1/csv-export/with_skill/response.md) · [diff.patch](../../evals/outcomes/results-v3.1/csv-export/with_skill/diff.patch) · [diffstat.txt](../../evals/outcomes/results-v3.1/csv-export/with_skill/diffstat.txt) · [timing.json](../../evals/outcomes/results-v3.1/csv-export/with_skill/timing.json)
- Measurements and blind verdicts (task `csv-export`): [v3.2](../../evals/outcomes/results/measurements-and-judgments.json) · [v3.1](../../evals/outcomes/results-v3.1/measurements-and-judgments.json) · cost and time for all four tasks: [summary.json](../../evals/outcomes/results/summary.json)
- How the comparison was run: [OUTCOMES.md](../../evals/outcomes/OUTCOMES.md) · [run_outcomes.sh](../../evals/outcomes/run_outcomes.sh) · [make_blind_copies.py](../../evals/outcomes/make_blind_copies.py)
- The skill itself: [SKILL.md](../../skills/ambitious/SKILL.md)
