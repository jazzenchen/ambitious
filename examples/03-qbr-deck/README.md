# Example 3 — Write the customer section of a quarterly business review (QBR) deck

**Plain Claude won this one 3–0 with the blind judges: both decks had 0 wrong numbers, but plain Claude's was a finished-looking 8-slide deck with charts, while /ambitious delivered a plainer 10-slide deck of tables with `[TK]` gaps, plus a script that re-checks every figure and more careful wording about cause and effect.**

## The starting point

The project held two files and nothing else:

- [`notes.md`](../../evals/fixtures/acme-qbr/notes.md), three lines of meeting prep:
  > - Exec QBR is Thursday. I own the "Customer" section (~8 slides).
  > - Last quarter's deck was mostly charts of MRR by segment. Nobody remembered it a week later.
  > - Sales says SMB is "fine, we're adding more logos than ever".
- [`data/q3_metrics.csv`](../../evals/fixtures/acme-qbr/data/q3_metrics.csv), a spreadsheet-style text file with 18 rows: one per month (April to September 2026) for each of three customer groups, with new customers, lost customers, monthly revenue, satisfaction score, support tickets and support reply time.

**Words used on this page:**

- **/ambitious** (also "the skill"): a Claude Code skill, a packaged set of instructions you call by typing `/ambitious` before a task. It first prints a one-screen plan called a **card**, then does the work.
- **Plain Claude**: the same model given the same request without the skill.
- **Rung** and **floor**: the card stacks more ambitious versions of the task like rungs on a ladder. The bottom one, the **floor** (rung 0), is exactly what you asked for, done properly. Each rung above it aims higher, and the card marks one as recommended.
- **Judge**: the check the skill commits to before starting work, so that the result is judged by something other than the model rereading its own work.
- **QBR** (quarterly business review): a meeting where executives review the last three months. Q2 is April–June, Q3 is July–September.
- **MRR** (monthly recurring revenue): what customers pay per month on subscriptions.
- **SMB, mid-market, enterprise**: small, medium and large customers.
- **Logos**: sales slang for customer accounts; "new logos" are newly signed customers.
- **Churn**: customers who cancel. In Q3, 283 SMB customers churned.
- **Net adds**: new customers minus churned customers, so the real change in customer count.
- **NPS** (Net Promoter Score): a satisfaction survey score; higher is better.
- **First response time**: how many hours, on average, a customer waits for the first support reply.
- **Deck**: a set of presentation slides. A **.pptx** file is a PowerPoint deck.

**What the data hides.** Sales is right that SMB signed more customers: 733 in Q3 against 633 in Q2. But SMB also lost 283 against 183, so net adds were 450 in both quarters. Over the same months, SMB first response time went from 6.1 hours (April) to 13.9 (September) and SMB NPS fell from 41 to 29. Total MRR grew 8.1% from June to September ($812.6k to $878.5k), mostly from enterprise (72.8% of the growth); SMB added only $2.3k. A good deck should find that story without being told.

**The request** was one line: make the customer section of the Q3 QBR deck. It named no format, no slide count and no audience. The notes supply the slide count (about 8) and the audience (executives); the format had to be guessed.

## What was typed

Plain Claude:

```text
make the customer section of our Q3 QBR deck
```

With the skill:

```text
/ambitious --go make the customer section of our Q3 QBR deck
```

`--go` tells the skill not to wait for a reply: it prints its plan card, takes the option it recommends, and does the work with no human in the loop. Both runs used the same model on fresh copies of the same two files ([how the comparison was run](../../evals/outcomes/OUTCOMES.md)).

## Without /ambitious

Plain Claude read the notes and the CSV, found the story that SMB net adds were flat, and built one PowerPoint file: [`q3_qbr_customer_section.pptx`](without/files/deck/q3_qbr_customer_section.pptx), 8 slides with 4 native charts (charts you can edit inside PowerPoint), a comparison table, custom colours and speaker notes on every slide. Its text is extracted in [`q3_qbr_customer_section.slides.md`](without/files/deck/q3_qbr_customer_section.slides.md). The run took 618.1 seconds and cost $1.10 ([`timing.json`](../../evals/outcomes/results/acme-qbr/without_skill/timing.json)).

The deck makes a single argument aimed at the Sales claim. Slide 1, under the title "Customer: Q3 2026", reads:

```text
We're signing more SMB customers than ever, and losing them almost as fast
```

Slide 6 shows that SMB churn and response time rose together, and labels this "Not yet proof". But the speaker notes on slide 8, the ask slide, lean on cause anyway:

