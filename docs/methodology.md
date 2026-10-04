# Methodology

How we went from 8,500 rows to one recommendation, step by step. Every number here can be reproduced from `data/sonicwave_subscribers.csv`. The Excel workbook (`analysis/churn_analysis.xlsx`) re-checks all of them on its Summary sheet.

---

## 1. The question

Between January and September 2026, SonicWave's monthly churn rose from 4.1% to 9.7%, with no change in price or features. The VP of Growth asked two questions:

1. **Who is leaving?**
2. **What would it take to stop them?**

## 2. The data

| Item | Detail |
|---|---|
| Source | `sonicwave_subscribers.csv` (synthetic snapshot provided by Case Closed 2026) |
| Rows | 8,500 (one per subscriber) |
| Columns | 12: profile, plan, tenure, spend, listening, payment, support tickets, signup channel, churn flag |
| Outcome | `churned` = 1 if the customer cancelled in the last 90 days |
| Overall churn | 825 of 8,500 = **9.7%** |

## 3. Data checks (Data Handling)

Before any analysis, we checked every row:

| Check | Result |
|---|---|
| Missing values | None in any column |
| Duplicate subscriber IDs | None (8,500 unique). 7 rows share every other value with another row, but they have different IDs and look like real look-alike customers, so we kept them |
| Valid categories | All category columns had only expected values (e.g. 4 plan types, 5 ticket topics) |
| Price consistency | Spend matches plan (Free = $0, etc.) |
| Logical consistency | "No ticket" customers always have 0 tickets, and every customer with a ticket topic has at least 1 ticket |
| Rows removed | **None**: the raw file was never modified |

**What we added (and why).** To make grouping easy in Excel and Power BI, we added 6 helper columns (the **Data** sheet of the workbook). No original values were changed.

| New column | Rule |
|---|---|
| `tickets_band` | Support tickets in 90 days: 0, 1, 2, 3+ |
| `tenure_band` | Months as a customer: 1–6, 7–12, 13–24, 25+ |
| `hours_band` | Avg weekly listening hours: 0–5, 5–10, 10–20, 20+ |
| `repeat_billing_flag` | 1 if `last_ticket_topic = Billing` **and** `support_tickets_90d >= 2` |
| `promo_lowusage_flag` | 1 if `signup_channel = Partner promo` **and** `content_mix = Low-usage` |
| `risk_segment` | Repeat billing problem / Promo Ghosts / Both segments / Everyone else |

The band cut-offs were our choice (the case did not define them). We picked round, easy-to-explain ranges.

## 4. Two kinds of percentage

We use two measures, and we label them clearly on every slide:

| Measure | Meaning | Example |
|---|---|---|
| **Churn rate** ("X% left") | Of the customers *in this group*, what share cancelled | 56.5% of repeat-billing customers left |
| **Share of all churn** ("X% of everyone who left") | Of the *825 customers who left*, what share came from this group | 47% of everyone who left came from the repeat-billing group |

A group can have a high churn rate but a small share of churn (if it is tiny), or the reverse. We needed both to choose where to act.

## 5. Hypotheses tested (Depth of Analysis)

We tested each factor on its own first, comparing churn rate across its groups.

