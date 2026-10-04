# Prediction Model

This folder contains the saved SonicWave churn model, desktop tester, training
code, aggregate results, and a bundled Python 3.14 runtime with its libraries.
It runs offline on compatible 64-bit Windows computers without installing Python
or referring to the original project. Keep the entire folder together; you can
copy it to another location, including a location whose name contains spaces.

## Run

Double-click **Run Prediction Model.bat**. Change subscriber details in the form
and click **Predict**. A churn score at or above 50% is classified as churn.
Scores have not been calibrated as probabilities.

Double-click **Verify Model.bat** to check isolated library paths, run a prediction,
and initialize the GUI libraries with a hidden window. If local subscriber data
and test predictions are present, it also reproduces all 1,700 saved predictions.
Double-click **Retrain Model.bat** to rebuild the model and evaluation
using data/subscribers.csv. The Git version excludes subscriber-level data; add
your training CSV at that path to retrain. Retraining replaces reports/churn_model.

## Contents

- runtime/: bundled Python, standard library, Tcl/Tk, and installed dependencies.
- src/: editable training and desktop tester code.
- data/subscribers.csv: local-only dataset for retraining; excluded from Git.
- data/case_dictionary.png: column definitions.
- reports/churn_model/model.joblib: saved preprocessing and random forest.
- reports/churn_model/report.md: evaluation and feature importance explanation.
- reports/churn_model/test_predictions.csv: local-only test results; excluded from Git.
- reports/churn_model/metrics.json and feature_importances.csv: evaluation details.

The saved model was evaluated on 1,700 held-out subscribers: 92.00% accuracy,
56.87% churn precision, and 72.73% churn recall. The predictors may overlap the
recorded churn period; future churn prediction needs temporal validation.
Prediction works without any subscriber dataset. The original local folder keeps
the dataset and per-subscriber predictions; sharing that entire local folder also
shares these files. They are excluded from the Git version.

Python and dependency licenses are preserved inside runtime/ and the installed
package metadata. This bundle targets Windows x64, not macOS or Linux.
