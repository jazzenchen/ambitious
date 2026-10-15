I'll look at the code first so the proposal is grounded in what's actually there.

`[tool] Bash: {"command": "cd \"$PWD\" && git ls-files && echo --- && git log --stat -3 | head -50", "description": "List tracked files and recent history"}`

`[tool] Bash: {"command": "git ls-files; git log --stat -3 | head -50", "description": "List tracked files and recent history"}`

`[tool] Bash: {"command": "for f in NOTES.md package.json src/checkout.js src/inventory.js test/checkout.test.js; do echo \"=== $f\"; cat -n $f; done", "description": "Print all project files"}`

I read the code, and this isn't really a flaky test. The test is flaky because `checkout` itself is broken, and the bug is shipping orders today.

## What's actually wrong

`src/checkout.js:6` uses `cart.items.forEach(async ...)`. `forEach` ignores the promises it gets back, so `checkout` returns before any reservation finishes. The test tries to cover this with a 25ms sleep (`test/checkout.test.js:10`), but `reserve` takes 0–40ms, so roughly 1 run in 3 loses the race. That matches the "~1 in 3" in `NOTES.md`.

What this means in production:
1. **Orders go out with an empty `reservations` array.** Callers get the result before inventory has confirmed anything.
2. **Out-of-stock items don't stop the checkout.** When `reserve` throws, nothing is listening, so you get an unhandled rejection while `checkout` still returns an `orderId`. Someone can "buy" `sku-blue-mug`, which has 0 in stock. Depending on how the process handles unhandled rejections, this could also crash the server.
3. **Partial failures leak stock.** In a multi-item cart where one item fails, the others stay reserved, and nothing releases them.

## Proposed plan, most ambitious first

**1. Fix checkout so it's correct and all-or-nothing**
- Reserve all items in parallel and actually wait for them (`Promise.allSettled`), which keeps the speed the comment was going for.
- If any item fails, release the ones that succeeded and throw a typed `OutOfStockError` listing the failed SKUs. This needs a new `release(sku, qty)` in `inventory.js`.

**2. Make the tests deterministic and cover the real behaviour**
- Remove the sleep. Add a way to inject latency into the inventory module (or use `node:test` mock timers) so the tests never depend on timing.
- New tests:
  - multi-item cart reserves everything
  - an out-of-stock item makes `checkout` reject
  - a partial failure restores stock
  - two concurrent checkouts racing for the last unit: exactly one wins and stock never goes negative
  - a regression test with randomised latency that runs many times and must pass every time

**3. Stop this class of bug from coming back**
- Add ESLint with `no-misused-promises` / `no-floating-promises` (via typescript-eslint type-aware linting on JS) or a simpler `no-restricted-syntax` rule against `forEach(async`, and run it in `npm test`.
- Add a CI "stress" step that runs the suite about 50 times, so new timing flakes fail the build instead of getting re-run.

**4. Check for production damage (I can only flag this, not do it)**
- Every order since this code shipped may have been confirmed without a reservation, or for stock that didn't exist. Someone with access to order and inventory data should look for overselling and unexplained stock drift. I'd write that up in the SHOP-412 note.

**Minimum version, if you'd rather keep it small:** steps 1 and 2 only. Replace the `forEach` with `Promise.all`, remove the sleep, and add an out-of-stock test. That's about 10 lines. I'd still strongly recommend at least the rollback in step 1, because without it a failed checkout keeps stock reserved.

Should I go ahead with the full plan (1–3, plus the write-up for 4), or a subset? I haven't changed anything yet.