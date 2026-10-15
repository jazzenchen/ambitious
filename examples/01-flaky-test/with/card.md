# The card /ambitious printed before doing any work (verbatim from the run)

The test isn't really flaky. `checkout()` returns before the stock reservation has finished, so an order for a sold-out mug still gets an order ID. Rung 1 fixes that and checks it with 1,000 clean test runs.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    fix the flaky checkout test (SHOP-412)
found    checkout.js:6 forEach(async) is never awaited; returns early
doubt    "the test is flaky" → test is right; checkout skips reserve
stakes   sold-out sku gets an orderId; red ~1 in 3 CI runs for 2 wks

  2 │    ban un-awaited async in src/: lint gate fails CI on it
  1 │    checkout awaits all; sold-out rejects, rolls back holds   ◀
  0 ┷    floor: test passes 1,000/1,000 runs with no sleep in it

deeper   latency 0-40 ms vs 25 ms sleep → 15/40 = 37.5% red runs
wider    concurrency: random latency orders · adversary: random carts
target   0 fails in 1,000 runs + stock never < 0 (now ~37%, est.)
judge    scratch stress loop + sold-out test; tier 1; must fail now
access   ✓ node 24 git gh · ~ typescript-eslint dev dep (you OK) → 2
access   ✗ order/CI history: can't check past oversold orders
cost     floor ~10 min · rung 1 ~25 min, ~3× tokens · you ~3 min
── reply: go (rung 1) · go 2 · go 0 (floor only) ───────────────────
```

```text
In src/checkout.js, checkout() calls cart.items.forEach(async ...), so it
returns { orderId, reservations } before any reserve() from
src/inventory.js has finished. The test in test/checkout.test.js then
sleeps 25 ms against 0–40 ms of simulated latency, which predicts about
37.5% red runs (NOTES.md reports about 1 in 3). Make checkout await every
reservation, reject the order when any item is out of stock, and release
any holds it already placed. Then remove the sleep from the test and add
tests for a sold-out cart and a mixed cart. Write the judge first and
show that it fails on the current code: a sold-out-cart test plus a loop
that runs the suite 1,000 times and counts failures. Then deliver the
minimal test fix as the floor. Report the measured before and after
failure counts, and anything the loop doesn't cover.
```

Taking rung 1, the recommended one, as `--go` allows.
