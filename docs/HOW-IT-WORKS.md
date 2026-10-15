# How /ambitious works

A plain-language guide for people who just installed `/ambitious` or are deciding whether to. It describes v3.2, the version you install. The skill's behaviour is defined in [`skills/ambitious/SKILL.md`](../skills/ambitious/SKILL.md); if this guide and that file ever disagree, the file wins.

`/ambitious` is unofficial. It was inspired by Felix Rieseberg's essay [How to be more ambitious: A tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/), and it is not affiliated with or endorsed by him or by Anthropic.

## 1. What /ambitious does

`/ambitious` is a Claude Code skill you type in front of one task (a bug fix, a deck, a launch post) to see a bigger version of that task before any work starts. First it makes about ten read-only calls to look at your real files and data, and at what this session can reach: command-line tools, MCP servers (connectors to outside services), and credentials, checked by name only. Then it prints one plain-English sentence and a screenshot-sized **card**. The card shows a ladder of **rungs** (bigger versions of your task), a finding from your own material, a hard target, and a **judge**: an outside check, not the model's own opinion, that decides whether the work succeeded. Your original ask is rung 0, the **floor**. Nothing changes until you reply `go` (or start it with `--go`, described below). After that, the floor is always delivered first, finished to at least the standard Claude would reach without the skill, and the work ends with a **receipt** whose numbers all come from the judge.

## 2. How to use it

Install:

```bash
npx skills add jazzenchen/ambitious
```

Other routes are in the [README](../README.md#install): copying the single file, installing it as a Claude Code plugin (the command then becomes `/ambitious:ambitious`), or uploading a zip to claude.ai or Claude desktop.

There are four ways to call it:

- **`/ambitious <task>`**: the normal way. It looks read-only at what the task touches (code, notes, tickets, feedback, data), computes a number or two from any data it finds, and takes stock of the tools and connections this session has. Then it prints the plain-English sentence, the card and a reusable prompt, and **stops and waits**. If you edit a rung or push back, it reprints only the lines that changed.
- **`/ambitious`** with no task: it infers the task from, in order, your latest unfinished request in the conversation, your uncommitted changes, then your last commit, and marks `asked` with `(inferred)`. If none of those exist, it prints a card whose only line is `asked    nothing to infer · reply with the task` and stops.
- **Replying `go`, `go N` or `go 0`** after a card: `go` takes the recommended rung, `go 2` takes rung 2, and `go 0` delivers just what you asked for. A reply that names a rung or plainly accepts the recommendation also counts. If your reply is ambiguous ("nice, but..."), it asks which rung, because this reply is what permits edits.
- **`/ambitious --go <task>`** (or `--go N`): prints the card and prompt, then starts work at once on the recommended rung, or with `N` on the highest rung at or below N whose judge it can run now. It says in one line which rung it took. `--go` needs task text: if the task had to be inferred, `--go` is ignored and it waits for you.

It doesn't ask clarifying questions before the card, because the card is the question. Any guess it made shows up in `asked` or `doubt`, and correcting it costs you one word.

**What it will never do without asking.** Before `go`, it changes nothing: no edits, installs, builds or test runs, and no network calls beyond reading material the task names. After `go`, it can edit files in your project, write scratch scripts, and install tools into a scratch directory (a throwaway folder kept apart from your work) or a virtual environment (an isolated install area) only if the card's `access` line named them. These always need a separate yes, every time, even under `--go`:

- production systems, deploys, migrations, pushes, or shared data
- anything that costs money
- sending or posting messages, or contacting anyone
- writing to shared tools such as tickets, CRMs or shared docs
- credentials or account settings
- global installs, any install beyond the scratch tools the card named, and any new dependency in your project's manifest or lockfile (the files that list what your project depends on, such as `package.json` and its lockfile)
- destructive local commands (`rm -rf`, `git reset --hard`, `git clean`, history rewrites, deleting your files or local databases)
- commits you didn't ask for

A revert can't undo any of these. Saying go approves a rung of work, not side effects in other people's world.

## 3. Anatomy of a card

This is the real card from the run in [`evals/results/go-run/`](../evals/results/go-run/), for the task "fix the flaky checkout test", pasted unchanged. That run used an earlier version of the skill (v3), before the v3.2 changes described in section 4:

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

A card is at most 18 lines of at most 70 columns, so it survives a phone screenshot without wrapping. Above it sits that one plain-English sentence, for anyone who won't decode a card (in this run: checkout isn't waiting for stock to be reserved, the same bug lets people order sold-out items, and rung 1 fixes both). Below it sits **the prompt**: 4–7 sentences with the real paths, numbers, goal, judge and floor, written so you can paste it into any model or tool that hasn't seen this conversation. Line by line:

- **`asked`**: your request in ten words or fewer. If the task was inferred, or the deliverable's format or location is a guess, it says so here, e.g. `(inferred)`.
- **`found`**: the one fact from your own material that changes the task, backed by a source (a file and line, a command, a data row). Here it found that checkout reserves stock inside `forEach(async ...)`. JavaScript's `forEach` starts each async step but never waits for it to finish, so checkout returns before any stock is reserved. A claim without a source stays off the card. If nothing surprising turned up, the line says `nothing unexpected in <where it looked>`.
- **`doubt`**: a belief baked into the ask, followed by what the raw material says or the test that would settle it. Here the belief is "flaky test", meaning one that fails at random. The code says otherwise: the test waits 25 ms, while the fake inventory service takes a random 0 to 40 ms. Any delay above 25 ms (15 of those 40 ms) loses the race, so about 38% of runs should fail. The random delay only decides which runs expose the problem; the cause is a real bug in checkout, with a predictable failure rate.
- **`stakes`**: what leaving it alone costs, in plain words, including damage that may already be done. Here a sold-out item still gets an order ID, and the out-of-stock error never reaches the code that called checkout (it ends up as an unhandled rejection, an error nothing catches). That turns "an annoying test" into "customers can buy stock you don't have".
- **The rungs (`2 │`, `1 │`, `0 ┷`)**: each numbered line is a bigger version of the task, highest on top. A ladder has 0 to 3 rungs above the floor and stops where the next rung couldn't be checked. `▲` caps a ladder that reaches rung 3; this one stops at 2. Each rung must change the method, the source or the outcome, not just do more of the same. For code the climb usually runs: fix this instance, then the whole class of bug, then make that class impossible, then own the outcome from live signals. Here rung 1 makes checkout all-or-nothing (reject out-of-stock orders and give back stock already held), and rung 2 makes this kind of bug impossible with a lint rule (an automatic code check) that fails CI (the checks that run on every change) on any promise nobody waits for. A promise is JavaScript's handle on work that finishes later.
- **`◀`**: marks the recommended rung, which is the highest one whose judge can run with today's access and whose cost the task can bear. Rung 2 isn't recommended because its lint tool (eslint) would be a new project dependency, which needs your OK. Rungs that need missing access stay visible, so you can see what they would take. If no rung above the floor can be judged, the floor itself is recommended.
- **The floor (rung 0, `┷`)**: your original ask, done properly, with its pass condition. Here that's: await every reservation, remove the 25 ms sleep, and pass 200 runs. It's always delivered first and kept separate, so the worst outcome of any climb is exactly what you asked for. "Done properly" includes finished: at least as polished as plain Claude would make it (see step 4 below).
- **`deeper`**: the instrument and the rawest source a top practitioner would use. Here, fixed latencies of 0 ms and 39 ms make the tests deterministic (same result every run), so they no longer depend on winning a race against a sleep. The method itself has to change; fancier words for the same method don't count.
- **`wider`**: two or three methods borrowed from other fields (`field: method`), including one adversary whose method attacks the result. Here: QA's stress loop (run the test suite many times in a row and count failures), the database idea of an all-or-nothing reservation, and a chaos-testing attack (deliberately injecting trouble, here 40 ms of delay) as the adversary. These are methods it actually runs, not characters it plays. The line is dropped when borrowing doesn't fit.
- **`target`**: one hard number, often far past the need, with today's baseline tagged `measured`, `est.` or `not measured yet`. Here the target is 0 failures in 500 runs, while the floor only promises 200. The baseline is an estimate from reading the code, because measuring it would mean running tests, which the look phase never does. A target that may be out of reach is labelled `stretch`; the floor is what makes aiming high safe.
- **`judge`**: the check that decides success, written before the work and never the model rereading its own output. Here it's a scratch stress script plus a test pinned at 39 ms of latency. "must fail now" means it has to fail on today's code, which proves it can tell broken from fixed. The tier says how strong it is: **1** runs and returns a number (a test loop, a benchmark, a backtest, a script that recomputes every figure, a claims check); **2** is a real-world metric with a date to check it (crash rate, ticket volume); **3** is people reading cold against a rubric written now, whom you recruit because it never contacts anyone; **4**, the weakest, is a fresh subagent (a separate model instance with none of this conversation) that sees only the deliverable and the rubric, labelled `proxy`. No judge, no rung: anything nothing could check gets dropped.
- **`access`**: what this session can reach right now. `✓` means reachable (here Node 24, git and the GitHub CLI). `~` means one step away: it names the step, who must take it, and which rung it would raise (here an eslint dev dependency that needs your OK, for rung 2). `✗` means out of reach (here order data, so it can't count orders the bug already let through). Anything it didn't check is marked `unverified` instead of assumed.
- **`cost`**: an estimate built from the steps each rung adds. Here that's minutes for the floor (~5) and the recommended rung (~15), tokens (the units of text the model reads and writes, which drive the bill) as a multiple of the floor's (~2×), and your own time for setup or review (~3 min).
- **The reply line**: what you can type back. `go` takes rung 1 here, `go 2` takes the higher rung, and `go 0` takes the floor only.

Before printing, every line is checked: it must not stay true if you swapped in a different task, the rungs must go deeper rather than just bigger, filler words (leverage, robust, comprehensive and similar) are banned, nothing is invented, and nothing private (secrets, tokens, emails, personal names) appears, because the card is built to be shared.

## 4. What happens after "go"

1. **Write the judge first,** as a file or one rerunnable command. Lasting checks go where the project keeps its tests, and throwaway harnesses go in a scratch directory. If the judge needs people, it drafts the reader brief and rubric and asks you to send them.
2. **Prove the judge can fail.** It runs the judge on the current state (or on a deliberately planted defect in a scratch copy) and records the baseline. A judge that passes unchanged work can't tell good from bad, and it would print a fake receipt.
3. **Freeze it.** The judge and the target are not loosened to get a pass. If the judge turns out to be wrong, it's fixed in the open and reported on the result card's `moved` line.
4. **Secure the floor, finished.** It delivers exactly what you asked, at least as polished as Claude would make it without the skill: in the format you expect, built with the best tools the session has (a slides, document or spreadsheet skill if one is available, real charts where the data shows a trend, clean prose). Deeper work goes on top of a finished floor, never instead of one, because a result that looks worse won't get used, however correct it is. The floor passes its check and is kept separate: its own file or a saved copy, or a commit only if you asked for commits.
5. **Invent nothing, and leave no holes.** Every fact, number or quote in the deliverable comes from material read this session, and it never writes quotes from users it hasn't seen. Where a fact is missing, it writes around it, saying less or saying something more general that is still true, so the piece still reads as finished. The missing facts go in a short **"to confirm" note** beside the deliverable and in its reply. There are no `[TK]` markers (editors' shorthand for "to come"), `TODO`s or bracketed blanks inside the deliverable itself. Judge scripts, saved floor copies and other scaffolding stay out of it too, in a scratch directory or a clearly separate file.
6. **Look at it before calling it done.** If the deliverable is visual (slides, a web page, a document), it renders it the way you'll see it, for example as a PDF or as images, and looks at every page. Anything that looks unfinished, crowded or broken gets fixed.
7. **Climb one rung at a time,** rerunning the judge after each meaningful change. If the target starts to look impossible, it tries two genuinely different approaches before concluding that it is.
8. **Stop** at the target or the chosen rung, after three attempts in a row that don't move the number, when missing access blocks the next step, or at about twice the runs or steps the cost line assumed. Then it reports, and the next decision is yours.

