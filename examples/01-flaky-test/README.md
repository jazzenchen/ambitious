# Example 1 — Fix a flaky test

**Both runs fixed the flaky test, but only the `/ambitious` run (skill version 3.2) also fixed a stock leak that plain Claude's version left in: a hidden check caught it, and a separate probe found it in 300 of 300 failed carts. The skill run cost about 3 times as much and took about 28 times as long (20 minutes against 44 seconds), and two of the three blind judges preferred it.**

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

**The stock leak, in plain words.** Picture a cart with one red mug (in stock) and one blue mug (sold out). Checkout tries to reserve both at once. The red mug's reservation succeeds, so one red mug is set aside for this order. The blue mug fails, so the whole order fails, which is correct. But nobody gives the red mug back. `Promise.all` also stops at the first failure without waiting for the other jobs, so sometimes the red mug's reservation is still on its way and lands after checkout has already reported the failure. Either way, a red mug ends up set aside for an order that doesn't exist, and no other customer can buy it. In a real shop, stock would show as unavailable while it sits on the shelf, and every failed cart would make it worse.

## With /ambitious

This run used version 3.2 of the skill. Before changing anything, it printed the sentence, card and prompt below. They are copied verbatim from [`card.md`](with/card.md). The run's full transcript is not included in this repo; [`response.md`](with/response.md) keeps its final message. This is a different run from the demo on the repo's front page, so the card differs from that one.

> The test isn't really flaky. `checkout()` returns before the stock reservation has finished, so an order for a sold-out mug still gets an order ID. Rung 1 fixes that and checks it with 1,000 clean test runs.

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

**What the card is saying**

- **asked:** it restates the request and attaches the ticket number it found in `NOTES.md`.
- **found:** line 6 of `src/checkout.js`, the `forEach(async ...)` explained above, is the real cause. "Never awaited" means nothing waits for those jobs to finish, so checkout "returns early".
- **doubt:** the team believes the *test* is flaky. The card says the opposite: the test is right to fail, because checkout skips past the reservation step.
- **stakes:** what leaving it costs. A sold-out item (`sku`) still gets an order number, and CI has failed about 1 run in 3 for two weeks.
- **The ladder** is the set of options, called rungs, with the most ambitious at the top. `◀` marks the one it recommends. Taking a rung means climbing to it one step at a time: the floor first, then each rung above it in turn.
  - **Rung 2:** a "lint gate". A linter is a tool that reads code and flags risky patterns; the gate makes CI fail whenever it finds an `async` job that nothing waits for. This needs a new tool installed in the project (see **access**), so it isn't recommended.
  - **Rung 1 (recommended):** checkout waits for every reservation, rejects an order with a sold-out item, and "rolls back holds", meaning it gives back any stock it had already set aside for that order.
  - **Rung 0, the floor:** exactly what was asked. The test passes 1,000 times in a row with the 25 ms wait taken out. The floor is guaranteed; everything above it is extra.
- **deeper:** how an expert would get to the bottom of it. Here that is arithmetic: a 25 ms wait against a 0 to 40 ms delay should fail about 15 runs in 40 (37.5%), which matches the team's "~1 in 3".
- **wider:** methods borrowed from other fields. From concurrency work (code where many things happen at once): let random delays change the order in which reservations come back. From the attacker's point of view: throw random carts at checkout.
- **target:** zero failures in 1,000 runs, and stock never drops below zero. Today's failure rate, about 37%, is labelled `est.` because it was worked out on paper, not measured.
- **judge:** what decides success instead of Claude's own opinion: a throwaway "stress loop" that runs the tests over and over and counts failures, plus a test with a sold-out item. "Tier 1" is the skill's strongest kind of judge, a program that runs and returns a number. "Must fail now" means it has to fail on today's code first, to prove it can tell broken from fixed.
- **access:** `✓` marks the tools it could use: node 24 (the JavaScript engine), git (version history) and gh (GitHub's command-line tool). `~` marks something one step away: typescript-eslint, a linter, added to the project as a development-only tool, which needs your OK first (the skill always asks before adding anything to a project's list of dependencies). With it, rung 2 becomes possible. `✗` marks what it couldn't reach: order and CI history, so it can't check whether sold-out stock was already oversold.
- **cost:** estimated time for the floor and for rung 1, rung 1's token use as a multiple of the floor's (tokens are the chunks of text a model reads and writes, and what usage is billed on), and about 3 minutes of your time to review.