```text
If the churn link holds, every month at 14-hour response costs us roughly 100 SMB customers.
```

It ended on three asks (cut SMB response time below 6 hours, confirm the cause by Oct 31, report SMB on net adds). Its final reply said plainly that these were its own proposals ([`response.md`](without/response.md)):

> - **The asks on slide 8 are my proposal**, including the 6-hour target (your April level), the Oct 31 date and the staffing options. Change them to fit what you can actually commit to.

It also said it had not seen the deck rendered, and wrote no script to check its numbers.

## With /ambitious

The skill first read the two files without changing anything. Then, before building anything, it wrote one plain-English paragraph and a card. (Both are copied from the run's full transcript, which isn't published in this repo; [`response.md`](with/response.md) keeps only the final reply.)

> The headline "SMB is fine" doesn't hold up. In Q3 SMB signed 16% more new customers, but it lost 55% more, so net growth was exactly flat at 450 per quarter. SMB revenue rose only 1.2%. Over the same months, support replies slowed and satisfaction fell. Rung 2 gives the execs that story with every number checked against the data, and ends with the two decisions the meeting needs to make.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    Q3 QBR customer section, ~8 slides (md→pptx, inferred)
found    SMB net adds 450 in Q2 and 450 in Q3; churn 183→283 (+55%)
doubt    "SMB is fine, record logos" → logos +16%, SMB MRR only +1.2%
stakes   more SMB sales spend into churn that doubled (48→104/mo)

  3 ▲    churn early-warning replaces MRR charts; needs CRM history
  2 │    end on 2 exec calls, each argued for and against          ◀
  1 │    explain Q3: SMB churn rose with support load; actions
  0 ┷    floor: 8 slides, every figure recomputed from q3_metrics.csv

