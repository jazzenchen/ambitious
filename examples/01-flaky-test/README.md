# Example 1 — Fix a flaky test

**Both runs fixed the flaky test, but only the `/ambitious` run also fixed a stock leak that plain Claude's version left in (a hidden check caught it, and a separate probe found it in 300 of 300 failed carts), at about 4 times the cost and 19 times the time, and two of the three blind judges preferred it.**

## The starting point

The project is a tiny pretend online shop, written for this comparison. In testing, a sample project like this is called a fixture. Some terms used below:

- A **test** is a small program that checks the code does what it should. A project's **test suite** is all of its tests together.
- A **flaky** test passes on some runs and fails on others, with no change to the code.
- **CI** (continuous integration) is the service that runs every test automatically each time someone changes the code. "Red" means a test failed.
- **ms** means milliseconds, thousandths of a second.

The project has five files:

- [`NOTES.md`](../../evals/fixtures/flaky-checkout/NOTES.md), the team's note on the problem:
  ```text
  CI has been red ~1 in 3 runs for two weeks because of `checkout reserves every item`.
  Team keeps hitting "re-run". Ticket SHOP-412: "fix the flaky checkout test".
  ```
- [`src/inventory.js`](../../evals/fixtures/flaky-checkout/src/inventory.js) is a pretend stock system. It starts with 3 red mugs and 0 blue mugs. Each reservation waits a random 0 to 40 ms to imitate a slow network. If there isn't enough stock, it fails with the error `out of stock: <sku>` (a SKU is an item's stock code, such as `sku-red-mug`).
- [`src/checkout.js`](../../evals/fixtures/flaky-checkout/src/checkout.js) is the checkout itself:
  ```js
  cart.items.forEach(async (item) => {
    reservations.push(await reserve(item.sku, item.qty));
  });
  return { orderId: `ord_${cart.id}`, reservations };
  ```
- [`test/checkout.test.js`](../../evals/fixtures/flaky-checkout/test/checkout.test.js) is the one test. It checks out one red mug, waits 25 ms (the code comment says `give reservations time to land`), then checks that one reservation was recorded.
- [`package.json`](../../evals/fixtures/flaky-checkout/package.json) holds the project settings. `npm test` runs the tests.

**What was really wrong, in plain words.** In JavaScript, `async` and `await` mark a step that has to wait for something slow, such as a network call. `forEach` means "do this for each item in the list". So `forEach(async ...)` reads as "for each item in the cart, start reserving it, and write the reservation down once it comes back."

The catch is that `forEach` starts each job and moves straight on. It never waits for the jobs to finish. Checkout therefore hands back an order, with an empty list of reservations, while the reservations are still on their way. It is like a cashier printing your receipt before the warehouse has confirmed the items exist.

The test hid this by waiting 25 ms before looking. But the stock system takes anywhere from 0 to 40 ms, so whenever it takes longer than 25 ms, the test looks too early and fails. That is 15 of the 40 possible milliseconds, about 37.5%, which matches the team's "~1 in 3". The test was never really flaky: about a third of the time, it caught a real bug. There is a second effect, too. When an item is sold out, its reservation fails, but by then checkout has already returned an order number, and nothing is waiting to catch the error. So a sold-out item still gets ordered.

**The request** was the ticket's own wording: *fix the flaky checkout test*.

## What was typed

Both runs used fresh copies of the same project, the same model (`claude-opus-5-5`) and permission to edit files ([how the runs were set up](../../evals/outcomes/OUTCOMES.md)).

Plain Claude:

```text
fix the flaky checkout test
```

With the skill (`--go` tells it to print its card, then carry out its recommended option right away, without waiting for a person to choose):

```text
/ambitious --go fix the flaky checkout test
```

## Without /ambitious

Plain Claude finished in 43.5 seconds for $0.18. It found the same cause, explained it correctly and fixed it in the code rather than by lengthening the wait. It replaced the `forEach` with `Promise.all`. A *promise* is JavaScript's IOU for a result that will arrive later, and `Promise.all` means "start all these jobs at once and wait for all of them". Here is the new core of [`src/checkout.js`](without/files/src/checkout.js):

```js
  const reservations = await Promise.all(
    cart.items.map((item) => reserve(item.sku, item.qty))
  );
```

