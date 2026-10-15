# Examples: the same request with and without /ambitious

Each example is one real request run twice in a fresh copy of the same small project, with the same model:

- **without:** typed as-is, the way you normally would (`fix the flaky checkout test`)
- **with:** typed after `/ambitious --go` (`/ambitious --go fix the flaky checkout test`). The skill prints its card, takes the option it recommends and does the work with no human in the loop.

Every page shows the exact prompt, the final reply and the actual files each run produced. They're published unedited, except that personal names and local paths were removed. Each page then shows what hidden checks measured on the finished work, and what three blind judges preferred.

| # | Request | What the hidden checks found | Blind judges preferred |
|---|---|---|---|
| [1](01-flaky-test/) | Fix a flaky test | Both fixed the flake. Without the skill, a failed checkout kept the stock it reserved: **300 of 300 trials**. With it: **0**. | with, 2–1 |
| [2](02-csv-export/) | Add a CSV export button | Both produced correct, injection-safe CSV (0 bad cells out of 2,000). | with, 3–0 |
| [3](03-qbr-deck/) | Customer section of a quarterly review deck | Both decks had 0 wrong numbers. Plain Claude's has **2 slides that render broken** in PowerPoint. v3.2's has 5 charts and nothing broken. | with, 3–0 |
| [4](04-launch-post/) | Product launch blog post | Without: livelier, but **14–20 claims made up**. With: shorter, **0 made up**. [See it highlighted](04-launch-post/side-by-side.png). | without, 2–1 |

**The pattern:** with v3.2, `/ambitious` is more correct and at least as polished on 3 of the 4 tasks. It still loses the blog post on liveliness. It costs about 3× more and takes about 4× longer, so use it when being wrong is expensive. (v3.1 lost the deck 0–3 because it skipped polish. Each page explains what changed.)

**How these were measured:** [`../evals/outcomes/OUTCOMES.md`](../evals/outcomes/OUTCOMES.md). One run per arm, model judges, and fixtures written by the author, so treat this as a sanity check, not a leaderboard. New to the card format? Read [`../docs/HOW-IT-WORKS.md`](../docs/HOW-IT-WORKS.md).
