# How the outputs were graded

Each grader and judge was a separate Claude subagent (claude-opus-5-5) with file access to the fixture and to the response or responses it was judging. The prompts below are verbatim except for the `{placeholders}`. Results: `../results/*/…grading.json` and `../results/blind-judgments.json`.

## 1. Assertion grader (one per output)

Structured output: `expectations[{text, passed, evidence}]`, `factual_errors[]`, `invented_content[]`, `notes`.

```text
You are a strict, evidence-based grader. Grade ONE response from an AI coding assistant.

The user asked (in a small project at {fixture_dir}): "{task}"
The response to grade is at: {response.md}
(Its tool-call log is at {transcript.md} — use it only to see what it actually looked at.)

First read every file in the fixture directory {fixture_dir} (it is small) so you can fact-check. Recompute any number the response cites from the raw files (write a quick python3 script for CSV math if needed).

Then evaluate each expectation below. PASS only with concrete evidence quoted from the response; if it is ambiguous or only gestured at, FAIL. Do not reward length. Judge the response as written.
{the 9 expectations from ../evals.json}

Also list factual_errors (claims contradicting the fixture, wrong numbers) and invented_content (unsupported facts, quotes, metrics). Return expectations in the same order with the exact text.
```

The 9 expectations are in `../evals.json`:
- Seven come from the essay's ideas: grounded, outside judge, hard target, tests an assumption, deeper not bigger, access audit, and the task-specific insight.
- Two test this skill's own design: floor kept, and stops before working. The essay asks for neither, which counts against the baseline on those two.

## 2. Blind pairwise judges (3 per task)

Structured output: `winner (A|B|tie)`, `confidence`, strengths and weaknesses per side, `reasoning`.

Order **alternated rather than randomized**: the /ambitious output was Response A for lenses 1 and 3 and Response B for lens 2. That puts it first in 8 of the 12 comparisons. Judges weren't told which response came from the skill.

```text
{lens}

Context: a user in the small project at {fixture_dir} asked an AI assistant: "{task}" — and asked it to aim higher than the literal request. Read the project files first (they are small) so you can tell real insight from plausible filler.

Two anonymous responses:
- Response A: {path}
- Response B: {path}

Read both fully. Do not read any other files in the iteration directories, and ignore surface formatting (a box/card vs prose) except insofar as it helps or hurts usefulness. Pick a winner (or tie) and explain.
```

Lenses:
1. You are the person who asked. You are busy and will act on one of these today. Which response would lead to a better real outcome for you, with the least wasted effort?
2. You are a senior practitioner in this field (engineering, analytics or writing as appropriate). Which response shows deeper, more correct understanding of the actual problem in these files, and a better method?
3. You are a skeptic. Penalize scope creep (bigger, not deeper), unverifiable or invented claims, generic advice, and plans with no way to check success. Which response is more trustworthy and verifiable?

## Reproducing

- `../run_evals.sh <out-dir>` regenerates the proposal runs, both with the skill and with the baseline.
- To grade them, give the prompts above to any capable model with file access.
- `../verify_go_run.sh` re-checks the end-to-end demo without a model.
