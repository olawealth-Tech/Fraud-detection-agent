"""Presentation-only theme for the Streamlit fraud dashboard."""
import streamlit as st

CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root { --ink:#e9efff; --muted:#9baac8; --panel:#111c32; --line:#263654; --accent:#64e3cf; }
html, body, [class*="css"], [data-testid="stApp"] {font-family:'DM Sans',sans-serif;}
[data-testid="stAppViewContainer"], .stApp {background:radial-gradient(ellipse at 80% 0%,#172d4b 0%,transparent 37%),linear-gradient(145deg,#081120 0%,#0d172b 65%,#101a30 100%);color:var(--ink);}
[data-testid="stHeader"] {background:transparent;}
[data-testid="stMainBlockContainer"] {max-width:1440px;padding-top:2.2rem;padding-bottom:4rem;}
h1,h2,h3 {font-family:'Manrope',sans-serif!important;letter-spacing:-.035em!important;color:#f3f7ff!important;}
h1 {font-weight:800!important;font-size:clamp(2rem,3.5vw,3.2rem)!important;}
h2,h3 {font-weight:750!important;}
p, label, [data-testid="stCaptionContainer"] {color:#b7c4dc;}
[data-testid="stCaptionContainer"] {font-size:.87rem;}
[data-testid="stMetric"] {background:linear-gradient(160deg,rgba(28,43,70,.96),rgba(15,27,47,.96));border:1px solid #2b3e5e;border-radius:18px;padding:22px 18px;min-height:126px;box-shadow:0 14px 35px rgba(0,0,0,.13);transition:transform .18s,border-color .18s;}
[data-testid="stMetric"]:hover {transform:translateY(-3px);border-color:#4e7d93;}
[data-testid="stMetricLabel"] {color:#a9b9d4!important;font-weight:600;}
[data-testid="stMetricValue"] {color:#f5f8ff!important;font-family:'Manrope',sans-serif;font-weight:800;font-size:clamp(1.5rem,2.5vw,2.15rem);}
[data-testid="stVerticalBlockBorderWrapper"] {border-radius:18px;}
[data-testid="stPlotlyChart"] {background:#111c32;border:1px solid #263654;border-radius:18px;padding:10px 8px;overflow:hidden;}
[data-testid="stDataFrame"] {border:1px solid #2b3e5e;border-radius:14px;overflow:hidden;}
[data-testid="stFileUploader"] {border:1px dashed #477188;background:rgba(17,28,50,.85);border-radius:16px;padding:14px;}
[data-testid="stFileUploaderDropzone"] {background:transparent;border:0;}
.stButton>button[kind="primary"], [data-testid="stDownloadButton"] button {background:linear-gradient(105deg,#35bba9,#54d9c5)!important;color:#061d26!important;border:0!important;border-radius:12px!important;font-weight:800!important;box-shadow:0 8px 20px rgba(30,183,162,.16);}
.stButton>button:not([kind="primary"]) {background:#1b2b47;color:#e5f1ff;border:1px solid #385071;border-radius:12px;font-weight:650;}
.stButton>button:hover, [data-testid="stDownloadButton"] button:hover {filter:brightness(1.1);transform:translateY(-1px);}
.stButton>button, [data-testid="stDownloadButton"] button {transition:transform .15s,filter .15s;min-height:2.8rem;}
[data-baseweb="select"]>div, [data-baseweb="input"]>div {background:#17253e!important;border-color:#3a5273!important;border-radius:10px!important;}
[data-testid="stExpander"] {background:rgba(18,32,54,.7);border:1px solid #2a3b59;border-radius:14px;}
hr {border-color:#293953!important;opacity:.8;}
.fraud-hero {background:linear-gradient(110deg,rgba(28,61,83,.95),rgba(17,31,56,.97));border:1px solid #37536b;border-radius:22px;padding:30px 34px;margin-bottom:22px;box-shadow:0 18px 44px rgba(0,0,0,.15);}
.fraud-eyebrow {display:inline-block;color:#74ebd5;font-size:.74rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase;margin-bottom:12px;}
.fraud-hero h1 {margin:0 0 9px 0!important;line-height:1.18;}
.fraud-hero p {margin:0;color:#b9cbe0;font-size:1rem;}
.fraud-tag {display:inline-block;margin-top:18px;border:1px solid #3d766f;background:#173d43;color:#a7f6e6;border-radius:999px;padding:6px 12px;font-size:.76rem;font-weight:700;}
.fraud-section {margin-top:10px;color:#f0f5ff;font-family:'Manrope',sans-serif;font-weight:800;font-size:1.3rem;}
[data-testid="stAlert"] {border-radius:12px;}
@media(max-width:750px){[data-testid="stMainBlockContainer"]{padding:1rem}.fraud-hero{padding:22px 18px}[data-testid="stMetric"]{min-height:105px;padding:16px 12px}}
</style>
"""

def apply_styles():
    st.markdown(CSS, unsafe_allow_html=True)
