I fixed the flaky test (SHOP-412) by fixing a real bug in checkout, not by changing the test's timing. The suite passed 30 runs in a row with no failures.

**The bug:** `src/checkout.js` used `cart.items.forEach(async …)`. `forEach` doesn't wait for async callbacks, so `checkout()` returned an order with an empty `reservations` array, and the reservations finished at some point afterwards. The test slept 25ms to "give reservations time to land", but the simulated stock call takes up to 40ms, so it failed whenever the call took longer than 25ms. This affects real orders too:
- Orders could come back without their reservations.
- Out-of-stock errors were never passed back to the caller, so a failed checkout still looked successful.

**What I changed:**
- **`src/checkout.js`:** it now waits for all reservations to finish before returning (`await Promise.all(cart.items.map(...))`). They still run in parallel, so checkout isn't slower.
- **`test/checkout.test.js`:** removed the sleep. I added a test for a cart with several items and one that checks an out-of-stock item makes checkout fail. That second test would have caught the swallowed error.

**Something to decide later:** if one item in a cart is out of stock, the other items that were reserved successfully still use up stock, because nothing rolls them back. The old code had the same problem, and this fix doesn't change it.

I haven't committed anything.