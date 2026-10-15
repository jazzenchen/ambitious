The section is built. In Q3, total revenue grew 8.1%, and 72.8% of that growth came from enterprise. SMB signed 100 more new customers than in Q2 but also lost 100 more, so net growth stayed at exactly 450. Over the same months SMB support replies slowed from 6.1 to 13.9 hours and SMB NPS fell from 41 to 29.

The deck ends on two decisions, each argued for and against:
- **Decision one:** move part of the Q4 SMB budget from winning customers to support.
- **Decision two:** change the SMB goal from new customers to net growth and revenue.

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

- **Placeholders:** the owner and decide-by slots on both decision slides are `[TK]`, plus one `[TK: check comp terms]`. I didn't fill these in because none of the files say who owns these decisions.
- **What the data can't show:** there's no count of active customers, so the deck shows churn as a share of new customers instead of a true churn rate. There are no customer IDs, so the deck can't link tickets to the customers who left. Both gaps are listed in the appendix.
- **Rerunning the check:** after any edit, run `python3 deck/verify_deck.py deck/customer_section.md`. Percents must keep one decimal place, and each number needs its segment and metric named on the same line.
- **Layout:** the .pptx files use pandoc's default template, so you'll want to restyle them in your deck template.

Nothing is committed. Everything new is in `deck/`.