After the card and its prompt (below), it printed ``Taking rung 1, the recommended one, as `--go` allows.``

<details><summary>It also printed a ready-to-paste prompt (the same plan written for any AI tool)</summary>

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
</details>

**What it did after `--go`.** Its final reply opens:

> The checkout test is fixed and passed 1,000 out of 1,000 runs, compared with 65 failures in 200 runs before.

It switched checkout to `Promise.allSettled`, which means "wait until every reservation has finished, whether it succeeded or failed, then look at all the results". If any reservation failed, it gives back the ones that succeeded through a new `release()` function in `src/inventory.js`, then reports the error. The core of [`src/checkout.js`](with/files/src/checkout.js):

```js
  const failed = results.find((r) => r.status === "rejected");
  if (failed) {
    // Give back whatever we did manage to hold before failing the order.
    for (const r of results) {
      if (r.status === "fulfilled") release(r.value.sku, r.value.qty);
    }
    throw failed.reason;
  }
```

It deleted the 25 ms wait from the test and added two tests to [`test/checkout.test.js`](with/files/test/checkout.test.js): one checking that a sold-out item makes checkout fail, and one checking that a failed mixed cart (2 red mugs plus a sold-out blue mug) gives the red mugs back, so all 3 can then be ordered. Then it printed its receipt:

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

A few lines need explaining:

- **target:** the result against the goal: 0 failures in 1,000 runs, against a goal of 0 in 1,000. Before the fix, the test failed 65 times in 200 (32.5%). That figure is marked `measured`, unlike the card's paper estimate of about 37%.
- **judge:** two separate checks, each run 1,000 times by its stress script: its own judge test file, and the project's test. Both had 0 failures.
- **doubt:** its judge has 4 tests, and 3 of them failed on the old code, so the "flaky test" belief is marked refuted.
- **untested:** what its checks don't prove. It had no order data, so it couldn't look for past orders of sold-out items. It also flags that the check for overselling when several carts check out at once was "trivial before the fix": the old code already passed it, so passing it now shows little.
- **cost:** 2,200 test runs. It put its elapsed time ("wall", as in wall-clock time) at about 25 minutes, the same as its estimate on the card; the script that launched both runs recorded 1,212 seconds (about 20 minutes), $0.52 and 130,705 tokens. It could not see its own token count.
- **next:** a suggested follow-up. 1.4.2 is the version number in the project's `package.json`.

There is no `moved` line, because it reported no change to its judge or target partway through. Its reply also says that callers will now get an error instead of an order number for a sold-out cart, and that nothing in this project relies on the old behaviour. Plain Claude's version changes this too. Its judge files (a stress script and a separate test file) were kept in a scratch folder outside the project, so they are not in this repo. Nothing was committed; it offered to commit on a branch for SHOP-412. In total the skill run changed 3 files (+32/−7 lines), added no new dependencies, and added one new function that other code can call, `release()`.

## What the hidden checks found

Neither run saw these checks. [`flaky_check.sh`](../../evals/outcomes/checks/flaky_check.sh) copies each finished project, runs its whole test suite 200 times, then adds 3 hidden tests ([`flaky_hidden.test.js`](../../evals/outcomes/checks/flaky_hidden.test.js)):

- **H1:** when checkout says it's done, every reservation has really been made.
- **H2:** a cart with a sold-out item doesn't get an order number.
- **H3:** after a failed mixed cart (red mug plus sold-out blue mug), all 3 red mugs can still be reserved, meaning the held mug was given back.