It deleted the 25 ms wait from the test and added two tests to [`test/checkout.test.js`](without/files/test/checkout.test.js): one for a cart with several items, and one checking that a sold-out item makes checkout fail. Its reply ([`response.md`](without/response.md)) says *"The suite passed 30 runs in a row with no failures."* In total it changed 2 files (+18/−5 lines).

It also noticed a remaining problem, said so plainly and left it alone:

> **Something to decide later:** if one item in a cart is out of stock, the other items that were reserved successfully still use up stock, because nothing rolls them back. The old code had the same problem, and this fix doesn't change it.

**What "a failed cart leaks held stock" means.** Picture a cart with one red mug (in stock) and one blue mug (sold out). Checkout tries to reserve both at once. The red mug's reservation succeeds, so one red mug is set aside for this order. The blue mug fails, so the whole order fails, which is correct. But nobody gives the red mug back. `Promise.all` also stops at the first failure without waiting for the other jobs, so sometimes the red mug's reservation is still on its way and lands after checkout has already reported the failure. Either way, a red mug ends up set aside for an order that doesn't exist, and no other customer can buy it. In a real shop, stock would show as unavailable while it sits on the shelf, and every failed cart would make it worse.

## With /ambitious

Before changing anything, the skill printed the text and card below, copied from the run's transcript (the transcript is not included in this repo; [`response.md`](with/response.md) keeps only the final message). This is a different run from the demo on the repo's front page, so the card differs from that one.

> The test isn't really flaky. Checkout returns before it has reserved any stock, and an item that's out of stock still gets an order number, so the test is catching a real bug. Rung 2 fixes the bug and adds a check that stops it coming back.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    fix the flaky checkout test (SHOP-412)
found    checkout.js:6 forEach(async) returns before reserve() runs
doubt    "the test is flaky" → the code is: 25ms sleep vs 0-40ms
         latency fails 15/40 = 37.5%, NOTES says ~1 in 3
stakes   out-of-stock throws go unhandled, so a sold-out cart still
         gets an orderId; such orders may exist already

  3 ▲    find orders already taken for sold-out stock, then fix them
  2 │    check in npm test fails on async forEach / dropped promise ◀
  1 │    await all holds; sold-out rejects, partial holds released
  0 ┷    floor: test passes without the sleep, 500/500 runs green

