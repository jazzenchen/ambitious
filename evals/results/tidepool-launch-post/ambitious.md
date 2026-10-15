The repo holds one 5-line README, so the post can only claim what those 5 lines say. The privacy promise is what readers will press hardest, and nothing in this repo can back it up. Rung 1 answers the questions self-hosters will ask before they ask them, and flags every fact you still need to supply before Tuesday.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    Tidepool v1.0 launch post (as posts/v1.md, inferred)
found    repo is one 5-line README: no changelog, benchmarks, feedback
doubt    "nothing leaves your house" → unverified: no source in repo
stakes   ships Tue; vague claims sink posts on r/selfhosted

  3 ▲    5 self-hosters cold-read it, rubric first; revise to 4/5
  2 │    rebuild from beta users' words + a Pi benchmark you run
  1 │    pre-answer r/selfhosted's 6 likely questions, or flag TK  ◀
  0 ┷    floor: the post, every claim matched to README:2-5 or [TK]

deeper   claims-to-source table; beta threads and issues, not README
wider    Show HN: install cmd up top · short seller: weakest claim
target   0 unsourced claims · 4/5 readers get it in 30 s (none yet)
judge    claims.py: unmatched claims vs sources, tier 1 · readers t3
access   ✓ git gh python3 · ~ code+feedback → 2 · ~ readers (you) → 3
cost     floor ~10 min · rung 1 ~25 min, ~3× tokens · you ~15 min
── reply: go (rung 1) · go 2 · go 0 (floor only) ───────────────────
```

```text
Write the launch blog post for Tidepool v1.0, a self-hosted family photo library that runs on a Raspberry Pi, deduplicates photos from everyone's phones and recognizes faces locally. It ships next Tuesday after 18 months of work, to about 400 beta users who mostly came from r/selfhosted. The only source available is a 5-line README, so every factual claim in the post must match a quoted span in that README or in a source the author supplies, and anything else is marked [TK: source needed]. Before drafting, write a script that takes a list of claims pulled from the post by a reader with no other context and counts the claims with no matching source span. Run it on a planted unsourced sentence to show it fails. Then list the six questions a skeptical self-hoster would ask first (which Pi model and library size, how long face indexing takes, whether anything phones home including model downloads, backup and export, license, install method), and answer each from a source or flag it as TK. Put the install command near the top, deliver the plain post first, and report the final unmatched-claim count and every open TK.
```