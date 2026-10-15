---
name: ambitious
description: "Unofficial skill based on Felix Rieseberg's essay on ambition with models. For one task, code or not (a fix, a deck, a launch post), it looks read-only at the real files, data and what this session can reach (CLIs, MCP servers, credentials by name), then prints a screenshot-sized card: a ladder of rungs above the original ask, which stays the guaranteed floor, with a finding from the user's own material, a hard target, a runnable outside judge, what to connect and a cost line. It builds only after the user says go. Use when the user types /ambitious or explicitly asks to think bigger, be more ambitious, aim higher or 10x the ambition of a task. Do not use for ordinary requests just because they are large, hard or important."
argument-hint: "[task, or blank for current work] [--go [N]]"
allowed-tools:
  - Bash(git status:*)
  - Bash(git log --oneline -20)
  - Bash(git diff --stat)
  - Bash(git diff)
  - Bash(ls:*)
  - Bash(command -v:*)
  - Bash(gh auth status)
---

# /ambitious

Show the user, on one card, the version of their task they didn't think to ask for: grounded in their real files, judged by something other than you, with their original ask as the guaranteed floor. Change nothing until they pick a rung.

Inspired by Felix Rieseberg, "How to be more ambitious: A tutorial for humans with models": https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/ — the kinds of ambition and the techniques under each (the depth questions and real instruments, unreasonable targets, challenging beliefs, new knowledge, the outside judge, nouns to verbs, fields rather than role-play), plus the review and crash-free examples, are paraphrased from it; the card, rungs and floor, access audit, cost line, stop rules and receipt are this skill's own.
Unofficial — not affiliated with or endorsed by Felix Rieseberg or Anthropic.

**Task:** $ARGUMENTS

- **`--go` or `--go N`:** strip it from the task. Print the card and prompt, then go straight to step 4 on the recommended rung, or on the highest rung at or below N whose judge you can run now; a no-climb card always means the floor. Say in one line under the card which rung you took. `--go` needs task text: if the task was inferred, ignore it, print the card and wait. It never covers the ask-first list in step 4.
- **Empty task:** use, in order, the latest unfinished request in the conversation, the uncommitted diff, then the last commit, and mark `asked` with `(inferred)` plus anything already done. If none applies, print only `asked    nothing to infer · reply with the task` inside the card frame and stop.
- **Anything unclear:** don't ask before the card; the card is the question. Put your assumption in `asked` or `doubt`. A wrong guess costs the user one word to fix; a question costs a round trip before they have seen anything.

## Why a card, and why this order

- You already deliver speed, the same work done faster. This skill pushes the essay's other three directions: altitude (the outcome the task serves), depth (how the field's best would do it, one layer down) and range (methods from other fields).
- This skill's premise: telling a model to be ambitious mostly yields bigger plans and confident summaries. Ambition becomes real with three things: access to the real material, a check that isn't you, and an honest account of cost and misses. Each step below supplies one of them.
- People judge a plan in seconds. A card built on numbers from their own files earns a go and gets shared; a long proposal gets skimmed. Choosing the bigger scope is their call, never yours.

## 1. Look: read-only, two batches of parallel calls, about 10 calls

Don't narrate while you look. A slow card gets skipped, and deep investigation belongs after go. Read-only means reading files, `git status/log/diff`, `ls`, `command -v`, `gh auth status`, a quick one-liner that reads a local data file and writes nothing, and a connector read of material the task names. No edits, installs, builds, test runs (suites write fixtures and caches) or other network calls. The frontmatter pre-approves a few of these commands to spare permission prompts; it is not a sandbox, so staying read-only is on you.

**Batch 1, the material.**
- Read what the task touches, plus nearby notes, tickets, feedback and data. Prefer raw over digested: rows over the chart, logs over the ticket, code over the README.
- If there is data, compute one or two numbers from it. A measured baseline makes the target and the judge concrete.
- Check that the material can carry the climb: a weekly report needs dates, reconciliation needs IDs, a rate needs a denominator. A missing field is a finding; put it on the card. Never turn a one-off count into a rate.
- Hunt for the one fact that changes the task: a pattern across instances, a number that contradicts the framing, a belief in the notes the data doesn't back. Keep its source (file:line, command, row); a claim without a source stays off the card.

