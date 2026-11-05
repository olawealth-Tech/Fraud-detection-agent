import pandas as pd
import plotly.express as px
import streamlit as st

RISK_ORDER = ["High", "Medium", "Low"]
COLORS = {"High": "#EF4444", "Medium": "#F59E0B", "Low": "#22C55E"}


def render_dashboard(result: dict, source: str = "Analysis") -> None:
    """Display scored transactions from fraud_agent.analyse_transactions."""
    df = pd.DataFrame(result.get("results", []))
    if df.empty:
        st.warning("No scored transactions were returned.")
        return

    df["risk_level"] = df["risk_level"].astype(str).str.title()
    df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["flagged"] = df["flagged"].astype(bool)

    total = len(df)
    flagged = int(df["flagged"].sum())
    high = int(df["risk_level"].eq("High").sum())
    medium = int(df["risk_level"].eq("Medium").sum())
    low = int(df["risk_level"].eq("Low").sum())

    st.subheader("Analysis overview")
    st.caption(f"Source: {source} | Heuristic scores are not fraud probabilities")
    cards = st.columns(5)
    for card, title, value in zip(
        cards,
        ["Transactions", "Flagged", "High risk", "Medium risk", "Flag rate"],
        [f"{total:,}", f"{flagged:,}", f"{high:,}", f"{medium:,}", f"{flagged / total:.1%}"],
    ):
        card.metric(title, value)

    counts = pd.DataFrame({
        "Risk": RISK_ORDER,
        "Transactions": [high, medium, low],
    })
    left, right = st.columns(2)
    with left:
        st.subheader("Risk distribution")
        fig = px.bar(counts, x="Risk", y="Transactions", color="Risk",
                     color_discrete_map=COLORS, text="Transactions",
                     category_orders={"Risk": RISK_ORDER})
        fig.update_layout(showlegend=False, height=360, margin=dict(l=10, r=10, t=15, b=10), paper_bgcolor="#111c32", plot_bgcolor="#111c32", font=dict(color="#cbd7ea"), xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#293953"))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Risk breakdown")
        nonzero = counts[counts["Transactions"] > 0]
        fig = px.pie(nonzero, names="Risk", values="Transactions", hole=0.55,
                     color="Risk", color_discrete_map=COLORS,
                     category_orders={"Risk": RISK_ORDER})
        fig.update_layout(height=360, margin=dict(l=10, r=10, t=15, b=10), paper_bgcolor="#111c32", font=dict(color="#cbd7ea"), legend=dict(font=dict(color="#cbd7ea")))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Transaction explorer")
    c1, c2 = st.columns(2)
    with c1:
        selected_risks = st.multiselect("Risk levels", RISK_ORDER, default=RISK_ORDER)
    with c2:
        only_flagged = st.checkbox("Show flagged only", value=False)

    filtered = df[df["risk_level"].isin(selected_risks)].copy()
    if only_flagged:
        filtered = filtered[filtered["flagged"]]

    amounts = df["amount"].dropna()
    if not amounts.empty and amounts.min() < amounts.max():
        minimum, maximum = float(amounts.min()), float(amounts.max())
        selected_range = st.slider("Transaction amount", min_value=minimum,
                                   max_value=maximum, value=(minimum, maximum))
        filtered = filtered[filtered["amount"].between(*selected_range)]

    st.caption(f"Showing {len(filtered):,} of {total:,} transactions")
    st.dataframe(filtered.sort_values("risk_score", ascending=False),
                 use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Flagged transactions requiring review")
    suspicious = df[df["flagged"]].sort_values("risk_score", ascending=False)
    if suspicious.empty:
        st.success("No transactions reached the configured flagging threshold.")
    else:
        st.warning(f"{len(suspicious)} transactions flagged for human review.")
        st.dataframe(suspicious, use_container_width=True, hide_index=True)

    st.subheader("Export reports")
    d1, d2 = st.columns(2)
    with d1:
        st.download_button("Download all scored transactions",
                           df.to_csv(index=False).encode("utf-8-sig"),
                           "fraud_analysis_results.csv", "text/csv",
                           use_container_width=True)
    with d2:
        st.download_button("Download flagged transactions",
                           suspicious.to_csv(index=False).encode("utf-8-sig"),
                           "flagged_transactions.csv", "text/csv",
                           use_container_width=True)
    st.info("Scores are heuristic screening indicators, not probabilities or proof of fraud. Review flagged transactions with authorised staff.")
