I wrote the launch post at `blog/tidepool-v1.0-launch.md`. Every factual claim in it now traces back to your README, but it isn't publishable until you fill 11 `[TK]` placeholders that only you can answer.

```text
── /ambitious · result ─────────────────────────────────────────────
floor    ✓ post, 0 unsourced claims · blog/tidepool-v1.0-launch.md
rung 1   ✓ 2 cold reads drove 3 revisions; scores 1→1→2→0 unmatched
target   real readers: not measured (proxy cold read 4/5 → 5/5)     ✗
judge    claims_check.py → unmatched: 0 of 10 claims (TK-flagged: 3)
doubt    "nothing leaves your house" → untested · now a TK'd goal
untested final draft never cold-read; dedup/Pi-speed claims only TK'd
files    + blog/tidepool-v1.0-launch.md · no deps · judge in scratch
cost     4 claim extractions + 2 cold reads vs ~3 est. · ~$1.20
next     fill the 11 TKs, then send rubric.md to 5 r/selfhosted users
────────────────────────────────────────────────────────────────────
```

**How it was checked:** a separate reader that saw only the post and the README listed every factual claim and the README line backing it. A script then confirmed each backing line really is in the README. Before using it, I tested the check on a fake "10,000 photos in 4 minutes" claim, and it caught it.

**What the revisions changed:**
- **"Nothing leaves your house"** is now stated as a design goal. A placeholder asks you to list every outbound connection (update checks, map tiles, model downloads) before you publish. The first cold reader picked this as the claim a commenter would test with a packet capture and attack.
- **Backups and export:** the first cold reader said the post never explains how to back up the library or get your photos out. I added a section for that. You have to write its content, because nothing in the project describes it.
- **Pi speed and dedup:** the second cold reader's most likely attack was how long the first face scan takes on a Pi. The other was whether dedup catches resized copies, like a photo forwarded through a chat app. Both are now placeholders asking for real measurements and details.
- **Opener:** I cut "Every family has the same mess" and the "four copies become one" image because the README backs neither. The opener is now a question. That cost the line both cold readers liked best.

**What fell short:**
- **No real readers yet:** your target was 4 of 5 people naming what Tidepool is for and why it's private within 30 seconds. That needs people, so I haven't measured it. The 5/5 score came from a model reading the post, which is weaker evidence.
- **Final draft not re-read:** the cold-read scores are for drafts 1 and 2. The final draft only changed the opener and added placeholders, and I didn't get a new cold read on it.
- **Release date:** the README says v1.0 ships "next Tuesday" without a date, so I left the date as a placeholder.

To finish it, fill the placeholders (the code audit for outbound connections matters most), then send the 5-question reader rubric to a few r/selfhosted users. The rubric and the check script are throwaway files, so they're in the scratchpad (`<scratchpad>/judge/`):
- `rubric.md` is the reader rubric.
- `claims_check.py` is the check script.

Nothing was committed.