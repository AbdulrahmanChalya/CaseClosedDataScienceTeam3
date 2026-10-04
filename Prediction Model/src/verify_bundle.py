"""Verify isolated imports, saved predictions, and the bundled GUI libraries."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
assert sys.flags.isolated, 'Use the bundled Python executable.'
for entry in sys.path:
    assert Path(entry).resolve().is_relative_to(ROOT), f'External import path: {entry}'

import joblib
import numpy as np
import pandas as pd
import sklearn
import tkinter as tk
from tkinter import ttk

for module in [joblib, np, pd, sklearn, tk]:
    assert Path(module.__file__).resolve().is_relative_to(ROOT)
model = joblib.load(ROOT / 'reports/churn_model/model.joblib')
model.named_steps['classifier'].n_jobs = 1
data_path = ROOT / 'data/subscribers.csv'
predictions_path = ROOT / 'reports/churn_model/test_predictions.csv'
if '--example-only' not in sys.argv and data_path.exists() and predictions_path.exists():
    data = pd.read_csv(data_path).set_index('subscriber_id')
    saved = pd.read_csv(predictions_path)
    rows = data.loc[saved.subscriber_id].drop(columns='churned')
    scores = model.predict_proba(rows)[:, 1]
    np.testing.assert_allclose(scores, saved.churn_probability, rtol=1e-10, atol=1e-12)
    assert np.array_equal((scores >= .5).astype(int), saved.predicted_churn)
    assert np.array_equal(data.loc[saved.subscriber_id, 'churned'], saved.actual_churn)
    metrics = json.loads((ROOT / 'reports/churn_model/metrics.json').read_text())
    assert abs(np.mean(saved.actual_churn == saved.predicted_churn) - metrics['accuracy']) < 1e-12
    prediction_check = f'all {len(saved):,} held-out predictions match the saved results'
else:
    example = pd.DataFrame([dict(age_group='25-34', plan_type='Basic',
        tenure_months=18, monthly_spend=7.99, avg_weekly_hours=15,
        content_mix='Balanced', payment_method='Credit card',
        support_tickets_90d=0, last_ticket_topic='No ticket', signup_channel='Web')])
    score = model.predict_proba(example)[0, 1]
    assert np.isfinite(score) and 0 <= score <= 1
    prediction_check = f'saved model predicts an example profile (score {score:.2%})'
window = tk.Tk()
window.withdraw()
ttk.Frame(window).pack()
window.update_idletasks()
assert Path(window.tk.eval('info library')).resolve().is_relative_to(ROOT)
window.destroy()
print(f'PASS: all Python imports and Tcl/Tk files are inside {ROOT}')
print(f'PASS: {prediction_check}')
print(f'PASS: bundled desktop interface libraries initialize successfully')
