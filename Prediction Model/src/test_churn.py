"""Open a desktop form for experimenting with the saved churn model."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

import joblib
import pandas as pd


def main():
    model = joblib.load(ROOT / 'reports/churn_model/model.joblib')
    # One thread keeps small interactive predictions responsive.
    model.named_steps['classifier'].n_jobs = 1
    preprocess = model.named_steps['preprocess']
    numeric = list(preprocess.transformers_[0][2])
    categorical = list(preprocess.transformers_[1][2])
    encoder = preprocess.named_transformers_['categorical'].named_steps['encode']
    choices = dict(zip(categorical, encoder.categories_))
    defaults = dict(age_group='25-34', plan_type='Basic', tenure_months='18',
        monthly_spend='7.99', avg_weekly_hours='15', content_mix='Balanced',
        payment_method='Credit card', support_tickets_90d='0',
        last_ticket_topic='No ticket', signup_channel='Web')
    if '--smoke-test' in sys.argv:
        row = {key: float(value) if key in numeric else value for key, value in defaults.items()}
        score = model.predict_proba(pd.DataFrame([row]))[0, 1]
        assert 0 <= score <= 1
        print(f'Tester verified: example churn score = {score:.2%}')
        return

    import tkinter as tk
    from tkinter import ttk, messagebox
    window = tk.Tk()
    window.title('SonicWave churn model tester')
    window.geometry('620x700')
    frame = ttk.Frame(window, padding=24)
    frame.pack(fill='both', expand=True)
    ttk.Label(frame, text='Try the churn model', font=('Segoe UI', 18, 'bold')).grid(
        row=0, column=0, columnspan=2, sticky='w', pady=(0, 8))
    ttk.Label(frame, text='Change subscriber details, then click Predict.',
        wraplength=550).grid(row=1, column=0, columnspan=2, sticky='w', pady=(0, 16))
    variables = {}
    for index, column in enumerate(model.feature_names_in_, start=2):
        variables[column] = tk.StringVar(value=defaults[column])
        ttk.Label(frame, text=column.replace('_', ' ').capitalize()).grid(
            row=index, column=0, sticky='w', pady=6, padx=(0, 16))
        if column in choices:
            widget = ttk.Combobox(frame, textvariable=variables[column],
                values=list(choices[column]), state='readonly', width=25)
        else:
            widget = ttk.Entry(frame, textvariable=variables[column], width=28)
        widget.grid(row=index, column=1, sticky='ew', pady=6)
    result = tk.StringVar(value='Click Predict to see a result.')
    note = tk.StringVar(value='')

    def predict():
        try:
            row = {key: float(value.get()) if key in numeric else value.get()
                for key, value in variables.items()}
            if any(not pd.notna(row[key]) or row[key] < 0 or row[key] == float('inf') for key in numeric):
                raise ValueError('Numeric values must be finite and nonnegative.')
            for key in ['tenure_months', 'support_tickets_90d']:
                if not row[key].is_integer():
                    raise ValueError('Tenure and ticket count must be whole numbers.')
            score = float(model.predict_proba(pd.DataFrame([row]))[0, 1])
            label = 'CHURN' if score >= 0.5 else 'RETAINED'
            result.set(f'Prediction: {label}    |    Churn score: {score:.1%}')
            note.set('Decision threshold: 50%. Change one field and predict again to compare.')
        except ValueError as error:
            messagebox.showerror('Check the subscriber details', str(error))

    ttk.Button(frame, text='Predict', command=predict).grid(row=12, column=0,
        columnspan=2, sticky='ew', pady=18)
    ttk.Label(frame, textvariable=result, font=('Segoe UI', 12, 'bold'),
        wraplength=550).grid(row=13, column=0, columnspan=2, sticky='w')
    ttk.Label(frame, textvariable=note, wraplength=550).grid(row=14,
        column=0, columnspan=2, sticky='w', pady=10)
    ttk.Label(frame, text='How it works: subscriber details are encoded, then 400 decision '
        'trees combine their scores. Scores are uncalibrated and are not guaranteed probabilities. '
        'This model was evaluated on recorded churn; future churn requires temporal validation.',
        wraplength=550).grid(row=15, column=0, columnspan=2, sticky='w', pady=12)
    frame.columnconfigure(1, weight=1)
    window.mainloop()


if __name__ == '__main__':
    main()
