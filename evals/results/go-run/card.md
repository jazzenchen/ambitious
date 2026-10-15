Checkout isn't waiting for stock to be reserved, so the test only fails when the fake network is slow (about 3 runs in 8). The same bug also lets people order sold-out items. I'm taking rung 1: it fixes both and proves the fix with a stress loop.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    fix the flaky checkout test (SHOP-412)
found    forEach(async) never awaited: checkout returns before reserve
doubt    "flaky test" → real bug; fails when latency>25ms = 15/40 ≈ 38%
stakes   sold-out sku-blue-mug still gets an orderId; error is dropped

  2 │    lint gate: no floating promises in src/, fails CI
  1 │    checkout rejects out-of-stock, releases partial holds     ◀
  0 ┷    floor: await all reservations, drop 25ms sleep; 200 runs ok

deeper   inject fixed latency (0ms, 39ms) instead of a sleep race
wider    QA: stress loop · DB: all-or-nothing reserve · chaos: 40ms
target   0 fails in 500 runs (now ~38% per run, est. from code)
judge    scratch stress.sh + 39ms-latency test, tier 1; must fail now
access   ✓ node 24 git gh · ~ eslint dev dep (your ok) → rung 2
         ✗ order data, so past damage can't be counted
cost     floor ~5 min · rung 1 ~15 min, ~2× tokens · you ~3 min
── reply: go (rung 1) · go 2 · go 0 (floor only) ───────────────────
```

```text
In this Node project, test/checkout.test.js fails about 1 run in 3 because src/checkout.js reserves stock with cart.items.forEach(async ...), so checkout() returns before reservations land, and the test covers that with a 25 ms sleep against up to 40 ms of simulated latency. The same bug means an out-of-stock item (sku-blue-mug, stock 0) still gets an order, and the error turns into an unhandled rejection. Before changing anything, write a stress script that runs the suite 500 times, plus deterministic tests that pin latency at 39 ms and order an out-of-stock item. Show that they fail on the current code. First deliver the floor: await every reservation and remove the sleep from the test. Then make checkout all-or-nothing: if any item fails to reserve, reject and release the items already reserved. The target is 0 failures in 500 runs. Report any misses with counts.
```

Taking rung 1 (`--go`). Writing the judge first: