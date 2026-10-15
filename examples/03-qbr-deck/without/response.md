I've built the 8-slide Customer section at `deck/q3_qbr_customer_section.pptx`, with speaker notes on every slide. **I haven't seen it rendered yet.** LibreOffice is missing from this Mac and pip couldn't download the official validator's packages. I only checked that the file structure is valid, so open it in PowerPoint before Thursday and look for text that overflows or overlaps.

**The story.** Your notes said last quarter's segment MRR charts were forgotten within a week, so this deck makes one argument instead. It also answers Sales' claim that SMB is "fine":

1. **Title:** "We're signing more SMB customers than ever, and losing them almost as fast."
2. **Q3 at a glance:** total MRR up 8.1%; SMB net new customers flat at 450; SMB first response time at 13.9 hours.
3. **Revenue:** enterprise drove 73% of new MRR. SMB added only $2.3K, despite 450 net new customers.
4. **SMB customers:** we signed 733 vs 633 in Q2, but lost 283 vs 183, so net growth was 450 both quarters. In September we lost 4 for every 10 signed; in April it was about 2.
5. **Support:** SMB first response went from 6.1h to 13.9h, tickets rose 66% and NPS fell from 41 to 29. Mid-market and enterprise stayed flat.
6. **The link:** SMB churn and response time rose together every month (correlation 0.99). The slide says this isn't proof: it's six data points and both numbers simply grew over time.
7. **All segments side by side:** mid-market and enterprise are healthy; every red number is SMB.
8. **Asks:** get SMB first response back under 6 hours; confirm the cause by Oct 31; report SMB on net new customers and net MRR, not gross sign-ups.

**Things to check before presenting:**
- **The asks on slide 8 are my proposal**, including the 6-hour target (your April level), the Oct 31 date and the staffing options. Change them to fit what you can actually commit to.
- **The $2.3K on 450 net new customers doesn't add up.** That's about $5 of MRR per customer. The data can't explain it: new customers on smaller plans, bigger customers leaving, or downgrades would each do it. Expect to be asked, or get the plan-mix data first.
- "Total MRR +8.1%" compares June with September, since there's no March data to compare quarter-end to quarter-end.

The colors are my own (charcoal, rust for SMB problems, teal for healthy), so restyle it if Acme has a QBR template. I didn't commit anything. The build script is at `<scratchpad>/build.js` if you want to rebuild it with changes.