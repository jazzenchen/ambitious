% Customer — Q3 2026 QBR

## Q3 in one line: total MRR grew 8.1%, but SMB growth has stalled

- Total MRR grew $65.9k to $878.5k; enterprise MRR supplied 72.8% of that growth.
- SMB signed 15.8% more new logos than in Q2, yet SMB net adds stayed at 450.
- Two decisions for today, both about SMB (last two slides).

::: notes
Lead with the tension, not the charts. The rest of the section backs these three lines.
:::

## Where Q3 MRR growth came from (end of June → end of September)

| Segment | Jun | Sep | Added | Share of growth |
|---|---|---|---|---|
| Enterprise MRR | $398.0k | $446.0k | +$48.0k | 72.8% |
| Mid-market MRR | $224.5k | $240.1k | +$15.6k | 23.7% |
| SMB MRR | $190.1k | $192.4k | +$2.3k | 3.5% |
| Total MRR | $812.6k | $878.5k | +$65.9k | |

## SMB: more new logos, same net adds

:::: {.columns}
::: {.column}

| SMB | Q2 | Q3 | Change |
|---|---|---|---|
| SMB new logos | 633 | 733 | +15.8% |
| SMB churned | 183 | 283 | +54.6% |
| SMB net adds | 450 | 450 | none |

:::
::: {.column}

- Sales is right that SMB is signing more: 733 SMB new logos in Q3 vs 633 in Q2.
- But SMB churned rose by the same 100, so SMB net adds did not move.
- SMB MRR rose only $2.3k in Q3 (net of churned, new, up- and downgrades; the file does not split these).


:::
::::
## SMB churn rose in every month since April

:::: {.columns}
::: {.column}

| | Apr | May | Jun | Jul | Aug | Sep |
|---|---|---|---|---|---|---|
| SMB churned | 48 | 61 | 74 | 83 | 96 | 104 |
| SMB churn as % of new | 22.9% | 30.8% | 32.9% | 34.6% | 41.6% | 39.7% |

:::
::: {.column}

- SMB churned equalled 39.7% of SMB new logos in September, up from 22.9% in April.

:::
::::

::: notes
We cannot give a churn *rate*: the data has no active-customer count. Churn as a share of new logos is the best ratio available.
:::

## SMB service and satisfaction slipped over the same months

:::: {.columns}
::: {.column}

| | Apr | Jun | Sep |
|---|---|---|---|
| SMB tickets | 920 | 1,180 | 1,530 |
| SMB first response (h) | 6.1 | 9.8 | 13.9 |
| SMB NPS | 41 | 35 | 29 |

:::
::: {.column}

- SMB first response more than doubled; mid-market went 4.2 → 5.1 h and enterprise 2.0 → 2.3 h.
- SMB churn, tickets, response time and NPS all moved together for six months.
- That is a trend, not proof of cause: six data points cannot show which drives which.


:::
::::
## Mid-market and enterprise: steady

:::: {.columns}
::: {.column}

| | Q2 | Q3 |
|---|---|---|
| Mid-market net adds | 89 | 89 |
| Enterprise net adds | 11 | 14 |
| Mid-market NPS (Jun → Sep) | 44 | 44 |
| Enterprise NPS (Jun → Sep) | 50 | 51 |

:::
::: {.column}

- Mid-market churned rose 13 → 18; worth watching, not yet a pattern.


:::
::::
## Decision one: move part of Q4 SMB spend from acquisition to support capacity?

**For**

- SMB first response went 6.1 → 13.9 h while SMB churn went 48 → 104 a month.
- SMB NPS fell 41 → 29 since April; mid-market NPS 47 → 44, enterprise NPS 52 → 51.
- Extra SMB acquisition in Q3 (+15.8% new logos) bought zero extra SMB net adds.

**Against**

- Cause is untested: churners may be poor-fit new logos, which support hours will not fix.
- SMB is 3.5% of Q3 MRR growth; the same money may return more in enterprise.

**What would settle it:** tickets and tenure of the SMB accounts that churned (needs customer IDs from CRM + support desk).
**Owner / decide by:** [TK: owner] / [TK: date]

## Decision two: should the SMB goal be net adds and MRR instead of new logos?

**For**

- SMB new logos rose 15.8% and SMB net adds did not move; a new-logos goal counted growth that segment churn then cancelled out.
- SMB MRR rose only $2.3k in Q3 while the logo goal was being hit.

**Against**

- Changing a sales goal mid-year disrupts comp plans [TK: check comp terms].
- A net-adds goal makes sales answer for churn that support and product may drive.

**What would settle it:** tenure of SMB accounts at churn (needs customer IDs). If most churners were signed this year, the logo goal is buying churn; if not, keep it.
**First step either way:** add active customers per segment to the monthly metrics file.
**Owner / decide by:** [TK: owner] / [TK: date]

## Appendix: data and method

- Source: data/q3_metrics.csv — monthly, by segment, April to September.
- Missing: active customer base (no churn rate), customer IDs (no ticket→churn link), churn reasons.
- Every number in this section is tied to that file by deck/verify_deck.py.
- Figures-only version: deck/customer_section_floor.md.
