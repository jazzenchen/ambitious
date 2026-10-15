# The card /ambitious printed before doing any work (verbatim from the run)

The README is the only material: five lines, with no install link, no performance numbers and nothing quoted from beta users. So the post can't make any claim the README doesn't support. Rung 1 gets you a finished post with every claim traced back to the README, which is then tested on readers who have seen nothing else and revised.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    launch post for Tidepool v1.0 (as blog/*.md, inferred)
found    README.md is 5 lines: 0 benchmarks, 0 user quotes, no URL
doubt    "README is enough to post from" → no install, speed, dedup
stakes   ships next Tue; ~400 beta users know it, strangers don't

  2 ▲    rebuilt on beta users' words + measured Pi import times
  1 │    cold-read tested on a rubric written first, then revised  ◀
  0 ┷    floor: finished post, every claim matched to README.md

deeper   claims-to-source table; beta threads + import logs as raw
wider    copy: 30 s hook test · docs: install-first · skeptic: weakest claim
target   0 unsourced claims · 3/3 cold reads get it (not measured yet)
judge    claims_check.py vs README (tier 1) + 3 cold reads (proxy)
access   ✓ git python3 pandoc · ~ beta quotes, Pi timings (you) → 2
cost     floor ~10 min · rung 1 ~25 min, ~4× tokens · you ~10 min
── reply: go (rung 1) · go 2 · go 0 (floor only) ───────────────────
```

```text
Write the launch blog post for Tidepool v1.0, a self-hosted family photo library that runs on a Raspberry Pi or small server, deduplicates photos from everyone's phones, and recognizes faces locally so nothing leaves the house; it ships next Tuesday after 18 months of nights-and-weekends work, to ~400 beta users mostly from r/selfhosted. The only source is a 5-line README.md, so every factual claim in the post must match a quoted span in it: no invented benchmarks, quotes, features or links. Before drafting, write a claims check (a fresh model lists every checkable claim in the post with its supporting README quote; a script verifies each quote exists verbatim and counts the failures) and prove it fails on a copy with a planted false claim. Also write a cold-read rubric first: a reader given only the post must say what it is, who it is for, and why it's different (local face recognition, nothing leaves home). Deliver a finished, readable post first, then run 3 independent cold reads, revise, and rerun both checks. Report the unsourced-claim count, cold-read passes out of 3, and a list of facts to confirm (install link, date, hardware specs) with numbers for any misses.
```

Going with rung 1 (`--go`).