**What changed in v3.2.** Steps 4 and 5 were tightened and step 6 is new. The previous version, v3.1, put checking ahead of polish. In the with/without test below, its deck used tables only and left `[TK]` placeholders for owners and dates on the slides, and its launch post showed 11 `[TK]` gaps to readers. The author looked at the v3.1 deck and said it looked worse than plain Claude's. The blind judges had preferred plain Claude too: 3–0 on the deck and 2–1 on the post. v3.2 keeps the checking and makes a finished result part of the floor.

One v3.2 run from that test shows steps 5 and 6 at work. The deck run left a [`TO_CONFIRM.md`](../examples/03-qbr-deck/with/files/qbr/TO_CONFIRM.md) next to the slides, listing what the data couldn't support (customer totals, so there's no true churn rate; reasons customers left; what more support would cost) instead of putting blanks on the slides. And step 6 is not foolproof: in that same run, the last round of wording edits never got rendered after three ways of rendering failed. Its final reply said so and asked for someone to open the deck and skim the titles on slides 1 and 6 to 8 before the meeting.

**Reading the result card.** Here's the receipt from the same flaky-checkout run as the card in section 3, pasted unchanged:

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

- **`floor`**: what was delivered and where it lives. A floor-only copy was saved separately, so you could keep just that.
- **`rung 1`**: one line per rung attempted. `✓` means the judge's own output shows it passed. A rung that fell short gets `✗` and the likeliest reason. Rung 2 has no line because rung 1 was the one chosen.
- **`target`**: the actual result vs the target, with the baseline in parentheses, and `✓` or `✗` at the end. The card had estimated about 38% failing from the code; the measured baseline was 32 of 100.
- **`judge`**: the command and the last line of its output, copied word for word rather than paraphrased. The second line is the "prove it can fail" step: the new tests run against the old code failed 4 of 4.
- **`doubt`**: the card's belief, now marked `held`, `refuted` or `untested`, with the evidence. "Flaky test" was refuted.
- **`untested`**: what the judge doesn't cover (here a `release()` call that itself fails, and orders placed before the fix). Untested is not the same as passed.
- **`moved`** (absent here): appears only when the judge or the target was changed, along with the reason.
- **`files`**: files added or changed, any new dependencies (none here), and behaviour that changed.
- **`cost`**: what was actually used vs the estimate. Tokens show as `not visible` because the session couldn't see its usage, and the skill says so instead of guessing.
- **`next`**: the one connection or step that would raise the ceiling. Here that's access to order data, to count orders placed without stock held.

