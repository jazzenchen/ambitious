The checkout test is fixed and passed 1,000 out of 1,000 runs, compared with 65 failures in 200 runs before. It was never really a flaky test. `checkout()` returned before stock was reserved, so an order for a sold-out item still got an order ID, and the test's 25 ms wait only sometimes covered the 0–40 ms simulated delay. Now checkout waits for every item, rejects the order if anything is out of stock, and puts back stock it had already reserved for that order.

```text
── /ambitious · result ─────────────────────────────────────────────
floor    ✓ sleep removed; test awaits real result · test/checkout.test.js
rung 1   ✓ checkout awaits all; sold-out rejects; held stock released
target   0/1000 failed vs 0/1000 (was 65/200, measured)            ✓
judge    node stress.mjs judge.test.js 1000 → stress: 0/1000 failed
judge    same loop on test/checkout.test.js → stress: 0/1000 failed
doubt    "the test is flaky" → refuted · 3/4 judge tests failed on old
untested past orders with sold-out items: no order data here
untested oversell under concurrent carts was trivial before the fix
files    checkout.js · inventory.js +release() · 2 new tests · no deps
cost     2,200 runs, ~25 min wall vs ~25 min est. · tokens not visible
next     check order logs since 1.4.2 for orders with sold-out skus
────────────────────────────────────────────────────────────────────
```

- **How checkout works now:** reservations still run in parallel (`src/checkout.js:5`), using `Promise.allSettled`. If any item fails, the items it did reserve are released through the new `release()` in `src/inventory.js`, and the out-of-stock error is passed back to the caller.
- **Callers:** any code that relied on getting an order ID for a sold-out cart will now get an error instead. Nothing in this repo does that.
- **Check the judge yourself:** the stress script and the separate test file are kept outside the project:
  - `<scratchpad>/stress.mjs`
  - `<scratchpad>/judge.test.js`
- **Not committed:** the three modified files are still uncommitted. Say the word if you want a commit on a branch for SHOP-412.