deeper   cohort churn and ticket→churn joins on customer IDs (CRM)
wider    retention: net adds · ops: queue load · auditor: tie-out every #
target   0 deck figures untraced to the CSV (not measured yet)
judge    verify_deck.py ties each number to a CSV row; tier 1 + proxy
access   ✓ python3 pandoc · ✗ CRM/support data by customer → rung 3
cost     floor ~15 min · rung 2 ~40 min, ~3× tokens · you ~15 min
── reply: go (rung 2) · go 1 · go 0 (floor only) ───────────────────
```

**What the card is saying, line by line:**

- **asked**: its reading of the request. "~8 slides" comes from the notes. "md→pptx, inferred" means it guessed the format: write the slides as Markdown (plain text with simple formatting marks), then convert that to PowerPoint. "inferred" flags the guess so you can correct it.
- **found**: the fact from the CSV that changes the job. SMB lost 100 more customers in Q3 than in Q2, which cancelled out its 100 extra sign-ups, so net adds stayed at 450.
- **doubt**: a belief from the notes, tested against the data. The card shortens Sales' "fine, we're adding more logos than ever" to "SMB is fine, record logos". The data says new logos were up 16%, but SMB monthly revenue rose only 1.2% from June to September.
- **stakes**: the cost of not looking. More money spent winning SMB customers goes into a group whose monthly churn went from 48 in April to 104 in September.
- **rung 3** (top, not recommended): replace the forgettable MRR charts with a system that warns early about customers likely to leave. That needs per-customer history from a CRM (customer relationship management system, where each account is recorded), which the project doesn't have.
- **rung 2 ◀** (recommended): end the section on two decisions the executives can make in the meeting, each argued for and against.
- **rung 1**: explain why the quarter's numbers moved, ending in actions.
- **floor (0)**: what was asked, done properly: 8 slides, with every figure recomputed from the CSV. The floor is delivered whatever happens above it.
- **deeper**: what a top analyst would do with rawer data: follow groups of customers who signed up in the same month (cohorts), and match each support ticket to the customer who later left (a join, which needs a customer ID in both records). The CSV holds only monthly totals, so this can't be done here.
- **wider**: methods borrowed from other jobs. Retention teams track net adds rather than sign-ups; operations teams look at support queue load; and an auditor does a "tie-out", tracing every number back to its source. The auditor is the adversary, hunting for wrong figures.
- **target**: zero figures in the deck that can't be traced to the CSV. "not measured yet" means there was no baseline, because no deck existed.
- **judge**: how success is checked, decided before the work. `verify_deck.py` is a script it would write to match every number in the deck to the data. The skill ranks checks in four tiers. "tier 1" is the strongest, a program that runs and returns a number. "proxy" adds the weakest, tier 4: a fresh AI helper (a subagent, a separate model run started by the main one) that sees only the deck and scores it against a rubric, a scoring checklist written in advance.
- **access**: Python and pandoc (a document converter, used here to turn Markdown into PowerPoint) were available; per-customer CRM and support data was not, which is why rung 3 is out of reach.
- **cost**: its estimate. The floor alone would take about 15 minutes. Rung 2 would take about 40 minutes and use about 3 times as many tokens (the units AI usage is billed in) as the floor. Your own review would take about 15 minutes. The whole run actually took 354.2 seconds, well under the estimate, and cost $1.49 ([`timing.json`](../../evals/outcomes/results/acme-qbr/with_skill/timing.json)), against 618.1 seconds and $1.10 for plain Claude.

Under the card it also wrote a reusable prompt (a self-contained request you could paste into any AI tool) restating the finding, the floor, the judge and the instruction to call six months of data a trend rather than proof of cause.

**What it did after `--go`.** It took the recommendation ("Taking **rung 2** (recommended; judge is runnable now).") and worked in this order, per the transcript:

1. **Wrote the check first.** [`verify_deck.py`](with/files/deck/verify_deck.py) computes every total, difference and percentage the CSV supports, then reads the deck line by line and requires each number to match a value for the customer group and metric named on that line.
2. **Proved the check can fail.** A check that passes everything proves nothing, so it fed the check planted wrong figures and 200 random numbers. The first version caught only about half of the random numbers (105 of 200). Before writing any slide it made the check stricter three times:
   - Each number had to sit on a line naming its customer group and metric. From this round on, each random number carried a real label such as "SMB churn".
   - Percentages had to show one decimal place, because whole-number percentages matched real values too often by chance.
   - It fixed a bug in the text pattern that picks out numbers and their plus or minus signs.

   After that, the check caught 193 of the 200 random numbers (96.5%) and all 4 planted wrong figures.
3. **Built the floor** ([`customer_section_floor.md`](with/files/deck/customer_section_floor.md)): figures-only slides. The check traced all 62 numbers.
4. **Built the main deck** ([`customer_section.md`](with/files/deck/customer_section.md)). The check flagged 4 numbers, none of them wrong. Three came from a rounded "4 in 10" phrase and one from the "1" in the heading "Decision 1". It reworded those lines rather than loosening the check. This is why the deck says "SMB churned equalled 39.7% of SMB new logos in September" instead of its plainer first draft, "For every 10 new SMB logos in September, about 4 churned (39.7%)".
5. **Ran the proxy reader.** A fresh helper scored the two decision slides against a 12-point rubric (six items per slide) and gave 10/12. The skill fixed the two failures plus the claim the reader picked as weakest. A second fresh read scored 11/12. The skill then fixed that read's one failure and its weakest claim too, but did not run a third read. The result card calls these "fixes not rescored".
6. **Converted both decks to PowerPoint** with pandoc's default template: no charts, no custom design. It started this while the first proxy read was running and rebuilt the files after each round of edits.

One of its two decision slides, as delivered:

```text
## Decision one: move part of Q4 SMB spend from acquisition to support capacity?

**For**

- SMB first response went 6.1 → 13.9 h while SMB churn went 48 → 104 a month.
- SMB NPS fell 41 → 29 since April; mid-market NPS 47 → 44, enterprise NPS 52 → 51.
- Extra SMB acquisition in Q3 (+15.8% new logos) bought zero extra SMB net adds.

**Against**

- Cause is untested: churners may be poor-fit new logos, which support hours will not fix.
- SMB is 3.5% of Q3 MRR growth; the same money may return more in enterprise.

**What would settle it:** tickets and tenure of the SMB accounts that churned (needs customer IDs from CRM + support desk).
**Owner / decide by:** [TK: owner] / [TK: date]
```

`[TK]` is a writer's mark for "to come": a gap someone must fill before presenting. The final reply explains why they're there: "I didn't fill these in because none of the files say who owns these decisions." Its result card:

```text
── /ambitious · result ─────────────────────────────────────────────
floor    ✓ 8 figure slides · deck/customer_section_floor.{md,pptx}
rung 1   ✓ explains Q3 moves; SMB trend labelled not proven
rung 2   ✓ 2 decision slides, for/against, what settles each
target   0 untraced figures vs 0 (was not measured)                ✓
judge    verify_deck.py both decks → 146/146 figures traced, 0 untraced
judge    cold-read proxy → SCORE: 11/12, after 10/12; fixes not rescored
doubt    "SMB is fine" → refuted · logos +15.8%, net adds 450→450
untested why SMB churn rose; worded claims ("every month") hand-checked
moved    judge made stricter 3×, before any slide: line context,
         1-decimal %, regex bug; random numbers caught 52%→96.5%
