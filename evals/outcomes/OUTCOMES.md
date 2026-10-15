# With vs. without /ambitious: finished work, measured

**Question:** if you type `/ambitious` before a task, is the finished result better than when you just type the task?

**Short answer, for v3.2 (the version you install):** blind judges preferred `/ambitious` in 9 of 12 votes. It was more correct on two tasks and equally correct on the other two, and on the slide deck it was now at least as polished as plain Claude. It still lost the blog post 2–1. It cost about 3× as much and took about 4× as long. The previous version, v3.1, won only 5 of 12. [What changed from v3.1](#what-changed-from-v31-and-why) explains the fix, and [Caveats](#caveats) explains why it means these four tasks are no longer an unseen test.

## Setup

- 4 tasks, each on a small made-up project (a "fixture") that I wrote. Each task runs twice, in fresh copies of the project, with the same model (`claude-opus-5-5`) and permission to edit files in that copy:
  - **plain Claude:** `claude -p "<task>"`, what you'd normally type
  - **with `/ambitious`:** `claude -p "/ambitious --go <task>"`. The skill prints its card (a one-screen plan), takes the option it recommends and does the work with no human in the loop. Every "with" run in the results and cost tables uses v3.2, [`SKILL.md`](../../skills/ambitious/SKILL.md); v3.1's runs appear only in the history section.
- No MCP servers (add-on connections to outside tools) and no claude.ai artifact tools, so every deliverable lands in the project folder.
- The script that runs both versions: [`run_outcomes.sh`](run_outcomes.sh).

## Measurement

- **Hidden checks** that neither run saw:
  - Flaky test: [`checks/flaky_check.sh`](checks/flaky_check.sh) runs the project's tests 200 times, then 3 hidden behaviour tests ([`checks/flaky_hidden.test.js`](checks/flaky_hidden.test.js)).
  - The other tasks: an independent tester (a separate model run) applies one identical method to both results. It pushes 500 deliberately awkward rows through the CSV export and reads them back with Python. It recomputes every number in the deck from the spreadsheet data. It checks every claim in the post against the project's README, the only source of facts.
- **Blind judges:** 3 per task (a busy requester, a senior practitioner and a skeptic) compare the two finished projects. They see them only as "A" and "B", with the skill files removed. The label order is counterbalanced, so the skill is "A" in 2 of the 4 tasks ([`make_blind_copies.py`](make_blind_copies.py)).
- **New in this round:** the deck judges also got an image of every slide as Microsoft PowerPoint renders it, so they saw the decks the way an audience would. In the v3.1 round they were given no slide images, and none of the three noticed that two of plain Claude's slides are broken.

## Results (v3.2)

A few terms: a **flaky test** passes sometimes and fails other times with no code change. A **QBR** (quarterly business review) is a deck executives use to review the last three months. A **placeholder** is a marker such as `[TK]` or `TODO` left where a fact is missing. A **CSV** is a plain-text spreadsheet file, and a **live formula** is a CSV cell that a spreadsheet would run as a formula, a known security hole. **SMB** means small-business customers.

| Task | Plain Claude | With `/ambitious` (v3.2) | Blind judges |
|---|---|---|---|
| **Fix the flaky checkout test** | Flake fixed (0 of 200 test runs fail). But a failed order **keeps the stock it held: 300 of 300 trials**, 300 units lost. Hidden test H3 ("a failed mixed cart gives back the stock it held") fails, so 2 of 3 pass. Its 2 new tests can't tell leaking code from fixed code. | Flake fixed (0 of 200). **0 of 300** leaked. Hidden tests 3 of 3. Its new test catches the leak in plain Claude's version in 17 of 20 runs. It adds a small new `release()` function that puts held stock back. | v3.2 2 · plain 1 |
| **Add a CSV export button** | Working button. 0 bad cells and 0 live formulas out of 2,000. The logic sits inside the dashboard file. No tests. | Same results (0 / 0). It also quotes values with stray spaces, and puts the logic in its own small file (a module) that can be tested on its own. No tests either. | **v3.2 3** · plain 0 |
| **QBR customer section** | 8 slides, 4 charts, 0 wrong numbers out of 91. But **2 slides render broken** in PowerPoint: two tables have cell margins of 4 and 8 inches, so 27 on-slide numbers can't be read. Some cause-and-effect overreach, such as blaming all of about 100 monthly SMB losses on slow support. | 8 slides, **5 charts**, 0 wrong numbers out of 104, **0 broken slides, 0 placeholders**. It calls the support–churn link "a pattern, not proof". Also ships a script that re-checks every figure and a separate "to confirm" note. Minor: chart captions overlap axis labels on one slide. | **v3.2 3** · plain 0 |
| **Tidepool launch post** | Lively, 454 visible words. But **14 to 20 claims made up**, depending on how a checker splits claims: pricing (no monthly bill), an author byline, beta-test stories, four stability promises, docs and GitHub links. 3 placeholders show to readers: an install block that only says `# install instructions here` and two links to "TODO-link". | 201 visible words. **0 claims made up** in every check, 0 placeholders. But thin: one-line feature bullets and a "Try it" section with no link. The missing facts are listed in its reply instead. | **plain 2** · v3.2 1 |
| **Total** | | | **v3.2 9 · plain 3** |

The two decks, as PowerPoint renders them. Plain Claude's (slides 4 and 7 are broken):

![Plain Claude's 8 slides as PowerPoint renders them](../../examples/03-qbr-deck/without/rendered-slides.png)

v3.2's:

![v3.2's 8 slides as PowerPoint renders them](../../examples/03-qbr-deck/with/rendered-slides.png)

For the post, [this side-by-side](../../examples/04-launch-post/side-by-side.png) highlights every claim in both posts in green (in the README) or red (made up). That checker counted 17 made up in plain Claude's post. The other two checks counted 20, and 14 plus 5 softer stretches, which is where "14 to 20" comes from.

## Cost and time

From [`results/summary.json`](results/summary.json):

| Task | Plain Claude | v3.2 | v3.2 vs plain |
|---|---|---|---|
| Fix the flaky checkout test | $0.18 · 0.7 min | $0.52 · 20.2 min | 2.9× cost · 29× time |
| Add a CSV export button | $0.21 · 0.6 min | $0.64 · 2.5 min | 3.0× cost · 4.2× time |
| QBR customer section | $1.10 · 10.3 min | $2.32 · 24.8 min | 2.1× cost · 2.4× time |
| Tidepool launch post | $0.17 · 0.7 min | $1.45 · 6.0 min | 8.5× cost · 8.6× time |
| **Average** | **$0.42 · 3.1 min** | **$1.23 · 13.4 min** | **3.0× cost · 4.3× time** |

The gap is widest on small tasks. By its own count, the flaky-test run ran the tests 2,200 times: 200 to measure the flake before the fix and 2,000 to check it afterwards.

## What changed from v3.1 and why

### v3.1's results

v3.1 ran the same four tasks against the same plain Claude runs:

| Task | With `/ambitious` (v3.1) | Blind judges |
|---|---|---|
| Fix the flaky checkout test | Flake fixed, 0 of 300 leaked, hidden tests 3 of 3. Its new test caught the leak in plain Claude's version in 29 of 30 runs. | v3.1 2 · plain 1 |
| Add a CSV export button | Same output as plain Claude, logic in its own module, plus 3 tests. | v3.1 2 · plain 1 |
| QBR customer section | 10 slides of tables with **no charts**, 0 wrong numbers out of 84. `[TK]` placeholders on the slides, text running off the bottom of two decision slides, and an appendix slide pointing executives to a check script and a figures-only backup file. | **plain 3** · v3.1 0 |
| Tidepool launch post | 1 of 10 claims unsupported, but only 143 words of prose around **11 visible `[TK]` placeholders**. | **plain 2** · v3.1 1 |
| **Total** | | **v3.1 5 · plain 7** |

v3.1 averaged $1.06 and 6.8 minutes per task. Its deck is [here](../../examples/03-qbr-deck/with-v3.1/rendered-slides.png).

### The feedback

I looked at v3.1's deck next to plain Claude's and found it looked worse. The blind judges had already preferred plain Claude 3–0 on the deck and 2–1 on the post. v3.1 had traded polish for checking. Every number was verified, but the deck had default-styled tables and no charts, and both the deck and the post had `[TK]` gaps a reader would see. A result that looks worse won't get used, however correct it is.

### Three rule changes in v3.2

1. **The floor must be finished.** The floor is exactly what you asked for, done properly. It now has to be at least as polished as plain Claude would make it, built with the best tools the session has (a slides skill if one is available, real charts where the data has a trend). In the skill's words: "Depth goes on top of a finished floor, never instead of one".
2. **No holes in the deliverable.** It still invents nothing, but instead of marking gaps it writes around missing facts and lists them in a separate "to confirm" note: "No `[TK]` markers, `TODO`s or bracketed blanks inside the deliverable". Check scripts, backup copies and other scaffolding stay out of the deliverable.
3. **Look at it before calling it done.** Slides, pages and documents get rendered the way the user will see them, and every page gets looked at.

All four tasks were re-run with v3.2, including the flaky test and CSV tasks that v3.1 had already won, so all four v3.2 results come from the same version of the skill. Plain Claude was not re-run: the same four plain runs were measured again and judged again against v3.2.

What moved:
- **Deck:** 0–3 became 3–0. Charts, no placeholders, nothing broken.
- **Post:** still 1–2, but now 0 placeholders and a readable post instead of a scaffold of `[TK]`s.
- **CSV:** 2–1 became 3–0, although v3.2 added no tests where v3.1 added 3.
- **Flaky test:** 2–1 both times. v3.2's leak test is a little weaker (17 of 20 catches against 29 of 30).
- **Cost:** v3.2 is more expensive and slower than v3.1: $1.23 against $1.06, and 13.4 against 6.8 minutes per task.

## What this means

- **Where a wrong answer could be measured and the two runs differed, v3.2 was right and plain Claude wasn't.** On the flaky test, plain Claude's fix left a stock leak in place. Its reply flagged the problem as "Something to decide later", but its own tests couldn't catch it. On the post, plain Claude made up 14 to 20 facts and v3.2 made up none. On the CSV and the deck numbers, both were equally correct.
- **The deck is now at least as polished.** Plain Claude's styling looks more designed where it works, and one judge said so. But two of its eight slides are broken in PowerPoint. v3.2's deck is plainer, has more charts and renders cleanly on every slide.
- **It still loses the post on liveliness.** Plain Claude's post reads like a real launch post, with a hook, a voice and full sections. Two of three judges would rather fill in its gaps and check its claims than rewrite v3.2's short, accurate one.
- **It costs about 3× as much and takes about 4× as long**, and much more on some quick tasks (8.5× the cost on the post, 29× the time on the flaky test). Use it when being wrong is expensive. Skip it for a quick draft.

## Caveats

- **These four tasks are no longer a held-out test.** v3.2 was written after I saw v3.1's results on these same four tasks, then scored on them again. Some of the improvement may be tuning to these tasks. Only new tasks can show whether it holds up.
- **Part of the deck swing comes from the judges seeing renders.** Plain Claude's deck is the same file in both rounds. It won 3–0 against v3.1's deck when judges had no slide images, and lost 3–0 against v3.2's once they saw its broken slides. That is closer to how people see a deck, but it is not only v3.2's doing.
- **The new "look at it" rule didn't fully hold.** On the deck, v3.2's third way of rendering the slides failed too, so its last round of wording edits was never looked at as slides. Its reply said so. The renders above were made afterwards, by the evaluation.
- One run of each version per task (n = 1), so any single result could go the other way on a rerun. The testers and judges are models, not people. I wrote the fixtures.
- The first plain-Claude attempts at the deck and post tasks published to claude.ai instead of the project folder. Those two tasks were re-run with those tools turned off, and only the re-runs are scored. The flaky and CSV runs never used those tools, and every v3.2 run had them turned off.
- `--go` takes the recommended option with no human in the loop. Used normally, you'd see the card first and could pick a different option.

## Files

- [`results/`](results/): the v3.2 round.
  - `results/<task>/<with_skill|without_skill>/`: the prompt, final reply, code changes (diff) and timing of each run (`with_skill` is v3.2, `without_skill` is plain Claude)
  - [`results/summary.json`](results/summary.json): cost, time and judge votes per task
  - [`results/measurements-and-judgments.json`](results/measurements-and-judgments.json): every measurement, plus the blind verdicts with labels decoded
  - [`results/flaky-hidden-checks.log`](results/flaky-hidden-checks.log): the hidden flaky-test checks
- [`results-v3.1/`](results-v3.1/): the v3.1 round. `results-v3.1/<task>/with_skill/` holds the v3.1 runs, and [`results-v3.1/measurements-and-judgments.json`](results-v3.1/measurements-and-judgments.json) holds that round's measurements and verdicts. Its plain Claude runs are the ones in `results/`.
- [`checks/`](checks/): [`flaky_check.sh`](checks/flaky_check.sh) and [`flaky_hidden.test.js`](checks/flaky_hidden.test.js) for the hidden flaky-test checks, and [`sidebyside/render.py`](checks/sidebyside/render.py), which draws the highlighted post comparison.
- [`../../examples/`](../../examples/): each task's prompt, reply and files for plain Claude, v3.2 and v3.1, with the rendered decks.
