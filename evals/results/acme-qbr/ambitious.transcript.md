`[tool] Bash: {"command": "cd \"$PWD\" && git ls-files && ls -la && git log --stat -3 | head -40", "description": "List project files and recent history"}`

`[tool] Bash: {"command": "command -v python3 duckdb sqlite3 node gh csvkit marp pandoc; gh auth status 2>&1 | head -3; python3 -c \"import os,re;print(*sorted(k for k in os.environ if re.search('token|key|secret|dsn',k,re.I)))\"", "description": "Check available tools and credential names"}`

`[tool] Bash: {"command": "cat notes.md; echo ---; cat data/q3_metrics.csv", "description": "Show the notes and Q3 metrics data"}`

`[tool] Bash: {"command": "python3 -I -c \"\nimport csv\nr=list(csv.DictReader(open('data/q3_metrics.csv')))\nfor seg in ['smb','mid_market','enterprise']:\n  s=[x for x in r if x['segment']==seg]\n  q2=s[:3];q3=s[3:]\n  f=lambda q,k:sum(int(x[k]) for x in q)\n  print(seg,'Q2 new/churn/net',f(q2,'new_customers'),`

Sales says SMB is fine because sign-ups hit a record, but SMB cancellations doubled. SMB gained the same 450 net customers in Q3 as in Q2, and its revenue barely grew. I recommend rung 2: build the section around the two decisions execs need to make, with every number checked by a script against your CSV.

```text
── /ambitious ──────────────────────────────────────────────────────
asked    Q3 QBR customer section, ~8 slides (slides.md, inferred)
found    SMB churn 48→104/mo Apr→Sep; Q3 net adds 450 = Q2's 450
doubt    "SMB is fine, more logos" → SMB MRR +1.2% Jun→Sep, ent +12%
stakes   last deck forgotten in a week; SMB NPS 41→29, reply 6→14 h

  3 ▲    replace MRR charts: monthly segment alert, shadow 1 quarter
  2 │    the 2 exec decisions on SMB, each argued both ways        ◀
  1 │    what moved in Q3 and why (trend, causes untested) + actions
  0 ┷    floor: 8 slides, every figure recomputed from q3_metrics.csv

deeper   per-account churn + ticket export to test the reply-time link
wider    analyst: MRR bridge · ops: queue load math · short: weakest claim
target   4 of 5 cold readers name the SMB call in 2 min (not measured)
judge    check.py traces each slide figure to CSV rows, tier 1; readers t3
access   ✓ python3 pandoc gh · ✗ customer base count → no churn rate
cost     floor ~20 min · rung 2 ~50 min, ~3× tokens · you ~20 min
── reply: go (rung 2) · go 1 · go 0 (floor only) ───────────────────
```

```text
Build the ~8-slide Customer section of Acme's Q3 exec QBR from data/q3_metrics.csv (monthly new, churned, MRR, NPS, tickets and first-response hours by segment, Apr–Sep 2026), as slides.md. First write a script that pulls every figure out of the slides and recomputes it from the CSV rows. Run it on a draft with one planted wrong number to prove it fails, and deliver plain slides that pass it before going further. Then build the section around the decisions execs need to make. The key finding: SMB sign-ups hit a record 262 in September, but SMB churn rose from 48 to 104 a month. SMB net adds were flat at 450 in both Q2 and Q3, and SMB MRR grew only 1.2% from Jun to Sep while enterprise grew 12%. Meanwhile SMB NPS fell from 41 to 29 and first response went from 6.1 to 13.9 hours. For each decision (for example, funding SMB support or slowing SMB acquisition), argue both sides with the number each side depends on. Call the churn-vs-response-time link a trend, not a cause: there are only 6 points and the data has no active-customer count, so no churn rate. Target: 4 of 5 cold readers can state the SMB decision within 2 minutes. Report any figure the check can't trace, and any target missed, with numbers.
```