Every number on this card comes from a judge run in this session, and every miss gets its own line and a reason. A partial climb with an honest `✗` counts as a good result. Under the receipt, this run also listed in plain words the behaviour change callers must handle (out-of-stock orders now fail), the past damage it couldn't check, where its scratch files are, and that nothing was committed. In v3.2, that part of the reply also carries the "to confirm" list from step 5 whenever facts were missing. [`evals/verify_go_run.sh`](../evals/verify_go_run.sh) rechecks the fix without a model. In its recorded run ([`recheck.log`](../evals/results/go-run/recheck.log)), the original suite failed 111 of 300 runs (37%, close to the card's 38% estimate), the fixed one failed 0 of 300, and the new tests failed 4 of 4 against the original checkout code.

## 5. When to use it, and when not to

The author ran four tasks twice on small sample projects, with the same model (`claude-opus-5-5`): once typed normally ("plain Claude") and once as `/ambitious --go <task>`, so the skill picked its own recommended rung with no person choosing. Then two kinds of check looked at the finished work ([full report](../evals/outcomes/OUTCOMES.md); every prompt, card and output is in [`examples/`](../examples/)):

- **Hidden checks** that neither run saw: for the flaky test, 200 suite runs, 3 hidden behaviour tests and 300 trials of a cart that fails partway; for the others, one identical method applied to both results (500 deliberately hostile CSV rows re-parsed, every deck number recomputed from the source CSV and every slide rendered the way PowerPoint shows it, every claim in the post checked against the product README).
- **Blind judges**: three model judges per task (a busy requester, a senior practitioner and a skeptic) compared the two finished projects labelled only A and B, with the skill's files removed.

