-- =====================================================================
-- SonicWave churn: segment analysis
-- Table: subscribers  (load data/sonicwave_subscribers.csv as-is)
-- Written in standard SQL and tested in SQLite. Works in PostgreSQL/BigQuery
-- with at most minor changes (e.g. ROUND on NUMERIC in PostgreSQL).
-- churned = 1 means the customer cancelled in the last 90 days
-- Comments and formatting were tidied with the help of an AI assistant.
-- =====================================================================


-- Q1. Overall churn: should return 8,500 customers, 825 churned, 9.7%
SELECT COUNT(*)                       AS customers,
       SUM(churned)                   AS churned,
       ROUND(100.0 * AVG(churned), 1) AS churn_rate_pct
FROM subscribers;


-- Q2. Churn rate by one factor (swap last_ticket_topic for any column:
--     signup_channel, content_mix, plan_type, payment_method, age_group)
SELECT last_ticket_topic,
       COUNT(*)                                             AS customers,
       ROUND(100.0 * AVG(churned), 1)                       AS churn_rate_pct,
       ROUND(100.0 * SUM(churned) / (SELECT SUM(churned) FROM subscribers), 1)
                                                            AS share_of_all_churn_pct
FROM subscribers
GROUP BY last_ticket_topic
ORDER BY churn_rate_pct DESC;


-- Q3. The two high-risk segments vs everyone else
--     Note: 35 customers are in BOTH segments, and they are shown separately
--     here so no one is counted twice
WITH tagged AS (
  SELECT *,
         CASE WHEN last_ticket_topic = 'Billing' AND support_tickets_90d >= 2
              THEN 1 ELSE 0 END AS repeat_billing,
         CASE WHEN signup_channel = 'Partner promo' AND content_mix = 'Low-usage'
              THEN 1 ELSE 0 END AS promo_ghost
  FROM subscribers
)
SELECT CASE
         WHEN repeat_billing = 1 AND promo_ghost = 1 THEN 'Both segments'
         WHEN repeat_billing = 1 THEN 'Repeat billing problem'
         WHEN promo_ghost   = 1 THEN 'Promo Ghosts'
         ELSE 'Everyone else'
       END                                                  AS segment,
       COUNT(*)                                             AS customers,
       SUM(churned)                                         AS churned,
       ROUND(100.0 * AVG(churned), 1)                       AS churn_rate_pct,
       ROUND(100.0 * SUM(churned) / (SELECT SUM(churned) FROM subscribers), 1)
                                                            AS share_of_all_churn_pct
FROM tagged
GROUP BY 1
ORDER BY churn_rate_pct DESC;


-- Q4. Top 5 churn-risk segments (case stretch goal)
--     Groups by channel x listening mix x ticket topic x repeat tickets.
--     Groups under 30 customers are ignored so tiny groups don't top the list.
WITH segments AS (
  SELECT signup_channel,
         content_mix,
         last_ticket_topic,
         CASE WHEN support_tickets_90d >= 2 THEN '2+' ELSE '0-1' END AS ticket_level,
         COUNT(*)                       AS customers,
         SUM(churned)                   AS churned,
         ROUND(100.0 * AVG(churned), 1) AS churn_rate_pct
  FROM subscribers
  GROUP BY signup_channel, content_mix, last_ticket_topic, ticket_level
  HAVING COUNT(*) >= 30
)
SELECT *
FROM segments
ORDER BY churn_rate_pct DESC
LIMIT 5;


-- Q5. Daily intervention list: customers who just reached a 2nd billing
--     ticket and are still active. In production this would also filter on
--     the ticket date (e.g. opened in the last 24 hours).
SELECT subscriber_id, plan_type, monthly_spend, support_tickets_90d
FROM subscribers
WHERE last_ticket_topic = 'Billing'
  AND support_tickets_90d >= 2
  AND churned = 0
ORDER BY monthly_spend DESC;
-- Expected today: 297 customers
