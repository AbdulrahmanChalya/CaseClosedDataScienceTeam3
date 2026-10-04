"""Train a reproducible churn classifier and report held-out performance."""
import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('reports/churn_model'))
    args = parser.parse_args()
    data = pd.read_csv(args.input)
    if data.empty or data.subscriber_id.duplicated().any():
        raise ValueError('Require nonempty data with unique subscriber IDs.')
    if data.churned.isna().any() or set(data.churned.unique()) != {0, 1}:
        raise ValueError('Require binary churned labels with both classes.')
    X = data.drop(columns=['subscriber_id', 'churned'])
    y = data.churned.astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42)
    numeric = X.select_dtypes(include='number').columns.tolist()
    categorical = X.columns.difference(numeric).tolist()
    preprocessing = ColumnTransformer([
        ('numeric', SimpleImputer(strategy='median'), numeric),
        ('categorical', Pipeline([
            ('impute', SimpleImputer(strategy='most_frequent')),
            ('encode', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ]), categorical)
    ])
    model = Pipeline([
        ('preprocess', preprocessing),
        ('classifier', RandomForestClassifier(n_estimators=400, min_samples_leaf=5,
            class_weight='balanced', random_state=42, n_jobs=-1))
    ])
    model.fit(X_train, y_train)
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    metrics = {
        'model': 'Random forest', 'sklearn_version': sklearn.__version__,
        'random_seed': 42, 'threshold': 0.5, 'train_rows': len(X_train),
        'test_rows': len(X_test), 'test_churn_rate': float(y_test.mean()),
        'accuracy': accuracy_score(y_test, predictions),
        'precision_churn': precision_score(y_test, predictions, zero_division=0),
        'recall_churn': recall_score(y_test, predictions, zero_division=0),
        'roc_auc': roc_auc_score(y_test, probabilities),
        'always_retain_accuracy': float((y_test == 0).mean()),
        'confusion_matrix_rows_actual_columns_predicted_0_1': confusion_matrix(y_test, predictions).tolist()
    }
    # Permute original columns so all one-hot levels count as one feature.
    importance = permutation_importance(model, X_test, y_test, scoring='roc_auc',
        n_repeats=10, random_state=42, n_jobs=1)
    features = pd.DataFrame({'feature': X.columns,
        'mean_auc_drop': importance.importances_mean,
        'std_auc_drop': importance.importances_std}).sort_values('mean_auc_drop', ascending=False)
    args.output.mkdir(parents=True, exist_ok=True)
    features.to_csv(args.output / 'feature_importances.csv', index=False)
    (args.output / 'metrics.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    pd.DataFrame({'subscriber_id': data.loc[X_test.index, 'subscriber_id'],
        'actual_churn': y_test, 'predicted_churn': predictions,
        'churn_probability': probabilities}).to_csv(args.output / 'test_predictions.csv', index=False)
    joblib.dump(model, args.output / 'model.joblib')
    report = f"""# SonicWave churn model

Random forest trained on {len(X_train):,} subscribers and evaluated on a held-out,
stratified test set of {len(X_test):,} subscribers (80/20 split; seed 42).
Subscriber IDs were excluded. Imputation and categorical encoding were fitted
only on training data. Churn is the positive class; prediction threshold is 0.5.
Hyperparameters were fixed before test evaluation; no test-set tuning was used.

| Metric | Test result |
|---|---:|
| Accuracy | {metrics['accuracy']:.2%} |
| Precision (churn) | {metrics['precision_churn']:.2%} |
| Recall (churn) | {metrics['recall_churn']:.2%} |
| ROC AUC | {metrics['roc_auc']:.4f} |
| Always predict retained: accuracy | {metrics['always_retain_accuracy']:.2%} |

Precision means the fraction of predicted churners who actually churned.
Confusion matrix (rows actual retained/churned, columns predicted retained/churned):
{metrics['confusion_matrix_rows_actual_columns_predicted_0_1']}.

## Top three features

Importance is the average decrease in test ROC AUC when the original feature
is shuffled, over 10 repeats. These are AUC units, not percentages of total
importance; correlated features can share or mask importance.

| Feature | Mean AUC decrease | Standard deviation |
|---|---:|---:|
"""
    for row in features.head(3).itertuples():
        report += f'| {row.feature} | {row.mean_auc_drop:.4f} | {row.std_auc_drop:.4f} |\n'
    report += """
## Interpretation limits

The dictionary defines churn as cancellation in the last 90 days, while some
predictors cover the last 8 weeks or 90 days. Their timing may overlap the outcome.
This model classifies recorded churn; prospective churn prediction requires
predictors captured before a subsequent churn window and temporal validation.
Feature importance describes predictive association, not causation. Class-weighted
forest probabilities are scores and have not been calibrated.
"""
    (args.output / 'report.md').write_text(report, encoding='utf-8')
    print(json.dumps(metrics, indent=2))
    print(features.head(3).to_string(index=False))


if __name__ == '__main__':
    main()