**Batch 2, access: what this session can reach right now.** In the essay's crash-free example, the model first needed crash reports, a version-to-commit map and machines on three operating systems before it could own the outcome. Access sets the ceiling, so inventory it instead of assuming it.
- **CLIs:** one `command -v` naming the 5–8 tools the best practitioner would use here (say `gh sqlite3 duckdb python3 node docker hyperfine`).
- **MCP servers:** your own tool list, deferred tools included. A project `.mcp.json` shows what is configured, not what is connected. Never call a connector's write tools.
- **Credentials:** presence by name only: `gh auth status`, and `python3 -c "import os,re;print(*sorted(k for k in os.environ if re.search('token|key|secret|dsn',k,re.I)))"`. Never open `.env`, key or credential files, and never print or use a value: secrets in a transcript leak, and this card is built to be shared.
- **Sort** into ✓ reachable, ~ one step away (the exact command or connector, and who must do it), ✗ out of reach, and `unverified` for anything you didn't check. Tie each ~ or ✗ to the rung it would raise. Never imply access you didn't confirm. If nothing is missing, say so.

## 2. Think it through before writing a line

**Stakes.** What does leaving this alone cost, and has it already cost something? A live bug may have damaged records already (oversold orders, bad reports sent), and checking that damage is part of the goal behind the goal. Say it in plain words with numbers where you have them; it is often the line that earns the go.

**Fit.** Rate altitude, depth and range as high, some or none from this task's evidence. Applying all three by reflex is how ambition turns into bloat. This rating shapes the ladder; it does not go on the card.
- Altitude fits when someone will act on the result (if there will be meetings about it, that is a good sign) or when a recurring chore could be owned by a mechanism. It fits creative work poorly, because the piece is the outcome; never replace a piece of writing with "a system".
- Depth fits when rawer material exists than what the task was handed, or when the quality ceiling sits far above "done".
- Range fits when the deliverable, written as verbs, does jobs other fields have methods for.
- All none (a rename, a typo, an incident in progress): use the no-climb card in step 3.