The [log](../../evals/outcomes/results/flaky-hidden-checks.log), verbatim:

```text
with_skill (v3.2): {"suite_fail":0,"suite_runs":200,"H1":true,"H2":true,"H3":true}
without_skill: {"suite_fail":0,"suite_runs":200,"H1":true,"H2":true,"H3":false}
```

A separate tester, also an AI model rather than a person, then probed both finished projects with one shared test script: 300 checkouts of a mixed cart (one red mug plus one sold-out blue mug), counting the red mugs in stock when checkout reported the failure and again 80 ms later, once any late reservation had landed. It also ran each project's tests against the other project's code ([`measurements-and-judgments.json`](../../evals/outcomes/results/measurements-and-judgments.json)):

| Measure | Plain Claude | With /ambitious |
|---|---|---|
| Test suite failures in 200 runs | 0 / 200 | 0 / 200 |
| H1 · H2 · H3 | pass · pass · **fail** | pass · pass · pass |
| Failed mixed carts that lost a red mug | **300 / 300** | 0 / 300 |
| Units of stock lost over those 300 trials | **300** | 0 |
| Red mug's reservation still on its way when checkout reported failure | 148 / 300 | 0 / 300 |
| Tests that check for the leak | 0 | 1 |
| Its tests, run against the other version's code | all passed 20 / 20 (can't tell the two apart) | failed 17 / 20 (caught the leak) |
| Average time to report a failed cart | 20.7 ms | 28 ms |
| Lines changed (files) | +18 / −5 (2) | +32 / −7 (3) |
| Time · cost · tokens | 43.5 s · $0.18 · 114,685 | 1,212 s · $0.52 · 130,705 |

What the numbers mean:

- **Both fixed the flake.** 0 failures in 200 full test runs each, and both pass H1 and H2.
- **Only one fixed the leak.** In plain Claude's version, every failed mixed cart kept a red mug: 300 trials, 300 mugs. In 152 trials the mug was already set aside when checkout gave up. In the other 148, the reservation was still on its way and landed afterwards. Plain Claude's tests never try this case, so they can't notice it.
- **The skill's leak test works, mostly.** Run against plain Claude's code, it failed 17 times in 20, so it catches the leak most of the time but not every time. A test that only sometimes fails is itself a kind of flaky test, which the skeptic judge below holds against it.
- **The skill's version has weak spots too.** The new `release()` function does no checking, so any code could add stock for something never reserved, or pass a negative amount. A failed cart takes a little longer to report (28 ms against 20.7 ms on average) because it waits for the slowest reservation. When several items fail, it reports only the first in cart order. And its judge files live outside the project, so you can't rerun them from this repo.

## What the blind judges said

Three judges, each an AI model rather than a person, compared the two finished projects. The projects were labelled only A and B, with the skill's files removed; here the skill's run was A. Each judge read the code and ran its own checks. "Confidence" is the number each judge gave for how sure it was of its pick: 1 means certain, and read as a probability, 0.5 would be a coin flip.

| Judge | Preferred | Confidence |
|---|---|---|
| Busy requester: wants the best real outcome today | /ambitious | 0.68 |
| Senior practitioner: looks for the deeper, more correct method | /ambitious | 0.70 |
| Skeptic: penalizes scope creep (doing more than was asked) and anything unverifiable | plain Claude | 0.74 |