| Task | Plain Claude | `/ambitious` v3.2 | Blind judges | Cost · time (plain → v3.2) |
|---|---|---|---|---|
| Fix a flaky test | Flake fixed (0 of 200 suite runs failed), but a cart that fails partway keeps the stock it reserved in 300 of 300 trials; 2 of 3 hidden tests pass | Flake fixed (0 of 200), 0 of 300 trials leaked, 3 of 3 hidden tests pass; its new test caught the leak in plain Claude's version in 17 of 20 runs | v3.2, 2–1 | $0.18 · 0.7 min → $0.52 · 20.2 min |
| CSV export button | Correct: 0 bad cells and 0 live formulas (cells a spreadsheet would run as code) out of 2,000; CSV code mixed into the dashboard file | Equally correct (0 and 0), with the CSV code in its own module so it can be tested; no tests added (the project has no test runner) | v3.2, 3–0 | $0.21 · 0.6 min → $0.64 · 2.5 min |
| QBR deck section (quarterly business review) | 8 slides, 4 charts, 0 wrong numbers, but 2 slides render broken in PowerPoint (tables with 4- and 8-inch cell margins), so 27 on-slide numbers can't be read; some causal overreach (claiming a cause the data can't show) | 8 slides, 5 charts, all 104 numbers correct, 0 broken slides, no placeholders; calls the support and churn link a pattern, not proof; adds a script that rechecks every figure | v3.2, 3–0 | $1.10 · 10.3 min → $2.32 · 24.8 min |
| Launch blog post | Livelier and longer (454 visible words), but 14 to 20 invented claims, depending on how a checker splits them; 3 placeholders a reader would see (an install block that reads only "# install instructions here" and two links to "TODO-link") | 0 invented claims, 0 placeholders, 201 visible words; thin, and its "Try it" section has no link because the source gave none | plain, 2–1 | $0.17 · 0.7 min → $1.45 · 6.0 min |
| **All four** | | | **v3.2 in 9 of 12** | **$0.42 · 3.1 min → $1.23 · 13.4 min** (averages) |