deeper   await every promise with Promise.all, then stress-loop it
wider    payments: all-or-nothing holds · chaos: 200ms random lag
target   0 failures in 2,000 stress checkouts (now ~37%, est.)
judge    scratch stress.js, tier 1, incl. sold-out cart; fails now
access   ✓ node 24 git gh · ✗ order data, CI history → rung 3
cost     floor ~10 min · rung 2 ~30 min, ~3× tokens · you ~5 min
── reply: go (rung 2) · go 1 · go 0 (floor only) ───────────────────
```

**What the card is saying**

- **asked:** it restates the request and attaches the ticket number it found in `NOTES.md`.
- **found:** line 6 of `src/checkout.js`, the `forEach(async ...)` explained above, is the real cause.
- **doubt:** the team believes the *test* is flaky. The card checks that belief with arithmetic: a 25 ms wait against a 0 to 40 ms delay should fail about 15 runs in 40 (37.5%), which matches the team's "~1 in 3". So the fault is in the code.
- **stakes:** what leaving it costs. A sold-out cart still gets an order number, and "unhandled" means the error is raised but nothing catches it. "May exist already" means real orders like that could already be in the system, but it had no way to check.
- **The ladder** is the set of options, called rungs, with the most ambitious at the top. `◀` marks the one it recommends. Taking a rung means climbing to it one step at a time: the floor first, then each rung above it in turn.
  - **Rung 3:** find past orders taken for sold-out stock and fix them. This needs the shop's order data, which it couldn't reach, so it isn't recommended.
  - **Rung 2 (recommended):** add a test that fails if anyone writes this pattern again. A "dropped promise" is a slow job that gets started but whose result nobody waits for.
  - **Rung 1:** wait for every reservation (a "hold"), reject sold-out items, and give back held stock when an order fails partway.
  - **Rung 0, the floor:** exactly what was asked. The test passes without the wait, 500 times in a row. The floor is guaranteed; everything above it is extra.
- **deeper:** the expert's method. Wait for every promise, then run the code thousands of times in a "stress loop" to shake out rare failures.
- **wider:** methods borrowed from other fields. From payments: holds are all-or-nothing, so a failed order keeps nothing. From chaos testing: deliberately add up to 200 ms of random delay to see what breaks.
- **target:** zero failures in 2,000 stress-test checkouts. Today's rate, about 37%, is labelled `est.` because it was worked out on paper, not measured.
- **judge:** what decides success instead of Claude's own opinion: a throwaway script, written before the fix, that includes a sold-out cart and must fail on the current code. "Tier 1" is the skill's strongest kind of judge, a program that runs and returns a number.
- **access:** `✓` marks the tools it could use: node 24 (the JavaScript engine), git (version history) and gh (GitHub's command-line tool). `✗` marks what it couldn't reach: real order data and past CI runs. Rung 3 would need both.
- **cost:** estimated time for the floor and for rung 2, rung 2's token use as a multiple of the floor's (tokens are the chunks of text a model reads and writes, and what usage is billed on), and about 5 minutes of your time to review.

Under the card it printed ``Taking rung 2 (`--go`).``, because `--go` means "take the recommendation".

<details><summary>It also printed a ready-to-paste prompt (the same plan written for any AI tool)</summary>

```text
In a Node ESM project, src/checkout.js:6 reserves cart items with `cart.items.forEach(async ...)`, so checkout() returns before any reservation lands. Out-of-stock errors from src/inventory.js reserve() become unhandled rejections, so a cart holding a 0-stock SKU still gets an orderId. test/checkout.test.js hides this with a 25 ms sleep against 0–40 ms of random latency, which fails about 37% of the time. First write a stress script that runs 2,000 checkouts, including a sold-out cart and a mixed cart, and fails on any missing reservation, any order for out-of-stock items, or any stock left held after a failure. Prove it fails on the current code. Then deliver the floor: checkout awaits every reservation (Promise.all), the test's sleep is removed, and 500 consecutive `node --test` runs pass. Next, make checkout all-or-nothing: if any reserve fails, release the holds already taken and reject. Finally, add a zero-dependency check to `npm test` that fails on async callbacks passed to forEach/map in src/, and prove it catches a planted example. Report any misses with numbers.
```
</details>

**What it did after `--go`**, in order, according to the transcript:

1. **Wrote the judge first.** It wrote a scratch script that runs checkouts over three kinds of cart (one red mug, one sold-out blue mug, and a mixed cart) and counts every problem. On the original code it reported 600 problems in 300 checkouts: 100 orders missing their reservation, 200 carts with a sold-out item accepted, and 300 errors nothing caught.
2. **Measured the old test.** Its first measuring loop called the test runner the wrong way and showed 60 failures in 60 runs. It noticed that didn't match "1 in 3", re-ran with the project's own test command, and got 34 failures in 100.
3. **The floor.** It made the same `Promise.all` change plain Claude made and removed the wait. The test passed 500 runs out of 500. But its own judge still failed: `FAIL 100 failures in 300 checkouts`. Every one was stock left held after a failed mixed cart, the same leak plain Claude shipped. Rung 1 was aimed at exactly this.
4. **Rung 1.** It switched to `Promise.allSettled`, which means "wait until every reservation has finished, whether it succeeded or failed, then look at all the results". If any reservation failed, it gives back the ones that succeeded through a new `release()` function, then reports the error. Run against its own floor-only version, its new tests gave 2 passes and 1 failure: the leak test caught the leak. The core of [`src/checkout.js`](with/files/src/checkout.js):
   ```js
     const failed = results.find((r) => r.status === "rejected");
     if (failed) {
       // All or nothing: give back any stock this order did manage to hold.
       const held = results.filter((r) => r.status === "fulfilled").map((r) => r.value);
       await Promise.all(held.map((r) => release(r.sku, r.qty)));
       throw failed.reason;
     }
   ```
5. **Rung 2.** It added [`test/no-async-foreach.test.js`](with/files/test/no-async-foreach.test.js), which reads every JavaScript file in `src/` and fails if it finds `.forEach(async`. It planted a copy of the original checkout in a scratch folder and confirmed the check flagged line 6.
6. **Final judge runs:** 2,000 stress checkouts with 0 failures, and `npm test` run 500 times with 0 failures. Then it printed its receipt:

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

A few lines need explaining:

- **untested:** the chaos idea from the card (200 ms of delay) was never run, and the new check only catches `forEach(async`, not other ways of dropping a promise.
- **moved:** it changed its own judge partway through and says so. Its leak check first went through `checkout()`, which on the old code never reported errors, so that check could never have seen a leak. It switched to calling `reserve()` directly. The skill requires any change to the judge to be reported in the open.
- **cost:** the run could not see its own token count. The script that launched both runs recorded 846.5 seconds (about 14 minutes) and 831,121 tokens, against the card's guess of about 30 minutes.
- **next:** the past-damage check (rung 3) still needs access to the order data.

Its reply also warns that `checkout()` now throws `out of stock: <sku>` (stops with that error) instead of returning an order number, so code that calls it must handle that error. Plain Claude's version changes this too. In total the skill run changed 4 files (+54/−8 lines) and added one new function that other code can call, `release()`.

## What the hidden checks found

Neither run saw these checks. [`flaky_check.sh`](../../evals/outcomes/checks/flaky_check.sh) copies each finished project, runs its whole test suite 200 times, then adds 3 hidden tests ([`flaky_hidden.test.js`](../../evals/outcomes/checks/flaky_hidden.test.js)):

- **H1:** when checkout says it's done, every reservation has really been made.
- **H2:** a cart with a sold-out item doesn't get an order number.
- **H3:** after a failed mixed cart (red mug plus sold-out blue mug), all 3 red mugs can still be reserved, meaning the held mug was given back.

The [log](../../evals/outcomes/results/flaky-hidden-checks.log), verbatim:

```text
with_skill: {"suite_fail":0,"suite_runs":200,"H1":true,"H2":true,"H3":true}
without_skill: {"suite_fail":0,"suite_runs":200,"H1":true,"H2":true,"H3":false}
```

A separate tester, also an AI model rather than a person, then probed both finished projects with one shared test script, 300 trials per scenario ([`measurements-and-judgments.json`](../../evals/outcomes/results/measurements-and-judgments.json)):

| Measure | Plain Claude | With /ambitious |
|---|---|---|
| Test suite failures in 200 runs | 0 / 200 | 0 / 200 |
| H1 · H2 · H3 | pass · pass · **fail** | pass · pass · pass |
| Failed mixed carts that leaked a red mug | **300 / 300** | 0 / 300 |
| Units of stock lost over those 300 trials | **300** | 0 |
| Mug still held at the moment checkout reported failure | 159 / 300 | 0 / 300 |
| Tests that check for the leak | 0 | 1 |
| Its leak test, run on plain Claude's code | — | caught it 29 / 30 times |
| Median time to report a failed cart | 21.3 ms | 30.5 ms |
| Lines changed (files) | +18 / −5 (2) | +54 / −8 (4) |
| Time · cost · tokens | 43.5 s · $0.18 · 114,685 | 846.5 s · $0.75 · 831,121 |

What the numbers mean:

- **Both fixed the flake.** 0 failures in 200 full test runs each, and both pass H1 and H2.
- **Only one fixed the leak.** In plain Claude's version, every failed mixed cart kept a red mug: 300 trials, 300 mugs. In 159 trials the mug was already set aside when checkout gave up. In the other 141, the reservation was still on its way and landed afterwards. Plain Claude's tests never try this case, so they can't notice it.
- **The skill's own leak test works, mostly.** Run against plain Claude's code, it failed 29 times in 30. It is slightly unreliable because it checks indirectly, by trying to reserve 3 mugs, without waiting for reservations still on their way.
- **The skill's version has weak spots too.** The new `forEach` check looks for the folder `src` relative to wherever it is run, so run from another folder it crashes with a "file not found" error (`ENOENT`). It also misses the pattern when `async` sits on the next line: it caught 1 of 2 in a test file. A failed cart takes a little longer to report (30.5 ms against 21.3 ms) because it waits for the slowest reservation. When several items fail, it reports only the first in cart order; plain Claude's version reports whichever failure happens first in time.

## What the blind judges said

Three judges, each an AI model rather than a person, compared the two finished projects. The projects were labelled only A and B, with the skill's files removed; here the skill's run was A. Each judge read the code and ran its own checks. "Confidence" is the number each judge gave for how sure it was of its pick: 1 means certain, and read as a probability, 0.5 would be a coin flip.

| Judge | Preferred | Confidence |
|---|---|---|
| Busy requester: wants the best real outcome today | /ambitious | 0.57 |
| Senior practitioner: looks for the deeper, more correct method | /ambitious | 0.64 |
| Skeptic: penalizes scope creep (doing more than was asked) and anything unverifiable | plain Claude | 0.80 |

- **Busy requester:** both fix the flake equally reliably and plain Claude's is the safer minimal change, but `/ambitious` also closes a real stock leak in the same code for about five more minutes of review, so it gets a narrow edge.
- **Senior practitioner:** its own probe found plain Claude's version leaked stock in 50 of 50 failed mixed carts against 0 of 50 for `/ambitious`. It judged that a real inventory bug and a source of future flaky tests, which outweighs the skill's extra scope and its awkward `forEach` check.
- **Skeptic:** plain Claude's three-line fix is the smallest correct change and adds nothing invented. `/ambitious` invented a new `release()` function that the real stock service, which this file only imitates, may not have. It also made checkout all-or-nothing when nobody asked for that, and added a `forEach` check that is itself fragile.

## Takeaway

Here, `/ambitious` paid off because writing a check before the fix turned the problem plain Claude left as "something to decide later" into a measured bug (100 leaks in 300 checkouts) and then proved it fixed (0 in 2,000). Plain Claude saw the same problem, said so honestly, and left it. Use the skill when a hidden mistake costs something real, like stock, money or customer orders, and you can afford about 4 times the cost and 19 times the wait. If you want the smallest change to review in 30 seconds and plan to handle the leak yourself, plain Claude's answer was correct and candid about the gap.

## Files

Plain Claude ([`./without`](without/)):
- [`prompt.txt`](without/prompt.txt) · [`response.md`](without/response.md)
- [`files/src/checkout.js`](without/files/src/checkout.js) · [`files/test/checkout.test.js`](without/files/test/checkout.test.js)

With /ambitious ([`./with`](with/)):
- [`prompt.txt`](with/prompt.txt) · [`response.md`](with/response.md) (local scratch paths replaced with `<tmp>`)
- [`files/src/checkout.js`](with/files/src/checkout.js) · [`files/src/inventory.js`](with/files/src/inventory.js)
- [`files/test/checkout.test.js`](with/files/test/checkout.test.js) · [`files/test/no-async-foreach.test.js`](with/files/test/no-async-foreach.test.js)

Starting project: [`evals/fixtures/flaky-checkout/`](../../evals/fixtures/flaky-checkout/)

Raw eval output ([`evals/outcomes/results/flaky-checkout/`](../../evals/outcomes/results/flaky-checkout/)):
- without: [`prompt.txt`](../../evals/outcomes/results/flaky-checkout/without_skill/prompt.txt) · [`response.md`](../../evals/outcomes/results/flaky-checkout/without_skill/response.md) · [`diff.patch`](../../evals/outcomes/results/flaky-checkout/without_skill/diff.patch) · [`diffstat.txt`](../../evals/outcomes/results/flaky-checkout/without_skill/diffstat.txt) · [`timing.json`](../../evals/outcomes/results/flaky-checkout/without_skill/timing.json)
- with: [`prompt.txt`](../../evals/outcomes/results/flaky-checkout/with_skill/prompt.txt) · [`response.md`](../../evals/outcomes/results/flaky-checkout/with_skill/response.md) · [`diff.patch`](../../evals/outcomes/results/flaky-checkout/with_skill/diff.patch) · [`diffstat.txt`](../../evals/outcomes/results/flaky-checkout/with_skill/diffstat.txt) · [`timing.json`](../../evals/outcomes/results/flaky-checkout/with_skill/timing.json)
- Hidden checks: [`flaky_check.sh`](../../evals/outcomes/checks/flaky_check.sh) · [`flaky_hidden.test.js`](../../evals/outcomes/checks/flaky_hidden.test.js) · [`flaky-hidden-checks.log`](../../evals/outcomes/results/flaky-hidden-checks.log)
- Measurements, and the judges' verdicts with the A/B labels decoded: [`measurements-and-judgments.json`](../../evals/outcomes/results/measurements-and-judgments.json)
- Method: [`OUTCOMES.md`](../../evals/outcomes/OUTCOMES.md) · [`run_outcomes.sh`](../../evals/outcomes/run_outcomes.sh) · the skill: [`SKILL.md`](../../skills/ambitious/SKILL.md)