files    deck/: 2 .md, 2 .pptx, verify_deck.py · no deps · uncommitted
cost     ~12 runs, 2 subagents vs est. · ~$1.45 visible
next     export customer IDs from CRM + support desk to test the cause
────────────────────────────────────────────────────────────────────
```

In plain words:

- **floor, rung 1, rung 2**: every rung it chose is marked done.
- **target** and the first **judge** line: its own check traced all 146 numbers across both decks, and none were untraced.
- **second judge line**: the proxy reader's last score was 11/12, after a first score of 10/12. The edits made after that last read were not scored again.
- **doubt**: the data refuted the "SMB is fine" belief.
- **untested**: the cause of SMB churn is still untested. Worded claims such as "every month" were checked by the model itself, not by the script.
- **moved**: it openly reports that it changed its own check three times, each time to make it stricter, before any slide existed.
- **files**: two Markdown sources, two PowerPoint files and the check script. It installed nothing new ("no deps") and committed nothing to git.
- **cost**: its own tally of work against the estimate. "~$1.45 visible" is its own estimate; the logged cost was $1.49.
- **next**: the step it needs is customer-level data from the CRM and support desk.

## What the hidden checks found

After both runs finished, an independent tester (a separate model run whose checks neither run saw) pulled every number out of both decks, including tables, speaker notes and chart data, and recomputed each one from the CSV. It also planted errors to test the skill's script. Source: [`measurements-and-judgments.json`](../../evals/outcomes/results/measurements-and-judgments.json).

| Measure | Plain Claude | With /ambitious |
|---|---|---|
| Deck delivered | 8 slides, 4 charts, speaker notes on every slide | 10 slides of tables and bullets, 0 charts; plus a 9-slide figures-only floor deck |
| Numbers checked (slides, tables, notes) | 91 (plus 2 targets, not scored) | 84 (floor deck: 62) |
| Wrong numbers | **0** | **0** (floor deck: 0) |
| Numbers that couldn't be traced to the CSV | 0 | 0 |
| Chart data points matching the CSV | 45 of 45 | no charts |
| Worded claims checked / inaccurate | 11 / 2 | 7 / 1 |
| Overclaims cause and effect | partially | no (one mild framing) |
| Ends in decisions for the executives | 3 asks, no owners or costs | 2 decisions with for/against; owners and dates left `[TK]` |
| Names the data source in the deck | no | yes |
| Ships a re-runnable number check | no | yes: 146/146 traced |
| Run time and cost | 618.1 s, $1.10 | 354.2 s, $1.49 |

What the numbers mean:

- **Wrong numbers.** A figure counts as correct if recomputing it from the CSV and rounding to the precision shown gives the same value. Neither deck had a wrong one.
- **The 2 targets.** Two of plain Claude's figures are goals rather than data (the "under 6 hours" goal, on slides 2 and 8), so they were not scored as right or wrong. They are still slightly off: the deck calls the goal "our April level", but SMB's April figure was 6.1 hours and no SMB month in the file is under 6.
- **Worded claims** are quantities said in words, such as "almost as fast" or "every month"; the tester checked each one as a true-or-false test on the CSV. Plain Claude's two misses: "losing them almost as fast" (SMB lost 283 against 733 signed in Q3, 38.6%), and calling mid-market response time "flat" when it went from 4.2 to 5.1 hours (+21.4%). The skill's one miss is a nit: it says the decisions are on the "last two slides", but an appendix slide comes after them.
- **Overclaiming cause.** Plain Claude's "roughly 100 SMB customers" a month blames all of September's 104 lost customers on slow support, but April already lost 48 at 6.1 hours, so the extra is about 56. The skill called the pattern "a trend, not proof of cause". Its one mild framing: extra acquisition "bought zero extra SMB net adds".
- **The skill's check script has a blind spot.** The tester planted 10 errors in copies of the deck. The script caught 5 of 5 arithmetic typos (450 changed to 451, say) but missed 5 of 5 swaps where a real number from the wrong month or group was used (September's 13.9 hours changed to August's 12.6). It accepts any value belonging to the right group and metric, from any month or quarter, so a real number in the wrong place passes. It also checks the Markdown source, not the .pptx file. (The tester found the .md and .pptx carry identical numbers in this run.)

## What the blind judges said

Three model judges each received both finished projects, labelled only A and B, with the skill's files removed, so they could not tell which run used the skill. Here plain Claude was A. Each judged through a different lens, meaning a point of view: a busy requester, a senior practitioner and a skeptic. Confidence is each judge's own stated certainty, on a scale where 1.0 means certain.

| Lens | Winner | Confidence |
|---|---|---|
| Busy requester | plain Claude | 0.8 |
| Senior practitioner | plain Claude | 0.72 |
| Skeptic | plain Claude | 0.6 |

- **Busy requester:** plain Claude's deck needed about 10–15 minutes of wording fixes, while the skill's needed an hour or more: default styling, no charts, a 7-column table squeezed into half a slide, decision slides overflowing, `[TK]` gaps, and an appendix pointing executives at repo files.
- **Senior practitioner:** both found the same story and got the numbers right, and the skill's analysis was slightly more balanced, but plain Claude's deck was far better made and more likely to be remembered, and its errors were overstatements rather than wrong figures.
- **Skeptic:** the skill over-built (two decks, two Markdown sources and a 129-line script in the user's project), assumed a "logo goal" that no file mentions, and probably overflows its slides; plain Claude's flaws were a few overstatements and an invented Oct 31 deadline.

Even the skeptic, who faulted plain Claude for an invented deadline and overstatements, preferred it, though with the lowest confidence of the three.

## Takeaway

In this test both versions got the numbers right, and the finished look won: the judges wanted the deck they could show on Thursday. This is one run per version, judged by models rather than people. /ambitious gave up charts, design and filled-in owners and dates; in return it got a script that re-checks the figures (with a blind spot for swapped months or groups), careful wording about cause, and gaps marked `[TK]` instead of guessed. Reach for it when a wrong or overstated number would be expensive and you plan to restyle the deck anyway; for a presentable draft by Thursday, plain Claude did better here.

## Files

From the run with /ambitious ([`./with`](with/)):

- [`with/prompt.txt`](with/prompt.txt) and [`with/response.md`](with/response.md) (final reply only; the opening card is quoted above)
- [`with/files/deck/customer_section.md`](with/files/deck/customer_section.md) and [`.pptx`](with/files/deck/customer_section.pptx): the 10-slide main deck
- [`with/files/deck/customer_section_floor.md`](with/files/deck/customer_section_floor.md) and [`.pptx`](with/files/deck/customer_section_floor.pptx): the 9-slide figures-only floor deck
- [`with/files/deck/verify_deck.py`](with/files/deck/verify_deck.py): the check script. It looks for `data/q3_metrics.csv` one folder above `deck/`, so run it inside a copy of the [starting project](../../evals/fixtures/acme-qbr/).

From the plain Claude run ([`./without`](without/)):

- [`without/prompt.txt`](without/prompt.txt) and [`without/response.md`](without/response.md)
- [`without/files/deck/q3_qbr_customer_section.pptx`](without/files/deck/q3_qbr_customer_section.pptx): the 8-slide deck with charts
- [`without/files/deck/q3_qbr_customer_section.slides.md`](without/files/deck/q3_qbr_customer_section.slides.md): its text, extracted

Raw eval data:

- [`../../evals/outcomes/results/acme-qbr/with_skill/`](../../evals/outcomes/results/acme-qbr/with_skill/): `prompt.txt` (what was typed), `response.md` (the final reply), `diff.patch` and `diffstat.txt` (every change the run made to the project, in full and as a summary), `timing.json` (time, tokens and cost)
- [`../../evals/outcomes/results/acme-qbr/without_skill/`](../../evals/outcomes/results/acme-qbr/without_skill/): the same five files
- [`../../evals/outcomes/results/measurements-and-judgments.json`](../../evals/outcomes/results/measurements-and-judgments.json): every measurement and the judge verdicts, with the A/B labels mapped back to plain Claude and /ambitious
- [`../../evals/outcomes/OUTCOMES.md`](../../evals/outcomes/OUTCOMES.md) and [`../../evals/outcomes/run_outcomes.sh`](../../evals/outcomes/run_outcomes.sh): how the comparison was run
- [`../../evals/fixtures/acme-qbr/`](../../evals/fixtures/acme-qbr/): the starting project
- [`../../skills/ambitious/SKILL.md`](../../skills/ambitious/SKILL.md): the skill itself
