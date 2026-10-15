I haven't changed anything yet. Here's what I found and what I'd propose.

## What's in the repo

- `src/Dashboard.tsx` is a bare table with four columns: ID, Customer, Total, Status. There's no filtering, sorting or date range.
- `FEEDBACK.md` says this month had **37 support tickets about export**, and the quotes show what people are trying to do:
  - "I copy the table into Excel **every Monday** to send to our **accountant**"
  - "Need to **reconcile with Stripe payouts**"
  - "Our ops lead **rebuilds this table in Google Sheets weekly**"
- `./useOrders` is imported but isn't in the repo. There's also no `package.json`, no backend and no tests.

None of the three users wants a button for its own sake. Each one is redoing a **weekly report by hand for someone downstream**. A button only saves them the copy-paste step.

## The most ambitious version: "Orders Reports"

**1. Exports that match what's on screen**
- Add date range, status and customer filters to the dashboard. The export then uses exactly the current view, so "last week's paid orders" takes one click.
- Formats: CSV, Excel-friendly CSV (UTF-8 BOM, CRLF, safe against formula injection) and .xlsx.
- Let users pick which columns to include, and add the fields the table doesn't show but accountants need: created/paid dates, currency, tax, fees, net and payment ID.

**2. A Stripe reconciliation preset**
- A report grouped by payout, with gross, fees, refunds and net per payout, and the Stripe charge/payout IDs. This turns "any way to download?" into "it already matches".

**3. Scheduled reports, so nobody has to remember Monday**
- "Email this report to accountant@… every Monday at 8am" using the saved filters.
- Or a live Google Sheets sync that keeps a sheet up to date, so the ops lead stops rebuilding it.

**4. Saved report templates** that the team shares ("Weekly accountant report", "Stripe recon").

**5. Large exports and auditing**
- Big exports are built in the background and the user gets a download link.
- Each export is logged with who ran it, when and which filters, since this is financial data.

## What's realistic here

Parts 1 and 2 (client side) I can build in this repo now. Parts 3–5 need a backend, an email/Sheets integration and auth, and none of those exist in this repo. For those I'd write the frontend and an API contract, not working code.

**My recommendation:** build **filters + export of the current view (CSV/Excel-safe CSV) + column picker + the extra accounting fields**. That covers all three complaints, and it doesn't box in scheduled reports later. For parts 3–5 I'd write a short spec.

Two things I need from you first:
1. Where does `useOrders` come from, and does the data include dates, currency, fees and Stripe IDs? If not, the Stripe preset needs backend work.
2. Go with the recommended scope, the full version (with stubs for the backend parts), or just the plain button?