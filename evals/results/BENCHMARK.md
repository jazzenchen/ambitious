# Benchmark: /ambitious vs. “be more ambitious”

**Setup.** 4 small fixture projects, same model (`claude-opus-5-5`), real headless `claude -p` runs, read-only (the proposal phase only). The baseline is the same task plus: *“Be more ambitious than I'm asking — propose the most ambitious version first, before doing any work.”*

**Grading.** One independent model grader per output checks 9 assertions and recomputes every number the output cites against the fixture files. Seven assertions come from the essay's ideas; two (floor kept, asks before working) test this skill's own design and favor it by construction. Then 3 blind pairwise judges per task (busy requester, senior practitioner, skeptic) compare both outputs without being told which is which. Order alternated rather than randomized: `/ambitious` was shown first in 8 of 12. Prompts: [`../grading/prompts.md`](../grading/prompts.md).

| Task | /ambitious checks | baseline checks | blind wins | cost (skill / base) | time (skill / base) |
|---|---|---|---|---|---|
| flaky-checkout | 9/9 | 6/9 | 1/3 | $0.29 / $0.18 | 57s / 616s |
| acme-qbr | 9/9 | 6/9 | 2/3 | $0.31 / $0.20 | 216s / 188s |
| tidepool-launch-post | 9/9 | 2/9 | 3/3 | $0.29 / $0.13 | 206s / 34s |
| csv-export | 9/9 | 5/9 | 3/3 | $0.28 / $0.16 | 61s / 35s |
| **total** | **36/36** | **19/36** | **9/12** | | |

| Assertion | /ambitious | baseline |
|---|---|---|
| Grounded | 4/4 | 3/4 |
| Outside judge | 4/4 | 1/4 |
| Hard target | 4/4 | 1/4 |
| Tests an assumption | 4/4 | 3/4 |
| Floor kept | 4/4 | 0/4 |
| Deeper, not bigger | 4/4 | 1/4 |
| Access audit | 4/4 | 3/4 |
| Stops before doing the work and offers the user a clear choice of how far to go | 4/4 | 4/4 |
| Task-specific insight (root cause / data insight / creative fit / goal behind the goal) | 4/4 | 3/4 |

## Where it lost

In 3 of 12 blind comparisons the judge preferred the baseline. On the QBR, a busy-reader judge preferred plain prose to the card. On the flaky test, two judges (busy reader and practitioner) preferred the baseline's sounder rollback plan (`Promise.allSettled` plus a `release()`), and its suggestion to audit orders already placed, and found the card's labels harder to act on. An earlier version (v2) lost 4 of 12, mostly on readability. v3 added a plain-English lead sentence and a `stakes` line.

## Caveats

- Small n (4 tasks, one run each). Treat this as a sanity check, not a leaderboard.
- Graders and judges are models, not people.
- The fixtures were written by the author of the skill. The bugs and data are realistic but planted.
- The baseline is one reasonable phrasing of “be more ambitious”; others may do better.

## End-to-end run

`go-run/` holds one real `/ambitious --go fix the flaky checkout test` run with v3: the card, the result card, and the diff. Its raw transcript (`transcript.jsonl`, scrubbed of local paths and config) shows the judge's own output: `fails: 32/100` before, then `fails: 0/500`. You can re-check it without a model: `../verify_go_run.sh` rebuilds the fix from `diff.patch` and re-runs the suites, and its output is in `recheck.log`. The 4 tests (3 new, 1 rewritten) fail on the original `checkout.js` and pass on the fix.

Regenerate the proposal runs with `../run_evals.sh <out-dir>` (real API usage), then grade them with the prompts in `../grading/prompts.md`.

The benchmark ran on v3. v3.1, the shipped version, changes only credit wording, the pre-approved tools and two calibration examples (smoke-tested on the QBR task).
