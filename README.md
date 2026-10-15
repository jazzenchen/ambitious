# ▲ /ambitious

**Type `/ambitious` before a task. Get the version you didn't think to ask for: grounded in your real files, checked by something other than the model, with your original ask as the guaranteed floor.**

An unofficial Claude Code skill inspired by Felix Rieseberg's essay [How to be more ambitious: A tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).

![/ambitious demo: the real card for “fix the flaky checkout test”](assets/demo.gif)

*The card text is verbatim from a real run; the terminal is re-drawn as an animation. The full 20-second cut, with the result card, is [`assets/hero.mp4`](assets/hero.mp4).*

## Before / after (real run)

```text
› /ambitious --go fix the flaky checkout test
```

> Checkout isn't waiting for stock to be reserved, so the test only fails when the fake network is slow (about 3 runs in 8). The same bug also lets people order sold-out items. I'm taking rung 1: it fixes both and proves the fix with a stress loop.

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

With `--go` it went straight on to the recommended rung, then printed:

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

The test wasn't flaky; the code was, and the same bug let sold-out items be ordered. Awaiting the reservations (the floor) fixed both. Rung 1 added releasing partial holds. It stopped there, because the lint rung needed a dev dependency the card had asked about. It doesn't pretend about data it can't see: `✗ order data, so past damage can't be counted`.

**Checked without a model:** [`evals/verify_go_run.sh`](evals/verify_go_run.sh) rebuilds the fix from the shipped diff. [Its log](evals/results/go-run/recheck.log): the original suite fails about 1 run in 3, and the fixed suite failed 0 of 300 runs. The 4 tests (3 new, 1 rewritten) fail on the old `checkout.js` and pass on the fix. The run's raw transcript, stress script and diff are in [`evals/results/go-run/`](evals/results/go-run/).

## Install

```bash
npx skills add jazzenchen/ambitious
```

Or copy the one file yourself:

```bash
curl -fsSL https://raw.githubusercontent.com/jazzenchen/ambitious/main/skills/ambitious/SKILL.md --create-dirs -o ~/.claude/skills/ambitious/SKILL.md
```

Or install it as a Claude Code plugin (the command becomes `/ambitious:ambitious`):

```text
/plugin marketplace add jazzenchen/ambitious
/plugin install ambitious@ambitious
```

**claude.ai / Claude desktop:** download `ambitious.zip` from [Releases](https://github.com/jazzenchen/ambitious/releases) and upload it under Customize → Skills.

## Use

```text
/ambitious fix the flaky checkout test     # card first, nothing changes yet
/ambitious                                  # infers the task you're working on
go · go 2 · go 0                            # pick a rung (0 = just what you asked)
/ambitious --go add CSV export              # card, then straight to the recommended rung
```

## What it does

1. **Looks before it leaps.** About 10 read-only calls at your real files and data, plus an inventory of what this session can actually reach: CLIs, MCP servers, and credentials by name only.
2. **Prints one sentence and one card.** The sentence is plain English. The card holds a finding from your own material, a belief worth doubting, what's at stake, a ladder of rungs above your ask, a hard target, an outside judge, missing access and a cost line. It fits in a screenshot.
3. **Builds the judge first** after you say go, and proves the judge can fail before touching anything.
4. **Secures the floor.** You always get exactly what you asked for; everything above it only adds.
5. **Prints a receipt.** Every number comes from a judge run, misses get a ✗ and a reason, and `untested` means untested.

It applies the essay's three directions:
- **Altitude:** the goal behind the goal.
- **Depth:** the instruments and raw material the best in the field would use.
- **Range:** methods borrowed from other fields, never role-play.

The never-grade-your-own-homework rule is the essay's. Several things are this skill's own: the guaranteed floor, the access audit, the cost line, the receipt, and saying so when a task doesn't deserve a climb.

## Does it actually help? With vs. without, measured

Same 4 tasks, same model. Each was run once as you'd normally type it and once as `/ambitious --go <task>`. The finished work was then measured with hidden checks neither run saw, and compared by blind judges.

| Task | Without the skill | With `/ambitious` |
|---|---|---|
| Fix a flaky test | Flake fixed, but **failed carts leak stock in 300/300 trials** | Flake fixed, **0/300** leaked, and a test that catches the leak |
| Launch blog post | Polished, but **20 of 29 claims invented** | 1 unsupported claim. The gaps are marked `[TK]` instead of made up. |
| CSV export button | Correct and injection-safe | Same quality, plus a tested module |
| QBR deck section | 0 wrong numbers, with charts and polish | 0 wrong numbers, a figure-check script, no charts, `[TK]` owners |
| Blind judges preferred | **7 of 12** | 5 of 12 |
| Avg cost / time | $0.42 · 3 min | $1.06 · 7 min |

In short, it's more correct and less polished. Where correctness was measurable (the code and the facts), `/ambitious` came out ahead. Where polish mattered (the deck and the post), the judges preferred plain Claude's finished look, flaws included. Use it when being wrong is expensive, and skip it for a quick draft. The full report, hidden tests and every output are in [`evals/outcomes/OUTCOMES.md`](evals/outcomes/OUTCOMES.md). Caveat: one run per arm, model judges, fixtures I wrote.

### Proposal quality vs. telling Claude to "be more ambitious"

Proposal phase only, before any work. `/ambitious` is compared with the same prompt plus *"Be more ambitious than I'm asking — propose the most ambitious version first, before doing any work."*

| | `/ambitious` | "be more ambitious" |
|---|---|---|
| Names an outside judge (not self-grading) | 4/4 | 1/4 |
| Sets a hard numeric target | 4/4 | 1/4 |
| Keeps your ask as a guaranteed floor | 4/4 | 0/4 |
| Goes deeper, not bigger | 4/4 | 1/4 |
| Grounded in your own files | 4/4 | 3/4 |
| Tests an assumption in the ask | 4/4 | 3/4 |
| Asks before doing the work | 4/4 | 4/4 |
| Says what access it lacks | 4/4 | 3/4 |
| Task-specific insight (root cause, data, fit) | 4/4 | 3/4 |
| **All 9 checks** | **36/36** | **19/36** |
| Preferred by blind judges | **9 of 12** | 3 of 12 |

Seven checks come from the essay's ideas. Two test this skill's own design (the floor, asking first), so they favor it by construction. Independent model graders recomputed every number each output cited. Blind judges weren't told which output was which; order alternated, and `/ambitious` went first in 8 of 12.

**Where it lost (3/12):** on the QBR, a busy-reader judge preferred plain prose to the card. On the flaky test, two judges preferred the baseline's sounder rollback plan (`Promise.allSettled` plus `release()`) and its suggestion to audit past orders, and found the card's labels harder to act on.

**Caveats:** small n (4 tasks), model graders, and fixtures written by me. Treat this as a sanity check, not a leaderboard. The benchmark ran on v3; v3.1, which you install, only tightens credit wording, the pre-approved tools and two examples.

The full table, every output and every grade are in [`evals/results/BENCHMARK.md`](evals/results/BENCHMARK.md), and the grader and judge prompts are in [`evals/grading/prompts.md`](evals/grading/prompts.md). Regenerate the runs with `evals/run_evals.sh <out-dir>`, which costs real API usage.

## Cost, honestly

- **Finished work:** in the with/without benchmark, `/ambitious --go` averaged $1.06 and 7 minutes per task. Plain Claude averaged $0.42 and 3 minutes, so the skill costs about 2.5× more.
- **Card only:** printing the card costs about $0.29.

Most of the extra goes to the skill's instructions, writing the judge before the work and running it. If your task is a rename, `/ambitious` will tell you not to bother.

## Credit

- Paraphrased from Felix Rieseberg's essay:
  - the kinds of ambition and the techniques under each: the depth questions and real instruments, unreasonable targets, challenging beliefs, new knowledge, the outside judge, and fields rather than role-play
  - the review and crash-free examples

  Read it: https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/
- "Rewrite the deliverable as verbs" comes from Tom Kelley and Jonathan Littman, *The Art of Innovation*, via the essay.
- The card, the rungs and floor, the access audit, the cost line, the stop rules and the receipt are this project's own.

**Unofficial.** Not affiliated with or endorsed by Felix Rieseberg or Anthropic. Claude and Claude Code are products of Anthropic.

## License

MIT
