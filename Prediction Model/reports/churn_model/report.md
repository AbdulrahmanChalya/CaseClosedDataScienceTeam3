# SonicWave churn model

Random forest trained on 6,800 subscribers and evaluated on a held-out,
stratified test set of 1,700 subscribers (80/20 split; seed 42).
Subscriber IDs were excluded. Imputation and categorical encoding were fitted
only on training data. Churn is the positive class; prediction threshold is 0.5.
Hyperparameters were fixed before test evaluation; no test-set tuning was used.

| Metric | Test result |
|---|---:|
| Accuracy | 92.00% |
| Precision (churn) | 56.87% |
| Recall (churn) | 72.73% |
| ROC AUC | 0.8202 |
| Always predict retained: accuracy | 90.29% |

Precision means the fraction of predicted churners who actually churned.
Confusion matrix (rows actual retained/churned, columns predicted retained/churned):
[[1444, 91], [45, 120]].

## Top three features

Importance is the average decrease in test ROC AUC when the original feature
is shuffled, over 10 repeats. These are AUC units, not percentages of total
importance; correlated features can share or mask importance.

| Feature | Mean AUC decrease | Standard deviation |
|---|---:|---:|
| support_tickets_90d | 0.0826 | 0.0055 |
| signup_channel | 0.0752 | 0.0131 |
| content_mix | 0.0729 | 0.0110 |

## Interpretation limits

The dictionary defines churn as cancellation in the last 90 days, while some
predictors cover the last 8 weeks or 90 days. Their timing may overlap the outcome.
This model classifies recorded churn; prospective churn prediction requires
predictors captured before a subsequent churn window and temporal validation.
Feature importance describes predictive association, not causation. Class-weighted
forest probabilities are scores and have not been calibrated.