You can see the difference on the deck yourself: [plain Claude's slides](../examples/03-qbr-deck/without/rendered-slides.png), [v3.2's slides](../examples/03-qbr-deck/with/rendered-slides.png) and, for comparison, [v3.1's slides](../examples/03-qbr-deck/with-v3.1/rendered-slides.png), each as PowerPoint renders them. For the post, a [side-by-side image](../examples/04-launch-post/side-by-side.png) highlights every factual claim in both posts, green if the README states it and red if it doesn't, as one checker labelled them (that checker counted 17 invented claims in plain Claude's post and 0 in v3.2's).

- **More correct where the results differed.** On the flaky test, v3.2 fixed a stock leak that plain Claude noticed but left as "Something to decide later", and that plain Claude's own tests couldn't see: they passed 20 of 20 runs against both versions. On the post, refusing to invent kept made-up claims out (three independent checks counted plain Claude's at 20, 14 plus 5 softer stretches, and 17). On the CSV button and the deck, both versions got every number right.
- **No longer the less polished one on the deck.** v3.1 lost the deck 0–3; v3.2 won it 3–0. Plain Claude's reply said "I haven't seen it rendered yet." Two of its slides came out broken, while v3.2's rendered cleanly with more charts. On the CSV button, all three judges preferred v3.2, mainly for its structure.
- **Plain Claude still won the post.** Two of three judges preferred its livelier, longer draft, invented claims and placeholders included, because v3.2's accurate post was thin. The skeptic judge picked v3.2 because nothing in it needed re-checking. On the flaky test, the skeptic preferred plain Claude's smaller fix: v3.2 added a stock-release function nobody asked for, and its new test caught the leak in most runs, not all.
- **About 3× the cost and 4× the time.** Finished work averaged $1.23 and 13.4 minutes instead of $0.42 and 3.1 minutes. The spread is wide: the flaky test took 20 minutes instead of under one. v3.2 also costs more than v3.1 did ($1.06 and 6.8 minutes on the same tasks). Printing the card alone, with no work after it, averaged about $0.29 across four runs in a [separate benchmark](../evals/results/BENCHMARK.md) of an earlier version (v3).
- **Caveats.** These are one run per arm on four tasks, tested and judged by models rather than people, on sample projects the author wrote. v3.2's changes were made after seeing v3.1's results on these same four tasks (it lost the deck and the post), so they are no longer an unseen test. The plain-Claude runs are the same ones v3.1 was compared against; only the skill side was re-run. Part of the deck swing comes from the judges: this time they were shown every slide as PowerPoint renders it, while the v3.1 judges were not and didn't notice plain Claude's two broken slides, so the same plain-Claude deck went from winning 3–0 to losing 3–0. Plain Claude's first attempts at the deck and the post published to claude.ai instead of the project, so those tasks were re-run with those tools turned off, and only the re-runs count. Used normally, you'd see the card and could pick a different rung. Treat all this as a sanity check.

**Use it when** being wrong is expensive (a bug that may already be damaging records, numbers a meeting will act on, claims going out under your name), when there's raw material to dig into (data, logs, code, feedback), when you want proof from something other than the model's own say-so, and when you can spare the extra time and cost.

**Skip it when** you need something in a minute or two, when you want a lively first draft and will check its facts yourself, when the change is mechanical, or when an incident is in progress and speed is the whole point.

**The no-climb case.** When a task has no deeper version, the skill says so with a short card instead of forcing a ladder, and it skips the prompt. This example comes from the skill's instructions:

```text
── /ambitious ─────────────────────────────────────────
asked    rename userId to accountId in api/
verdict  floor: a mechanical rename has no deeper version
cost     climbing adds ~20 min nobody would notice
── reply: go 0 ────────────────────────────────────────
```

`verdict` replaces the ladder, and the only reply offered is `go 0`. An honest no is worth more than a padded ladder.

## 6. FAQ

**Does it change my files before I say go?** No. The look phase only reads: files, `git status/log/diff`, `ls`, `command -v`, `gh auth status`, and one-liners that read local data without writing anything. A few of these commands are pre-approved to spare you permission prompts. That pre-approval isn't a sandbox; staying read-only is a rule the skill gives the model.

**Can I pick a different rung?** Yes. Reply `go N` for rung N or `go 0` for the floor alone, or edit a rung and it reprints just the changed lines. If the rung you pick needs access the session lacks, the climb stops at that point and reports what's missing.

**What does it check about credentials?** Only whether they exist, by name: `gh auth status`, plus a one-liner that lists the names (never the values) of environment variables containing "token", "key", "secret" or "dsn" (a database or service connection string). It never opens `.env`, key or credential files, and never prints or uses a secret. For connectors, it reads its own tool list and never calls a connector's write tools.

**Why does it cost more?** It runs a longer set of instructions, writes a judge before the work, proves the judge can fail, and reruns it after each change. It also finishes the floor to full polish and, for visual work, renders it and looks at every page. In the four-task test that came to about 3× the cost and 4× the time of plain Claude. The `cost` line estimates this up front, and the climb stops at about twice the steps that line assumed.

**Does it work outside code?** Yes. For decks and reports, the rungs climb from building on every source behind the numbers, to explaining what moved and why, to setting up the decisions the meeting exists to make, and at the top to designing a replacement for the recurring report itself, tested on past periods (the old process stays until you decide). The floor there is finished slides with real charts where the data has a trend and every figure checked, rendered and looked at page by page. For posts and essays the piece is the outcome, so it climbs in evidence and craft rather than scope. The floor is a finished, readable piece with every claim traced to a source, and its judges are a claims check against named sources, cold readers you recruit, or, as a weaker stand-in labelled `proxy`, fresh model readers.

**Will it leave `[TK]` or `TODO` markers in my document?** Not since v3.2. Where a fact is missing, it writes around it so the deliverable still reads as finished, and lists what's missing in a separate "to confirm" note and in its reply. In the launch-post test, the list in its reply asked for an install or download link, the launch date and hardware requirements beyond "a Raspberry Pi", and the post simply left those details out. Version 3.1 did leave `[TK]` markers, and four of the five blind votes for plain Claude's deck and post counted those placeholders against v3.1.

**What if the target is impossible?** The card gives a reason the target may be reachable, or labels it `stretch`. After go, it treats "impossible" as a hypothesis and tries two genuinely different approaches before concluding. If the number still won't move, the receipt shows `✗` with a reason, and you still have the floor. The target is never quietly lowered; any change shows up on the `moved` line.

**Will it kick in on its own?** Only when you type `/ambitious` or explicitly ask Claude to think bigger, aim higher or 10× a task. It isn't meant for ordinary requests just because they're large, hard or important.

**Is it official?** No. It's an unofficial skill, not affiliated with or endorsed by Felix Rieseberg or Anthropic. Its ideas are paraphrased from the essay linked at the top; the card, the rungs and floor, the access audit, the cost line, the stop rules and the receipt are this project's own.