- **Busy requester:** both passed 100 of 100 runs, where the original failed 33 of 100. Plain Claude's 3-line change could be approved in seconds, and its leak was already in the old code, so it isn't a new bug. But `/ambitious` also closes the leak, which this judge saw as the likely source of the next flaky test, for a slightly closer review. Its verdict: "I'd ship A."
- **Senior practitioner:** the two are equal on the core fix. Once checkout really reports failures, a half-failed cart becomes a path that really runs, and plain Claude's fix doesn't deal with the stock it leaves behind; when this judge ran the skill's rollback test against plain Claude's code, a failed order permanently used up 2 red mugs. It noted that `release()` isn't waited for, which would matter against a real, slow stock service.
- **Skeptic:** plain Claude's is the smallest correct fix and adds no new function or behaviour. `/ambitious` invented a `release()` function that the real stock service, which this file only imitates, may not have, and added a rollback nobody asked for. Its new rollback test failed only 31 of 40 runs against a version without rollback: "For a ticket about a flaky test, that is a bad thing to add."

## Takeaway

Here, `/ambitious` paid off because its recommended rung included giving back held stock, and it wrote checks that failed on the old code before changing anything. So it fixed the problem plain Claude flagged as "Something to decide later", and the hidden check H3 and the 300-trial probe confirm the difference. Plain Claude saw the same problem, said so honestly, and left it. Use the skill when a hidden mistake costs something real, like stock, money or customer orders, and you can afford about 3 times the cost and a 20-minute wait instead of a 44-second one. If you want the smallest change, one you can approve in seconds, and plan to handle the leak yourself, plain Claude's answer was correct and candid about the gap, and the skeptic judge preferred it as the smallest correct fix.

## Earlier version (v3.1)

The skill's previous version, v3.1, ran the same task against the same plain-Claude run. Version 3.2 exists because a human reviewer found the v3.1 deck looked worse than plain Claude's, and blind judges had preferred plain Claude on the deck (3–0) and the launch post (2–1). Its changes (a finished floor, no placeholders, helper scripts and backup copies kept out of the deliverable, looking at rendered pages) mostly matter for those tasks. On this code task, both versions made the same core fix.

What v3.1 did differently: its card recommended a higher rung, a check inside `npm test` that fails on `forEach(async` and needs no new tools. Its stress script counted 600 failures in 300 checkouts on the old code. It made the same `Promise.allSettled` plus `release()` fix, and added [`test/no-async-foreach.test.js`](with-v3.1/files/test/no-async-foreach.test.js). Its result card reports 0 failures in 2,000 stress checkouts and 0 in 500 `npm test` runs, and openly notes that it fixed its own judge partway through ([`response.md`](with-v3.1/response.md)). Version 3.2's card offered a similar check as rung 2, but as a lint tool that needed your OK to install, so it recommended rung 1 and, under `--go`, stopped there.

| | v3.1 | v3.2 |
|---|---|---|
| Rung taken | 2: fix, leak, `forEach` check | 1: fix, leak |
| Hidden checks | 0 / 200 suite failures; H1, H2, H3 pass | 0 / 200 suite failures; H1, H2, H3 pass |
| Failed mixed carts that lost a red mug | 0 / 300 | 0 / 300 |
| Its leak test against plain Claude's code | caught it 29 / 30 times | caught it 17 / 20 times |
| Lines changed (files) | +54 / −8 (4) | +32 / −7 (3) |
| Time · cost · tokens | 846.5 s · $0.75 · 831,121 | 1,212 s · $0.52 · 130,705 |
| Blind judges | 2–1 for v3.1 (0.57, 0.64; skeptic 0.80 for plain Claude) | 2–1 for v3.2 (0.68, 0.70; skeptic 0.74 for plain Claude) |

Both versions passed all three hidden checks. The probe and leak-test numbers come from different testers using their own scripts ([v3.1 measurements](../../evals/outcomes/results-v3.1/measurements-and-judgments.json)), so small differences between the columns don't mean much. v3.1's extra `forEach` check had its own flaws: run from any folder other than the project's top folder it failed with a "file not found" error (`ENOENT`), and it missed the pattern when `async` sat on the next line (it caught 1 of 2 in a sample file the tester wrote). The skeptic judge marked it down as a fragile test added while fixing a flaky one.

## Files

Plain Claude ([`./without`](without/)):
- [`prompt.txt`](without/prompt.txt) · [`response.md`](without/response.md)
- [`files/src/checkout.js`](without/files/src/checkout.js) · [`files/test/checkout.test.js`](without/files/test/checkout.test.js)

