`[tool] Bash: {"command": "cd \"$PWD\" && git ls-files | head -100 && echo --- && git log --stat -1 | head -40", "description": "List project files and last commit"}`

`[tool] Glob: {"pattern": "**/*"}`

`[tool] Read: {"file_path": "<project>/notes.md"}`

`[tool] Read: {"file_path": "<project>/data/q3_metrics.csv"}`

Here's what I'd pitch before building anything. I've only read `notes.md` and `data/q3_metrics.csv`.

## What the data says

Your notes say last quarter's MRR charts were forgotten within a week, and Sales says SMB is "fine." The data tells a different, more memorable story:

| SMB, Q2 → Q3 | Q2 (Apr–Jun) | Q3 (Jul–Sep) | Change |
|---|---|---|---|
| New logos | 633 | 733 | **+16%** |
| Churned logos | 183 | 283 | **+55%** |
| **Net adds** | **450** | **450** | **0** |
| NPS (start → end) | 41 | 29 | −12 pts |
| First response time | 6.1h | 13.9h | 2.3× slower |
| Support tickets / mo | 920 | 1,530 | +66% |
| MRR | $182K | $192K | roughly flat |

**Sales is right that we're adding more logos than ever. Churn grew faster and ate every extra one: 100 more gross adds in Q3 produced zero more net growth.** By September, SMB was losing 104 customers for every 262 it signed. Meanwhile enterprise grew +15% MRR and mid-market +12%, with steady NPS and response times of about 2h and 5h.

## The ambitious version: a decision section, not a metrics recap

**Headline:** *"SMB is a leaky bucket: we're running faster to stand still."*

1. **The one number:** Q3 net SMB adds = 450, the same as Q2, despite record signups.
2. **Sales' claim, granted:** gross adds really are at a record. Concede it openly so the room trusts the rest.
3. **The leak:** monthly churn and gross adds as two lines, with the gap between them shrinking. Churn went from 23% of adds in April to 40% in September.
4. **The likely cause:** first-response time, NPS and churn plotted together. All three trend up or down in lockstep from April to September. I'd label this as correlation from 6 monthly data points, not proof.
5. **The contrast:** enterprise and mid-market are healthy with fast support, which suggests the product isn't the problem in those segments.
6. **What happens if nothing changes:** a straight-line projection showing net SMB adds turning negative within a few quarters if current trends continue. It would be clearly labeled as a trend line, not a forecast.
7. **The ask:** 2–3 concrete options for the execs to choose from, e.g. (a) fund SMB support/onboarding capacity to bring response time back to about 6h, (b) move some SMB acquisition spend into retention, (c) run a 30-day churn-reason sprint before deciding.
8. **Appendix:** the full segment table, so nobody can say the data was hidden.

**Format:** a slide deck built from the Slides artifact type (it downloads as .pptx or PDF). It would include speaker notes for each slide and a one-paragraph pre-read you can send execs before Thursday.

**Stretch add-on:** an interactive "fix the leak" page where execs move a response-time slider and see the implied net adds. This is the most memorable piece, but also the easiest to over-read, because the model would rest on 6 monthly data points. I'd only build it if you're comfortable presenting it as illustrative.

## What would make it stronger (I don't have this data)

- **SMB customer counts or revenue per account:** these would let me show the dollar cost of the churn, which execs remember better than logo counts.
- **Churn reasons, or churn by signup month:** these would turn "likely cause" into evidence.
- **Acquisition cost per customer (CAC):** this would let me say "we're paying $X to acquire customers we lose within months."

## Before I start

1. **Sales:** are you comfortable directly contradicting their "SMB is fine" claim in front of execs? If not, I'd soften slide 2, or you could preview the story with the Sales lead before Thursday.
2. **Dates:** I'm treating Q3 as Jul–Sep calendar months. Is that right?
3. **Scope:** do you want the full 8 slides, with or without the interactive page? Or a scaled-down version, the same story in 4 slides plus an appendix?

Once you confirm, I'll build it.