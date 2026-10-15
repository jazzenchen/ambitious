# Examples: the same request with and without /ambitious

Each example is one real request run twice in a fresh copy of the same small project, with the same model:

- **without:** typed as-is, the way you normally would (`fix the flaky checkout test`)
- **with:** typed after `/ambitious --go` (`/ambitious --go fix the flaky checkout test`). The skill prints its card, takes the option it recommends and does the work with no human in the loop.

Every page shows the exact prompt, the final reply and the actual files each run produced. They're published unedited, except that personal names and local paths were removed. Each page then shows what hidden checks measured on the finished work, and what three blind judges preferred.

| # | Request | What the hidden checks found | Blind judges preferred |
|---|---|---|---|
| [1](01-flaky-test/) | Fix a flaky test | Both fixed the flake. Without the skill, a failed checkout kept the stock it had reserved: **300 of 300 trials**. With it: **0**. | with, 2–1 |
| [2](02-csv-export/) | Add a CSV export button | Both produced correct, injection-safe CSV (0 bad cells out of 2,000). With the skill: also a tested module, at 2.7× the cost. | with, 2–1 |
| [3](03-qbr-deck/) | Customer section of a quarterly review deck | Both decks had 0 wrong numbers. Without: a polished deck with charts. With: a script that re-checks every figure, but no charts and placeholders left in. | **without, 3–0** |
| [4](04-launch-post/) | Product launch blog post | Without: polished, but **20 of 29 claims invented**. With: 1 unsupported claim, and the gaps are marked `[TK]`. | **without, 2–1** |

**The pattern:** `/ambitious` is more correct and less polished. Where mistakes can be measured (a bug, made-up facts), it came out ahead. Where a finished look matters (a deck, a post), the judges preferred plain Claude. It costs about 2.5× more, so use it when being wrong is expensive.

**How these were measured:** [`../evals/outcomes/OUTCOMES.md`](../evals/outcomes/OUTCOMES.md). One run per arm, model judges, and fixtures written by the author, so treat this as a sanity check, not a leaderboard. New to the card format? Read [`../docs/HOW-IT-WORKS.md`](../docs/HOW-IT-WORKS.md).