With /ambitious, v3.2 ([`./with`](with/)):
- [`prompt.txt`](with/prompt.txt) · [`card.md`](with/card.md) · [`response.md`](with/response.md) (local scratch paths replaced with `<scratchpad>`)
- [`files/src/checkout.js`](with/files/src/checkout.js) · [`files/src/inventory.js`](with/files/src/inventory.js) · [`files/test/checkout.test.js`](with/files/test/checkout.test.js)

With /ambitious, v3.1 ([`./with-v3.1`](with-v3.1/)):
- [`prompt.txt`](with-v3.1/prompt.txt) · [`response.md`](with-v3.1/response.md) (local scratch paths replaced with `<scratchpad>`)
- [`files/src/checkout.js`](with-v3.1/files/src/checkout.js) · [`files/src/inventory.js`](with-v3.1/files/src/inventory.js)
- [`files/test/checkout.test.js`](with-v3.1/files/test/checkout.test.js) · [`files/test/no-async-foreach.test.js`](with-v3.1/files/test/no-async-foreach.test.js)

Starting project: [`evals/fixtures/flaky-checkout/`](../../evals/fixtures/flaky-checkout/)

Raw eval output ([`evals/outcomes/results/flaky-checkout/`](../../evals/outcomes/results/flaky-checkout/)):
- without: [`prompt.txt`](../../evals/outcomes/results/flaky-checkout/without_skill/prompt.txt) · [`response.md`](../../evals/outcomes/results/flaky-checkout/without_skill/response.md) · [`diff.patch`](../../evals/outcomes/results/flaky-checkout/without_skill/diff.patch) · [`diffstat.txt`](../../evals/outcomes/results/flaky-checkout/without_skill/diffstat.txt) · [`timing.json`](../../evals/outcomes/results/flaky-checkout/without_skill/timing.json)
- with (v3.2): [`prompt.txt`](../../evals/outcomes/results/flaky-checkout/with_skill/prompt.txt) · [`response.md`](../../evals/outcomes/results/flaky-checkout/with_skill/response.md) · [`diff.patch`](../../evals/outcomes/results/flaky-checkout/with_skill/diff.patch) · [`diffstat.txt`](../../evals/outcomes/results/flaky-checkout/with_skill/diffstat.txt) · [`timing.json`](../../evals/outcomes/results/flaky-checkout/with_skill/timing.json)
- with (v3.1): [`prompt.txt`](../../evals/outcomes/results-v3.1/flaky-checkout/with_skill/prompt.txt) · [`response.md`](../../evals/outcomes/results-v3.1/flaky-checkout/with_skill/response.md) · [`diff.patch`](../../evals/outcomes/results-v3.1/flaky-checkout/with_skill/diff.patch) · [`diffstat.txt`](../../evals/outcomes/results-v3.1/flaky-checkout/with_skill/diffstat.txt) · [`timing.json`](../../evals/outcomes/results-v3.1/flaky-checkout/with_skill/timing.json)
- Hidden checks: [`flaky_check.sh`](../../evals/outcomes/checks/flaky_check.sh) · [`flaky_hidden.test.js`](../../evals/outcomes/checks/flaky_hidden.test.js) · [`flaky-hidden-checks.log`](../../evals/outcomes/results/flaky-hidden-checks.log)
- Measurements, and the judges' verdicts with the A/B labels decoded: [v3.2](../../evals/outcomes/results/measurements-and-judgments.json) · [v3.1](../../evals/outcomes/results-v3.1/measurements-and-judgments.json)
- Method: [`OUTCOMES.md`](../../evals/outcomes/OUTCOMES.md) · [`run_outcomes.sh`](../../evals/outcomes/run_outcomes.sh) · the skill (v3.2): [`SKILL.md`](../../skills/ambitious/SKILL.md)
