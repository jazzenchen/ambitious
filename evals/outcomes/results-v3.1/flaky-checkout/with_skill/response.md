I fixed it. The test was never the problem. Checkout returned before it had reserved any stock, and sold-out items still got an order number. Checkout now waits for every reservation and rejects sold-out items. If an order fails partway, it gives back any stock it had already reserved. A new check in `npm test` stops the original pattern from coming back. Nothing is committed.

```text
── /ambitious · result ─────────────────────────────────────────────
floor    ✓ checkout awaits all reserves; 25ms sleep removed
rung 1   ✓ sold-out cart rejects; failed order frees its held stock
rung 2   ✓ new test fails on forEach(async) in src/; caught planted
target   0 fails in 2,000 stress checkouts (was 600 in 300)        ✓
judge    stress.mjs . 2000 → PASS 0 failures in 2000 checkouts
         npm test ×500 → failed 0/500 (old test failed 34/100)
doubt    "the test is flaky" → refuted · code returned too early
untested 200ms lag; other dropped-promise forms (.map w/o await)
moved    stock check went via checkout(), which never threw on old
         code; now calls reserve() directly
files    src/checkout.js src/inventory.js (+release) · tests: 2 new
         + no-async-foreach.test.js · no new deps
cost     ~8 runs vs est. ~6 · tokens not visible
next     order data access → find orders already sold out (rung 3)
────────────────────────────────────────────────────────────────────
```

- **Behaviour change:** `checkout()` now throws `out of stock: <sku>` instead of returning an order number. Any caller that relied on always getting an order number needs to handle that error.
- **Possible damage already done:** for as long as this code has been live, sold-out items could have been ordered, and failed orders may have kept stock reserved. I couldn't check because I have no access to order data. That's rung 3.
- **Limit of the new check:** it only catches `forEach(async …)`. It won't catch other ways of dropping a promise, such as a `.map(async …)` whose results are never awaited.
- **Scratch files:** the stress script is `<scratchpad>/stress.mjs`. The floor-only version of checkout is saved as `<scratchpad>/checkout.floor.js` if you want only the minimal fix.