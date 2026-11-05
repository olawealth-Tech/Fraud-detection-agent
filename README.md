# Fraud Detection Agent (LangGraph)

An explainable fraud-screening prototype. LangGraph coordinates validation, scoring, and summary nodes. The scoring node combines transparent rules with scikit-learn IsolationForest when at least 20 valid transactions are supplied.

## Features
- CSV upload and validation
- Duplicate transaction ID removal
- Explainable rule-based risk indicators
- Optional unsupervised anomaly detection for datasets with >=20 valid rows
- Low/Medium/High risk bands and downloadable CSV results
- Streamlit user interface

## Input schema
Required CSV columns:
`transaction_id, amount, hour, distance_from_home_km, failed_attempts, is_new_device, is_international`

Booleans accept `true/false`, `yes/no`, or `1/0`. Use synthetic or anonymised data. Do not upload card numbers, CVVs, passwords, or unnecessary personal information.

## Run locally
Python 3.11 or 3.12 recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, then click **Run with demo data**.

## Run tests
```bash
pytest -q
```

## Deploy to Streamlit Community Cloud
1. Push this project folder to a GitHub repository.
2. Visit https://share.streamlit.io and sign in with GitHub.
3. Choose **Create app**, select the repository and branch, and set the main file to `app.py`.
4. Deploy. No API key is required for this deterministic prototype.

## How the LangGraph workflow works
`START -> validate_and_clean -> score_transactions -> create_summary -> END`
If validation fails, the graph ends with an explanatory error. The scoring node applies configured rules and, for larger datasets, an IsolationForest anomaly model. All results include reasons.

## Risk rules (editable)
- Amount >= 1,000: +25
- Hour <= 5 or >= 23: +15
- Distance from home >= 500 km: +20
- Failed attempts >= 3: +20
- New device: +10
- International transaction: +10
- IsolationForest anomaly: +15

Scores are capped at 100. Low: 0–29, Medium: 30–59, High: 60–100. These are illustrative thresholds, not calibrated fraud probabilities. Adjust them only using representative, labelled data and a documented validation process.

## Limitations and responsible use
This is a learning/demo project, not a production financial control. IsolationForest detects unusual patterns, not fraud itself. The thresholds are illustrative and may create false positives or miss fraud. Do not automatically decline, freeze, report, or accuse anyone based only on this output. A qualified human should review alerts. Production deployment would require secure authentication, encryption, access controls, audit logging, monitoring, model validation, drift checks, fairness testing, and compliance/legal review.
