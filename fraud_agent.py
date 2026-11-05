"""Explainable fraud-screening workflow orchestrated with LangGraph.

This is a demonstration decision-support system, not a production fraud model.
It never blocks transactions or makes a definitive finding of fraud.
"""
from __future__ import annotations

from typing import Any, TypedDict
import math
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from langgraph.graph import StateGraph, START, END

REQUIRED_COLUMNS = {"transaction_id", "amount", "hour", "distance_from_home_km",
                    "failed_attempts", "is_new_device", "is_international"}

class FraudState(TypedDict, total=False):
    raw_rows: list[dict[str, Any]]
    clean_rows: list[dict[str, Any]]
    results: list[dict[str, Any]]
    summary: dict[str, Any]
    error: str


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def validate_and_clean(state: FraudState) -> dict:
    rows = state.get("raw_rows", [])
    if not rows:
        return {"error": "The uploaded dataset is empty."}
    missing = REQUIRED_COLUMNS - set(rows[0].keys())
    if missing:
        return {"error": "Missing required columns: " + ", ".join(sorted(missing))}

    clean, seen = [], set()
    for row in rows:
        try:
            txid = str(row["transaction_id"]).strip()
            amount = float(row["amount"])
            hour = int(float(row["hour"]))
            distance = float(row["distance_from_home_km"])
            failed = int(float(row["failed_attempts"]))
            if not txid or txid in seen or not all(map(math.isfinite, [amount, distance])):
                continue
            if amount < 0 or distance < 0 or not 0 <= hour <= 23 or failed < 0:
                continue
            seen.add(txid)
            clean.append({
                "transaction_id": txid, "amount": amount, "hour": hour,
                "distance_from_home_km": distance, "failed_attempts": failed,
                "is_new_device": _as_bool(row["is_new_device"]),
                "is_international": _as_bool(row["is_international"]),
            })
        except (KeyError, TypeError, ValueError):
            continue
    if not clean:
        return {"error": "No valid transactions remained after data validation."}
    return {"clean_rows": clean}


def score_transactions(state: FraudState) -> dict:
    rows = state.get("clean_rows", [])
    if not rows:
        return {"error": state.get("error", "No valid transactions to score.")}

    feature_frame = pd.DataFrame([{ 
        "log_amount": math.log1p(r["amount"]),
        "hour": r["hour"],
        "distance_from_home_km": r["distance_from_home_km"],
        "failed_attempts": r["failed_attempts"],
        "is_new_device": int(r["is_new_device"]),
        "is_international": int(r["is_international"]),
    } for r in rows])

    anomaly_flags = [False] * len(rows)
    # IsolationForest is used only when there is enough data to fit a meaningful
    # unsupervised baseline. Rule-based scoring remains available for small files.
    if len(rows) >= 20:
        model = make_pipeline(StandardScaler(), IsolationForest(
            n_estimators=150, contamination="auto", random_state=42
        ))
        labels = model.fit_predict(feature_frame)
        anomaly_flags = [label == -1 for label in labels]

    results = []
    for i, row in enumerate(rows):
        score, reasons = 0, []
        if row["amount"] >= 1000:
            score += 25; reasons.append("High transaction amount (≥ 1,000)")
        if row["hour"] <= 5 or row["hour"] >= 23:
            score += 15; reasons.append("Unusual transaction hour")
        if row["distance_from_home_km"] >= 500:
            score += 20; reasons.append("Large distance from usual location")
        if row["failed_attempts"] >= 3:
            score += 20; reasons.append("Multiple failed attempts")
        if row["is_new_device"]:
            score += 10; reasons.append("New device")
        if row["is_international"]:
            score += 10; reasons.append("International transaction")
        if anomaly_flags[i]:
            score += 15; reasons.append("Unusual combination of transaction features (anomaly model)")
        score = min(score, 100)
        level = "High" if score >= 60 else "Medium" if score >= 30 else "Low"
        results.append({**row, "risk_score": score, "risk_level": level,
                        "flagged": score >= 30,
                        "reasons": "; ".join(reasons) if reasons else "No configured risk indicators"})
    return {"results": results}


def create_summary(state: FraudState) -> dict:
    results = state.get("results", [])
    if not results:
        return {"summary": {"total": 0, "flagged": 0, "high": 0, "medium": 0, "low": 0}}
    return {"summary": {
        "total": len(results),
        "flagged": sum(r["flagged"] for r in results),
        "high": sum(r["risk_level"] == "High" for r in results),
        "medium": sum(r["risk_level"] == "Medium" for r in results),
        "low": sum(r["risk_level"] == "Low" for r in results),
    }}


def build_graph():
    builder = StateGraph(FraudState)
    builder.add_node("validate_and_clean", validate_and_clean)
    builder.add_node("score_transactions", score_transactions)
    builder.add_node("create_summary", create_summary)
    builder.add_edge(START, "validate_and_clean")
    builder.add_conditional_edges(
        "validate_and_clean",
        lambda state: END if state.get("error") else "score_transactions",
        {"score_transactions": "score_transactions", END: END},
    )
    builder.add_conditional_edges(
        "score_transactions",
        lambda state: END if state.get("error") else "create_summary",
        {"create_summary": "create_summary", END: END},
    )
    builder.add_edge("create_summary", END)
    return builder.compile()


def analyse_transactions(rows: list[dict[str, Any]]) -> FraudState:
    """Run the full LangGraph workflow on transaction dictionaries."""
    return build_graph().invoke({"raw_rows": rows})