| # | Hypothesis | What we found | Verdict |
|---|---|---|---|
| 1 | Support tickets drive churn | Billing tickets: 28.1% left vs 5.7% with no ticket | **Held up** (strongest) |
| 2 | Playback problems drive churn (leadership's suspicion) | Playback ticket: 4.9% left, *below* the 9.7% average | **Cleared** |
| 3 | Signup channel matters | Partner promo: 22.4% vs ~7.5% for Web, iOS, Android | **Held up** |
| 4 | Listening style matters | Low-usage: 22.6% vs ~7.4% for other mixes | **Held up** |
| 5 | Plan type matters | Premium 13.2% vs ~7–8% for others, **but** only 3.1% once Promo Ghosts are removed | **Cleared** (a decoy) |
| 6 | Payment method matters | 9.3%–10.5% across methods | **Cleared** |
| 7 | Age matters | 9.0%–10.2% across age groups | **Cleared** |
| 8 | Tenure matters | 8.1%–10.9% across tenure bands | **Cleared** (small effect) |
| 9 | Listening hours matter | 10.5 vs 10.7 hrs/week for leavers vs stayers | **Cleared** |

"Cleared" means the factor moves churn by about 2 points or less from the 9.7% average, or the gap disappears once the two risk segments are removed.

## 6. Finding the segments (combining factors)

Next we crossed the factors that held up, using two-way pivot tables in Excel (`analysis/churn_analysis.xlsx`, sheets `PT_topic_x_tickets` and `PT_channel_x_mix`).

**Segment 1: Repeat billing problem.** Filter: `last_ticket_topic = 'Billing' AND support_tickets_90d >= 2`

| Billing tickets | Customers | Churn rate |
|---|---|---|
| 1 | 847 | 5.3% |
| 2 | 547 | 57.2% |
| 3+ | 135 | 53.3% |
| **2+ (segment)** | **682** | **56.5%** |

- One billing ticket is harmless. The **second** one is where churn jumps 10×.
- **Ruling out "it's just ticket volume":** customers with 2+ tickets on *non-billing* topics churn at only **6.1%** (362 customers).
- Share of all churn: **47%** (385 of 825).

**Segment 2: Promo Ghosts.** Filter: `signup_channel = 'Partner promo' AND content_mix = 'Low-usage'`

| Group | Customers | Churn rate |
|---|---|---|
| Promo + Low-usage | 435 | 51.7% |
| Promo + other listening mixes | 845 | ~7.3% |
| Other channels + Low-usage | 842 | 7.6% |

- Neither factor alone explains it. **The combination does.**
- 350 of the 435 are on Premium, and 63% of those left. This is what makes Premium look risky overall.
- Share of all churn: **27%** (225 of 825).

**Everyone else:** 7,418 customers, **3.1%** churn, flat across age, plan, payment and channel (about 2.5%–4%).

**Overlap:** 35 customers are in both segments. Combined, the two segments cover 1,082 customers (**13%**) and 592 of the 825 who left (**72%**).

## 7. Model cross-check (stretch goal)

To check that our ranking was not just our judgment, we trained a prediction model on the same data.

<!-- SAAD: fill in model type, train/test split, accuracy, precision, recall and top 3-4 features -->
| Item | Result |
|---|---|
| Model | _[to be added]_ |
| Accuracy / precision / recall | _[to be added]_ |
| Top features | _[to be added]_ |

**How to read this honestly:**

- Only 9.7% of customers churn, so a model that predicts "nobody churns" is already about 90% accurate. Accuracy alone is misleading, which is why we also report precision and recall.
- We used the model to **confirm which factors matter**, not as the recommendation. The segments are simpler to explain and act on.

## 8. Correlation vs. cause

Everything above shows **who is at risk**, not **proof of why**. For example, the data cannot tell us whether billing issues *cause* churn or whether some other factor causes both. That is why the recommendation starts with a **randomized 30-day test** before full rollout.

## 9. Choosing the recommendation

| | Repeat billing | Promo Ghosts |
|---|---|---|
| Share of all churn | **47%** | 27% |
| Lost monthly revenue (in this data) | **$4.1K** of $9.1K | $2.9K of $9.1K |
| Clear trigger moment | **Yes**: the 2nd billing ticket | No single moment |
| Cause we control | **Yes**: support / billing process | Needs product onboarding + partner terms |
| Speed to launch | **Weeks** | Months |

**Recommendation:** the moment a customer opens a second billing ticket, route them to a billing specialist, resolve it on that contact, and give a one-month credit.

**Estimates (clearly labelled as estimates):**

- **Volume:** 682 customers reach 2+ billing tickets per 90 days, so about **227 per month**.
- **Credit cost:** 227 × ~$10.60 average bill ≈ **$2.4K/month**, plus specialist time.
- **Scenario, not a forecast:** halving this group's churn would keep ~190 customers and ~$2K/month in revenue.

## 10. 30-day test design

| Item | Detail |
|---|---|
| Who | Every customer who opens a 2nd billing ticket during the 30 days |
| Split | Random 50/50: the fix vs today's process |
| Main metric | % who cancel within 30 days (today's baseline: 56.5%) |
| Supporting metrics | % who open a 3rd ticket, % resolved on first contact |
| Success target | Fix group churn at least 10 points below control. This is a goal we set, not a forecast. |
| Decision | Day 30: if it wins, roll out to all customers. Then start Case #2 (Promo Ghost onboarding). |

## 11. Limitations / what we did not test

- **Snapshot data:** one point in time, so we cannot see churn trends month by month.
- **No billing details:** we cannot see *why* billing issues happen (errors, failed payments, double charges).
- **No partner details:** we cannot compare partner deals or promo terms.
- **Revenue figures** come from this 8,500-customer sample, not SonicWave's full base.
- **Small sub-segments:** some combinations in the SQL top-5 list have only 31–76 customers.

## 12. Tools

| Tool | Used for |
|---|---|
| **Excel** | Pivot tables for every factor, two-way pivots, a check sheet that confirms every headline number, charts (`analysis/churn_analysis.xlsx`) |
| **SQL** | Reproducible segment queries (`analysis/sql_deliverable.sql`) |
| **Prediction model** | Cross-check of the strongest churn drivers |
| **Power BI** | Weekly churn dashboard for the VP (`dashboard/`) |
| **PowerPoint** | Final presentation (`presentation/`) |
| **Agentic AI assistant (Claude)** | Analysis co-pilot: automated data-quality checks, built the formula-driven workbook, re-validated every headline number, commented and formatted the SQL code. **The team owned the hypotheses, decisions and final verification.** |

## 13. How we worked: human-led, AI-assisted

We treated AI as a **co-pilot, not an autopilot**:

| Step | Team | AI assistant |
|---|---|---|
| Frame the question and hypotheses | ✅ Decided what to test | |
| Data-quality checks | Reviewed results | ✅ Ran checks on all 8,500 rows |
| Excel workbook | Defined what each pivot should show | ✅ Built pivots, charts and the Summary check sheet |
| Segment definitions | ✅ Chose the filters and cut-offs | Confirmed sizes and churn rates |
| Recommendation | ✅ Chose billing over Promo Ghosts, designed the test | Stress-tested the numbers |
| SQL deliverable | ✅ Wrote the queries and logic | Added comments and formatted the code for readability |
| Final numbers | ✅ Verified against the data | Re-calculated every figure |

**Why it matters:** we spent less time building spreadsheets and more time testing hypotheses. That's how we covered 9 factors, two-way combinations and a model check within the case window. Every number in the deck traces back to a formula on the workbook's Summary sheet, so nothing depends on trusting the AI.
