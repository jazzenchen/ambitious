The test isn't really flaky. Checkout returns before any stock is reserved, so the test passes or fails depending on random timing, and a cart with a sold-out mug still gets an order number. Rung 1 fixes checkout itself, so sold-out carts fail cleanly and half-finished reservations are undone, and proves it with 200 clean test runs plus new sold-out tests that fail today.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    fix the flaky checkout test (SHOP-412)
found    checkout.js:6 forEach(async) returns before any reserve()
doubt    "the test is flaky" → test waits 25 ms, reserve takes 0-40
stakes   sold-out cart gets orderId; CI red ~1 in 3 for 2 weeks

  2 │    stop it recurring: lint ban + deterministic latency in tests
  1 │    fix checkout: sold-out rejects, partial holds rolled back ◀
  0 ┷    floor: await all reserves, drop the sleep; 200/200 green

deeper   race math: P(latency>25ms)=15/40=37.5% vs notes' ~1 in 3
wider    payments: all-or-nothing hold · chaos: inject 0/40ms delays
target   0 fails in 200 runs (now ~37.5% fail, est. from code)
judge    scratch loop of node --test ×200 + sold-out tests; tier 1
access   ✓ node 24 git gh · ~ eslint dev dep (you OK) → rung 2
access   ✗ CI run history, order logs: no remote found (unverified)
cost     floor ~10 min · rung 1 ~30 min, ~3× tokens · you ~5 min
── reply: go (rung 1) · go 2 · go 0 (floor only) ───────────────────
```

```text
In a Node ESM project, test/checkout.test.js ("checkout reserves every item") fails about 1 in 3 CI runs. The cause is in src/checkout.js:6: cart.items.forEach(async ...) means checkout() returns before any reserve() finishes. The test then sleeps 25 ms, while reserve() in src/inventory.js waits a random 0–40 ms, which predicts 37.5% failures. The same bug means a cart containing an out-of-stock SKU still gets an orderId, the error becomes an unhandled rejection, and stock reserved for other items is never released. First, write a harness that runs `node --test` 200 times and counts failures, and add tests that a sold-out cart rejects and that a mixed cart releases its partial holds; show that both fail on the current code. Deliver the floor first: await every reservation (Promise.all) and remove the sleep, so the original test passes 200 of 200 runs. Then make checkout all-or-nothing, so it rejects with the out-of-stock error and rolls back any reservations already taken. Report the before and after failure counts with the exact commands, and list anything the tests do not cover.
```