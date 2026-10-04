# The Vanishing Subscribers 🔍
**Case Closed 2026 · Data Science & Analytics Track · Team The Churn Detectives**

> SonicWave's churn more than doubled (4.1% → 9.7%) with no price or product change.
> We found that **13% of customers cause 72% of the churn**, and that one fix aimed at the biggest group can be tested in 30 days.

---

## The case in 30 seconds

| | Finding |
|---|---|
| **Suspect #1: Repeat billing problem** | Customers with 2+ billing tickets: **56.5% left**. They are 8% of customers but **47% of everyone who left**. One billing ticket is harmless (5.3%), the second is the alarm bell. |
| **Suspect #2: Promo Ghosts** | Partner-promo sign-ups who barely listen: **51.7% left**, **27% of everyone who left**. 8 in 10 are on Premium. |
| **Everyone else** | 7,418 customers (87%): only **3.1% left**. |
| **Cleared** | Playback complaints (4.9%, below average), ticket volume alone (6.1%), Premium plan (3.1% outside the segments), payment, age, tenure and listening hours. |
| **The fix** | The moment a customer opens a **2nd billing ticket**: route to a billing specialist, solve it on that contact, give a one-month credit. |
| **The test** | 30-day randomized test. Success = fix group churns at least 10 points less than control. Also tracking 3rd-ticket rate and first-contact resolution. |

## Repository structure

```
the-vanishing-subscribers/
├── README.md                       ← you are here
├── data/
│   └── sonicwave_subscribers.csv          raw data (never modified)
├── analysis/
│   ├── churn_analysis.xlsx         Excel pivots for every factor, 2-way pivots, number checks, charts
│   └── sql_deliverable.sql         SQL: overall churn, segments, top-5 risk segments, daily at-risk list
├── dashboard/
│   ├── SonicWave_Churn_Dashboard.pbix     Power BI dashboard (weekly view for the VP)
│   └── dashboard_preview.png              screenshot
├── presentation/
│   ├── Case_Closed_Deck.pptx
│   └── Case_Closed_Deck.pdf
└── docs/
    └── methodology.md              how we did it, step by step
```

## How to reproduce the numbers

| Tool | Steps |
|---|---|
| **Excel** | Open `analysis/churn_analysis.xlsx`. The **Summary** sheet confirms every headline number against the data (all rows show ✓ Match). One sheet per factor (`PT_...`). |
| **SQL** | Load `data/sonicwave_subscribers.csv` as a table named `subscribers`, then run `analysis/sql_deliverable.sql`. |
| **Power BI** | Open `dashboard/SonicWave_Churn_Dashboard.pbix`. |

## Methodology (short version)

1. **Checked the data:** no missing values, no duplicate IDs, valid categories. Nothing removed.
2. **Tested 9 hypotheses** one factor at a time: tickets, ticket topic, signup channel, listening mix, plan, payment, age, tenure, hours.
3. **Combined the factors that held up** to find small, high-churn segments, ranked by churn rate *and* share of total churn.
4. **Cross-checked with a prediction model** to confirm which factors matter most.
5. **Picked the intervention** with the biggest share of churn, a clear trigger moment, and a cause we control.
6. **Designed a 30-day test**, because our findings show correlation, not proof of cause.

Full detail: [`docs/methodology.md`](docs/methodology.md)

## Team

| Member | Role |
|---|---|
| **Roshan Roby** | Lead analyst & project manager: data checks, Excel analysis, SQL deliverable, segment definitions, number validation, coordination |
| **Saad Allahwall** | Visualization & modeling: Power BI dashboard, prediction model |
| **Abdul Rahman** | Presentation & documentation: slide deck, presentation script, repository organization |

## Notes

- Data is a synthetic snapshot built for Case Closed 2026. Revenue figures refer to this 8,500-customer sample.
- **Human-led, AI-assisted workflow.** We used an agentic AI assistant (Claude) as an analysis co-pilot: it automated the data-quality checks, built the formula-driven Excel workbook, and re-checked every headline number against the raw data. The team set the hypotheses, chose the segments, made the recommendation, and verified every figure. This let a 3-person team test 9 hypotheses and validate every number within the 3-hour case window.
