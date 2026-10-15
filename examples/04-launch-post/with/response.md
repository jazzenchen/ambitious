The post is at `blog/tidepool-v1.0.md`. A separate check, run by a fresh model that saw only the post and the README, found **0 of 15** claims without a source in the README. Three readers who saw only the post all came away knowing what it is, who it's for and why it's different, but those reads were done one revision before the final text.

```text
── /ambitious · result ─────────────────────────────────────────────
floor    ✓ finished launch post · blog/tidepool-v1.0.md (uncommitted)
rung 1   ✓ cold-read tested, revised 4× against the claims check
target   0 unsourced claims, 3/3 cold reads (was 10 of 21)         ✓
judge    claims_check.py claims_v5.json README.md
         → unmatched 0 of 15 claims
judge    coldread_score.py answers_v2.json → cold reads passed 3 of 3
doubt    "README is enough to post from" → held, barely · 3/3 readers
         stopped at: no install link, no screenshots, no Pi specs
untested final text not cold-read (v3–v5 only removed claims);
         readers were model proxies, not real r/selfhosted users
files    + blog/tidepool-v1.0.md · judge files in scratchpad only
cost     9 subagent runs vs ~5 est. · ~25 min · tokens not visible
next     send install link + beta feedback → rung 2 (users' words)
────────────────────────────────────────────────────────────────────
```

**What the checks showed:**
- **My first draft failed the claims check.** 10 of its 21 claims weren't in the README, including "find every picture of your kid in 30 seconds" and things the beta testers supposedly did. I cut all of them instead of changing the check to let them pass.
- **The check can fail.** On a copy where I added a fake benchmark ("10,000 photos in under 4 minutes"), it flagged that claim.
- **One flag was the checker being inconsistent, not the post.** In the fourth run it flagged "face recognition runs on your own machine", a line earlier runs had accepted. I changed the post to use the README's own wording rather than loosen the check.
- **The cost:** the dedup line is now one bare sentence, because each example I tried claimed more than the README says.

**To confirm before Tuesday.** I left these out of the post rather than guess them:
- **An install or download link and a repo URL.** All three readers stopped here. Add it to "Try it".
- **The launch date.** The post says "v1.0 ships" with no date.
- **Hardware requirements** beyond "a Raspberry Pi", and how photos get from phones to Tidepool. The skeptical reader asked about both, and also about Immich, backups and the license.
- **A beta-user quote or a measured import time.** Either would give the post the proof it currently lacks. That's rung 2.

The judge scripts, rubric and reader answers are in `<scratchpad>/judge/`. Nothing has been committed.