I fixed the flaky test: it was a real bug, not flakiness. Checkout returned before the stock reservations finished, so it failed whenever the fake network delay ran past 25 ms. It also let orders through for items that were sold out. Checkout now waits for every reservation. If any item can't be reserved, it gives back the ones already held and fails the order. The suite now passes 500 runs in a row; it failed 32 of 100 before.

```text
── /ambitious · result ─────────────────────────────────────────────
floor    ✓ checkout awaits all reservations; 25ms sleep removed
         · src/checkout.js (floor-only copy in scratchpad)
rung 1   ✓ out-of-stock rejects; partial holds released on failure
target   0/500 fails vs 0 in 500 (was 32/100, measured)             ✓
judge    stress.sh 500 → fails: 0/500
         new tests on old code → ℹ pass 0 · ℹ fail 4
doubt    "flaky test" → refuted · forEach(async) never awaited
untested a release() that itself fails; past orders already placed
files    src/checkout.js · src/inventory.js (+release, test hooks)
         · test/checkout.test.js (1 → 4 tests) · no new deps
cost     ~4 judge runs + 600 suite runs vs est. · tokens not visible
next     order data access to count orders made without a hold
────────────────────────────────────────────────────────────────────
```

- **Behaviour change:** an order with an out-of-stock item used to get an order ID. It now fails with `out of stock: <sku>`. Anything that calls `checkout()` needs to handle that error.
- **Past damage:** I couldn't check whether the bug already let real orders through without reserved stock, because this session has no access to order data.
- **Inventory stub:** `src/inventory.js` gained a `release()` function and two test-only helpers (`_setLatency`, `_stock`).
- **Scratch files:** the stress loop is at `<scratchpad>/stress.sh`. The floor-only fix is saved next to it as `checkout.floor.js`.
- **Nothing committed:** the changes are only in your working tree.