I added an **Export CSV** button to the orders dashboard in `src/Dashboard.tsx`. Clicking it downloads `orders-YYYY-MM-DD.csv` with the ID, Customer, Total and Status columns, and the button is greyed out when there are no orders. I haven't compiled or run it: the repo has no `package.json` and no `useOrders` file, so there's nothing to build against. One assumption to check is that each order has `id`, `customer`, `total` and `status` fields.

Because `FEEDBACK.md` says most people asking for this open it in Excel or Google Sheets:
- **Accents and non-Latin names show correctly in Excel.** Without this, Excel can garble them when opening the file.
- **Text with commas, quotes or line breaks is quoted**, so a name like `Acme, Inc.` stays in one column.
- **Text that looks like a formula isn't run as one.** Excel and Sheets would otherwise treat a customer name starting with `=`, `+`, `-` or `@` as a formula, so I put a `'` in front of it. That `'` shows up in the cell; it doesn't touch the numbers in the Total column.

The table headers now come from the same column list as the CSV, so the two stay in sync.

The export only includes the orders currently loaded on the page. If `useOrders` loads one page at a time, the export would need its own server endpoint to cover everything, which matters for the people reconciling against Stripe payouts.