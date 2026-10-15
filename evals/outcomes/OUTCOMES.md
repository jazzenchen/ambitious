# With vs. without /ambitious: finished work, measured

**Question:** if you type `/ambitious` before a task, is the result better than when you just type the task?

**Setup.**
- 4 tasks on small fixture repos. Each runs twice, on fresh git copies, with the same model (`claude-opus-5-5`) and full edit permission:
  - **without:** `claude -p "<task>"`, what you'd normally type
  - **with:** `claude -p "/ambitious --go <task>"`, where the skill prints its card, picks its recommended rung and does the work with no human in the loop
- No MCP servers and no claude.ai artifact tools, so every deliverable lands in the repo.
- Harness: [`run_outcomes.sh`](run_outcomes.sh).

**Measurement.**
- Hidden checks that neither run saw:
  - [`checks/flaky_check.sh`](checks/flaky_check.sh) runs 200 suite runs plus 3 hidden behaviour tests.
  - For the other tasks, an independent tester applies one identical method to both results: 500 fuzzed CSV rows re-parsed with Python, every deck number recomputed from the CSV, every claim in the post checked against the README.
- Then 3 blind judges per task compare the two finished repos: a busy requester, a senior practitioner and a skeptic. Results are labelled A/B, the skill files are removed, and the label order is counterbalanced, so the skill is "A" in 2 of the 4 tasks.

## Results

| Task | Without the skill | With `/ambitious` | Blind judges |
|---|---|---|---|
| **Fix the flaky checkout test** | Flake fixed (0/200 suite runs fail). But a failed cart **leaks the stock it held: 300 of 300 trials**, 300 units lost. Hidden test H3 fails. | Flake fixed (0/200). **0 of 300** leaked. Hidden tests 3/3. It added a regression test that catches the leak in the other version (29/30 runs). | with 2 · without 1 |
| **Add a CSV export button** | Correct and injection-safe: 0 bad cells and 0 live formulas out of 2,000. No tests. | Same output quality (0 / 0), plus the logic in a pure module and 3 tests. | with 2 · without 1 |
| **QBR customer section** | 8-slide `.pptx` with charts. 0 wrong numbers out of 91, and the "flat net adds" insight. Some causal overreach, and two loose statements. No check script. | 10-slide deck. 0 wrong numbers out of 84, no causal overreach, and a script that re-checks every figure. But it uses tables only (no charts) and leaves `[TK: owner/date]` placeholders. | **without 3** · with 0 |
| **Tidepool launch post** | Polished, 460 words. **20 of 29 factual claims invented**: pricing, features, a beta story, stability promises, an author byline. | 1 of 10 claims unsupported (implied by a heading). Honest, but sparse: 11 visible `[TK]` placeholders where facts were missing. | without 2 · with 1 |
| **Total** | | | **without 7 · with 5** |

**Cost and time** (4 tasks): without, $0.42 and 3.1 min on average; with, $1.06 and 6.8 min. The skill costs about 2.5× as much.

## What this means

- **Where correctness can be measured, `/ambitious` came out ahead:**
  - On the code task, plain Claude shipped a subtle stock leak that its own tests couldn't see. The skill's judge-first approach caught it.
  - On the post, plain Claude made up 20 facts. The skill refused to invent and marked the gaps.
- **Where polish matters, plain Claude won the blind vote:** a finished-looking deck with charts, and a ready-to-publish post. The judges preferred something you can ship today, even with flaws in it.
- **It costs more and takes longer.** Use it when being wrong is expensive. Skip it for a quick draft.

## Caveats

- One run per arm per task (n=4). Model testers and judges, not people. I wrote the fixtures.
- The first no-skill attempts at the QBR and post tasks published to claude.ai instead of the repo. Both arms of those two tasks were then re-run with those tools disabled, and only the re-runs are scored. The flaky and CSV runs never used those tools.
- `--go` takes the recommended rung with no human in the loop. Interactively, you'd see the card and could pick another rung.

## Files

- `results/<task>/<with_skill|without_skill>/`: prompt, final response, diff, timing
- `results/measurements-and-judgments.json`: every measurement, plus the blind verdicts, de-blinded
- `results/flaky-hidden-checks.log`: the hidden flaky-test checks