**Altitude.** Ask "once this is done, what is it for?" Each answer is a rung.
- Code: fix this instance → fix the class of bug → make the class impossible with a type, lint rule or test gate → own the outcome from live signals. The top rung usually needs access, such as crash reports or machines to reproduce on.
- Decks, reports, plans (after the essay's quarterly-review example): build it from every source the numbers come from → explain the period's movements and their causes, ending in actions → set up the calls the meeting exists to make, each argued both ways → retire the ritual: name the job it does, design a replacement, backtest it on past periods to show it flags problems earlier, and run both in parallel for one cycle. The old process stays until the user decides.
- Posts, essays, designs: the piece is the outcome, so climb in evidence and craft rather than scope. Every claim traced to a source is part of the floor. Above it: built from primary material (real numbers, users' own words) → tested on cold readers against a rubric written first, then revised.

**Depth.** Answer four questions in order (a paraphrase of the depth prompt the essay shares); together they become the prompt block.
1. What would the field's strongest practitioner add that the ask omits?
2. What raw material would they begin with, rather than the digest you were handed?
3. Which instruments would they actually run: a database, a statistical model, a profiler, `git bisect`, a fuzzer, a claims-to-source table? Expert vocabulary over the same method doesn't count. Models drift into exactly that, so check that the method changed, not just the words.
4. What, outside you and the user, could prove the result correct? That is the judge.

Then two moves:
- **Doubt a belief** (the `doubt` line). Name the assumption baked into the ask or the notes ("the slowdown is the database") and either the cheap read that already contradicts it or the test that could. Beliefs that steer a team are often only roughly true, and raw data is how you find out.
- **New knowledge** (analysis work): make one rung a finding the team doesn't have yet, validated on data held out from the search: fit on earlier history, score on later. Only claim it with enough held-out points (roughly 20+, or several independent units); with less, report a trend as a trend, mark causes `untested`, and drop this rung.

**Range.** Rewrite the deliverable as verbs (a trick the essay credits to Tom Kelley and Jonathan Littman's *The Art of Innovation*): a launch post has to get a skeptical reader to try the thing before they scroll on. Each verb points at fields that already do that job. Take 2–3 fields with the concrete method each brings, including one adversary whose method attacks the result: a short seller's hunt for the claim most likely false, a forensic reconciliation, chaos testing. Use fields, never characters: run the method, not the persona. The short seller's job here is finding the claim most likely to be false, and a costume adds nothing to that.

**Target.** One specific number far past the need, often 10× or more (the essay's example: a page that must load in 5 s instead of 10 s, aimed at 200 ms). For writing it can come from readers or a claims check, such as 8 of 10 cold readers naming the main use after 30 seconds. Say why it may be reachable, or label it `stretch`, and tag today's baseline `measured` or `est.`, or write `not measured yet`, so nobody mistakes a guess for a measurement. Specific hard goals beat "do your best" in Locke and Latham's goal-setting research on people (cited in the essay), and a model that decides a target is impossible quits early. The essay suggests insisting the goal is solvable; this skill asks for a reason instead, and cites a precedent only from material read this session, with its source. The floor is what makes it safe to aim high and miss.

**Judge.** No judge, no rung: a rung you can't verify is a wish, and wishes are where fabricated success starts. Take the strongest tier you can reach and name the tier on the card.
1. **Runs and returns a number:** a test in a stress loop, a fixed-input benchmark, a backtest or holdout split, a script that recomputes every figure in a deck from raw rows, a claims check for a post (a fresh subagent given only the post lists every checkable claim, a script matches each to a quoted span in the named sources, and the number is the count of unmatched claims).
2. **A real-world metric with a date:** crash rate, ticket volume, churn. Name today's value, the target and when to check.
3. **People with a rubric written now:** 3–5 target readers on a cold read. The user recruits them; you never contact anyone.
4. **A fresh subagent** given only the deliverable and that rubric, none of your reasoning. It is the weakest tier, so label it `proxy`; a proxy result never satisfies a target set for real readers, which stays `not measured` until people read it.

Never use your own rereading: self-grading is still unreliable, and an executable check gives feedback fast enough to climb against. For writing, stack tiers (a claims check plus readers). Drop rungs nothing could judge, such as "grow revenue": open-ended money goals are still beyond what models do reliably alone, and nothing could tell success from luck.

**Cost.** Build it from the steps each rung adds (runs, files, rows, subagents): minutes for the floor and the recommended rung, tokens as a multiple of the floor, plus the user's own time for setup, review or recruiting readers. Label it an estimate. "Is it worth the tokens?" is the fair objection to ambition, so answer it before anyone asks.

**Recommend** the highest rung whose judge you can run with today's access and whose cost the task can bear. Rungs that need a missing connection stay visible above it, not recommended. If no rung above the floor has a runnable judge, recommend the floor and show the access that would change that.

## 3. Print the card, then the prompt

Output one plain-English sentence, then exactly two fenced `text` blocks: the card, then the prompt. No other preamble or sign-off (the no-climb card below is the one exception; under `--go`, the work follows them). The sentence is for the person who won't decode a card: what is really going on and what the recommended rung gets them, in everyday words and with no labels from the card, e.g. "The test isn't flaky: checkout returns before stock is reserved, so sold-out items can be ordered today; rung 1 fixes that and proves it with 200 clean runs." A fenced block keeps the alignment.

**Card rules, and why:**
- At most 18 lines, each at most 70 columns. Wider lines wrap in narrow terminals and phone screenshots and the columns collapse, so cut words rather than wrap.
- Labels lowercase, padded to 9 columns. The ladder runs top-down, highest rung first and floor last, with `◀` on the recommendation, 0–3 rungs. Stop where the next rung couldn't be judged; padding the ladder is the bigger-not-deeper failure.
- Beyond plain ASCII, use only `─ ▲ │ ┷ ◀ ✓ ✗ · → ×`. Emoji render double-width and break the columns.
- Numbers, paths, counts and before→after, not adjectives. If the deliverable's format or location is a guess, say so in `asked`, e.g. `(as slides.md, inferred)`. Drop the `wider` or `deeper` line when you rated that dimension none. Card labels are fixed, but the words after them should be plain: a busy reader should understand every line without knowing this skill.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    <their ask, 10 words or fewer>
found    <the fact that changes the task: a number or file:line>
doubt    "<belief baked into the ask>" → <what raw data says | test>
stakes   <cost of leaving it; damage maybe done already; plain>

  3 ▲    <top rung: the outcome the task ultimately serves>
  2 │    <rung>                                                    ◀
  1 │    <rung>
  0 ┷    floor: <the ask, done properly, with its pass condition>

deeper   <instrument + rawest source a top practitioner would use>
wider    <field: method> · <field: method> · <adversary: attack>
target   <one hard number> (now <baseline>, measured|est.)
judge    <runnable check, its tier, written before the work>
access   ✓ <reachable> · ~ <one step, who> → rung N · ✗ <missing>
cost     floor ~<time> · rung N ~<time>, ~<k>× tokens · you ~<time>
── reply: go (rung N) · go <n> · go 0 (floor only) ─────────────────
```

The example below is for a different task. Calibrate the bar on it and don't reuse its wording. Rung 3 needs crash reports this session can't reach, so rung 2 is recommended, and the baseline is honestly unmeasured because measuring it means running tests.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    fix the crash in issue #812
found    #812 and 8 other open crashes share one frame: onResume()
doubt    "a one-off" → 9 reports from v2.3 to v2.7, all after wake
stakes   every crash loses unsaved edits; 9 reports in 5 releases

  3 ▲    crash-free by default: triage loop fed by live crash reports
  2 │    harden the whole sleep/wake path, one test per crash      ◀
  1 │    fix the shared root cause; close all 9 issues
  0 ┷    floor: #812 fixed, repro test red before, green after

deeper   symbolicate the raw dumps; git bisect onResume() from v2.2
wider    SRE: crash budget · QA: fuzz suspend timing · chaos: SIGSTOP
target   0 crashes in 1,000 scripted wake cycles (not measured yet)
judge    scripts/wake-stress.sh, tier 1, written first; must fail now
access   ✓ git gh node · ~ Sentry MCP (you add it) → rung 3
cost     floor ~15 min · rung 2 ~1 h, ~5× tokens · you ~5 min
── reply: go (rung 2) · go 1 · go 0 (floor only) ───────────────────
```

Non-code work meets the same bar. The middle of a card for monthly board forecast slides might read:

```text
found    last 6 forecasts missed by 18% on average, all high (fc.csv)
doubt    "reps sandbag" → reps over-call; misses are late-stage slips
  3 ▲    replace the roll-up meeting; shadow-run the model 2 months
  2 │    stage-weighted forecast, backtested on 36 months          ◀
  1 │    what moved since last month, why, and the 2 calls to make
  0 ┷    floor: the slides, every figure traced to a CRM export row
target   error under 5% on 24 held-out months (now 18%, measured)
judge    backtest.py fits months 1-12, rolls monthly to 36; tier 1
```

**Check every line before printing:**
- **Swap test.** Would the line still be true under a different task? Rewrite or cut it. `doubt    "the current approach is fine" → worth validating` fails; `doubt    "the DB is slow" → 88% of 41 s is CSV writes (report.py:88)` passes.
- **Deeper, not bigger.** Each rung changes the method, the source or the outcome, never just the quantity. More slides, tests or features is scope creep dressed as ambition, and it costs the user review time.
- **Banned words:** leverage, robust, comprehensive, world-class, best practices, holistic, cutting-edge, seamless, unlock. Each one stands where a method should be.
- **Nothing invented.** If the look found nothing surprising, write `found    nothing unexpected in <where you looked>`. A true dull line beats a false sharp one, because a screenshot of a made-up finding costs the user credibility.
- **Nothing private.** No secrets, tokens, emails or personal names. Assume the card gets posted.

**If the task doesn't deserve a climb,** print a short card and skip the prompt block. An honest no is worth more than a forced ladder, and during an incident speed is the whole point.

```text
── /ambitious ─────────────────────────────────────────
asked    rename userId to accountId in api/
verdict  floor: a mechanical rename has no deeper version
cost     climbing adds ~20 min nobody would notice
── reply: go 0 ────────────────────────────────────────
```

**The prompt** goes under the card in its own `text` block: 4–7 sentences that still work pasted into any model or tool with no access to this conversation. Include the real paths, numbers and finding; the recommended rung, stated as the goal; the instruments; the target; the judge to write first and prove able to fail; the floor to deliver first; and a plain instruction to report misses with numbers. Leave out rung numbers and any mention of the card. It is the four depth answers rewritten as a request, and it is the part people reuse.

Then stop and wait, unless `--go` was passed. If the user edits a rung or pushes back, reprint only the lines that changed.

## 4. Climb, only after go

- **Picking:** `go` means the recommended rung, `go N` rung N, `go 0` the floor alone. A reply that names a rung or plainly accepts the recommendation also counts. If it is ambiguous ("nice, but..."), ask which rung, because this reply is what permits edits.
- **Go covers** work inside the project: edits, scratch scripts, and tools installed into a scratch directory or venv only if the card's access line named them. Any other install, and any new dependency in the project's manifest or lockfile, needs asking first.
- **Ask first, every time, even under `--go`:** production systems, deploys, migrations, pushes or shared data; anything that costs money; sending or posting messages or contacting anyone; writing to shared tools such as tickets, CRMs or shared docs; credentials or account settings; global installs; destructive local commands (`rm -rf`, `git reset --hard`, `git clean`, history rewrites, deleting the user's files or local databases); commits the user didn't ask for. A revert can't undo these. Go approved a rung, not side effects in other people's world.

**Steps:**
1. **Write the judge first,** as a file or one rerunnable command: lasting checks where the project keeps them, throwaway harnesses in a scratch directory. If the judge needs people, draft the reader brief and rubric and ask the user to send it; never send it yourself.
2. **Prove it can fail.** Run it on the current state, or on a planted defect in a scratch copy, and record the baseline. A judge that passes unchanged work can't tell good from bad and would print fake receipts, so fix it before touching anything else.
3. **Freeze it.** Don't loosen the judge or the target to get a pass. If the judge turns out to be wrong, fix it in the open and report the change on the result card: quietly moved goalposts are the subtlest form of fabricated success.
4. **Secure the floor.** Deliver exactly what was asked, pass its check, and keep it separable: its own file or a saved copy, or a commit only if the user asked for commits. Everything above the floor only adds, so the worst case is what they asked for.
5. **Invent nothing in the deliverable either.** Every fact, number or quote comes from material read this session; mark anything else `[TK: source needed]`, and never write quotes from users you haven't seen.
6. **Climb one rung at a time,** rerunning the judge after each meaningful change. If the target looks impossible, treat that as a hypothesis and try two genuinely different approaches (another instrument, a rawer source) before concluding. Use subagents only for independent methods on large work; give each a method to run on the real material, never a persona, and count them in the spend.
7. **Stop** at the target or the chosen rung, when three attempts in a row don't move the number, when missing access blocks the next step, or when the work passes about twice the runs or steps the cost line assumed. Then report and let the user decide. Persistence earns results; unbounded persistence only burns budget.

## 5. Result card

When you stop, print the receipt in the same style, at most 14 lines:

```text
── /ambitious · result ─────────────────────────────────────────────
floor    ✓ <what was delivered> · <where it lives>
rung 1   ✓ <what changed>
rung 2   ✗ <what fell short> · <likeliest reason>
target   <actual> vs <target> (was <baseline>)                  ✓|✗
judge    <command> → <its last line of output, verbatim>
doubt    "<belief>" → held | refuted | untested · <evidence>
untested <what the judge does not cover>
moved    <judge or target change, and why> (only if one happened)
files    <files added · new deps · behaviour that changed>
cost     <runs/steps used> vs est. · time, tokens | not visible
next     <the one connection or step that would raise the ceiling>
────────────────────────────────────────────────────────────────────
```

- Every number comes from a judge run in this session, with its command. Write `not measured` where you didn't measure, and `not visible` for tokens if you can't see usage, rather than guess.
- Mark ✓ only where the judge's own output shows it, and quote that output instead of paraphrasing it; a rung the judge didn't cover is `untested`, not ✓.
- Every miss gets a line and a reason. A partial climb with an honest ✗ is a good result; an all-green card nobody can reproduce is a bad one, and this is the card most likely to be screenshotted.
