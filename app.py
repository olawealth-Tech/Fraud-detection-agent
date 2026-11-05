import pandas as pd
import streamlit as st
from fraud_agent import analyse_transactions
from dashboard import render_dashboard
from styles import apply_styles

st.set_page_config(page_title="Fraud Detection Agent", page_icon="🛡️", layout="wide")
apply_styles()
st.markdown("""
<div class="fraud-hero">
  <span class="fraud-eyebrow">Shield / Intelligence workspace</span>
  <h1>Fraud Detection Agent</h1>
  <p>Intelligent transaction monitoring, explainable risk signals, and actionable insights.</p>
  <span class="fraud-tag">● ANALYSIS READY &nbsp; · &nbsp; Human-in-the-loop screening</span>
</div>
""", unsafe_allow_html=True)

with st.expander("Required CSV columns and example"):
    st.code("transaction_id,amount,hour,distance_from_home_km,failed_attempts,is_new_device,is_international\nTX001,1250,2,650,3,true,true")
    st.write("Boolean values accept true/false, yes/no, or 1/0. Amounts use your dataset's currency units.")

sample = pd.DataFrame([
    [f"TX{i:03d}", 45 + (i * 37) % 420, (9 + i) % 24, (i * 13) % 80, i % 2, i % 7 == 0, i % 9 == 0]
    for i in range(1, 31)
], columns=["transaction_id", "amount", "hour", "distance_from_home_km", "failed_attempts", "is_new_device", "is_international"])
sample.loc[4, ["amount", "hour", "distance_from_home_km", "failed_attempts", "is_new_device", "is_international"]] = [2400, 2, 900, 4, True, True]
sample.loc[17, ["amount", "hour", "distance_from_home_km", "failed_attempts", "is_new_device", "is_international"]] = [1800, 23, 700, 3, True, False]

uploaded = st.file_uploader("Upload transaction CSV", type=["csv"])
col_a, col_b = st.columns([1, 3])
with col_a:
    use_demo = st.button("Run with demo data", use_container_width=True)
run_upload = st.button("Analyse uploaded CSV", type="primary", disabled=uploaded is None, use_container_width=True)

if use_demo or run_upload:
    try:
        df = pd.read_csv(uploaded) if run_upload else sample.copy()
        result = analyse_transactions(df.to_dict(orient="records"))
        if result.get("error"):
            st.error(result["error"])
            st.session_state.pop("analysis_result", None)
        else:
            st.session_state["analysis_result"] = result
            st.session_state["analysis_source"] = "Uploaded CSV" if run_upload else "Demo data"
    except Exception as exc:
        st.session_state.pop("analysis_result", None)
        st.error(f"Could not analyse the file: {exc}")

if "analysis_result" in st.session_state:
    render_dashboard(st.session_state["analysis_result"], st.session_state.get("analysis_source", "Analysis"))
else:
    st.info("Upload a CSV or select 'Run with demo data' to see your dashboard.")

st.divider()
st.caption("Privacy: Uploaded data is processed within the app session. Do not upload real card numbers, CVVs, passwords, or sensitive personal data. Use synthetic or properly anonymised data for testing.")
