import os
import json
import shutil
import subprocess
import tempfile
import traceback
import cv2
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageOps
# ----------------------------------------------------------------------------

# PAGE CONFIG

# ----------------------------------------------------------------------------
st.set_page_config(page_title="TrekStep AI", page_icon="🐎", layout="wide")
# ----------------------------------------------------------------------------
# THEME — "TREKSTEP OUTDOOR-AI" (single, organized CSS block)
# Palette: forest green · teal · golden yellow · orange · sky blue · mint
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* =====================================================================
       1. DESIGN TOKENS  (forest · teal · gold · orange · sky · mint)
       ===================================================================== */
    :root {
        --forest:      #285943;
        --forest-dk:   #1d4433;
        --teal:        #2F7D75;
        --teal-dk:     #266862;
        --gold:        #F4C95D;
        --orange:      #E89B4A;
        --sky:         #75B9E6;
        --mint:        #DDF2E5;
        --soft-yellow: #FFF3C4;
        --soft-orange: #FFE0BD;
        --soft-blue:   #DCEFF8;
        --soft-green:  #E5F3E9;
        --bg:          #F4F8F5;
        --card:        #FFFFFF;
        --ink:         #26352C;
        --ink-2:       #66756C;
        --danger:      #D95D5D;
        --danger-bg:   #FCE5E5;
        --caution:     #E5A93D;
        --caution-bg:  #FFF2CF;
        --safe:        #4E9B68;
        --safe-bg:     #E2F3E7;
        --line:        rgba(40, 89, 67, 0.14);
        --shadow:      0 6px 18px rgba(40, 89, 67, 0.10);
        --shadow-lg:   0 14px 34px rgba(40, 89, 67, 0.16);
        --radius:      18px;
        --radius-sm:   12px;
        --font: Inter, "Segoe UI", -apple-system, BlinkMacSystemFont, "SF Pro Text",
                "Helvetica Neue", Arial, sans-serif;
    }
    /* =====================================================================
       2. PAGE BACKGROUND + SUBTLE OUTDOOR DECOR (behind all content)
       ===================================================================== */
    html, body, .stApp, [class*="st-"] { font-family: var(--font); }

    .stApp {
        background: var(--bg);
        color: var(--ink);
    }
    /* soft glows: sky (top-right), gold (right), green (bottom-left) */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background:
            radial-gradient(620px 420px at 88% -6%, rgba(117, 185, 230, 0.30), transparent 70%),
            radial-gradient(520px 420px at 102% 46%, rgba(244, 201, 93, 0.22), transparent 70%),
            radial-gradient(720px 520px at 8% 108%, rgba(78, 155, 104, 0.20), transparent 70%);
    }
    /* faint layered mountain ridge along the bottom */
    .stApp::after {
        content: "";
        position: fixed;
        left: 0; right: 0; bottom: 0;
        height: 230px;
        z-index: 0;
        pointer-events: none;
        opacity: 0.55;
        background-repeat: no-repeat;
        background-position: bottom center;
        background-size: 100% 100%;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 230' preserveAspectRatio='none'%3E%3Cpath d='M0 230V150l140-70 120 60 170-100 150 90 160-60 190 100 130-70 180 80 200-70v220z' fill='%23cfe6d6' fill-opacity='.45'/%3E%3Cpath d='M0 230V185l180-60 150 50 200-80 170 80 180-50 220 70 140-40 200 50v75z' fill='%2394c7a8' fill-opacity='.30'/%3E%3C/svg%3E");
    }
    [data-testid="stAppViewContainer"] {
        position: relative;
        z-index: 1;
        background: transparent !important;
    }
    section.main, .main { background: transparent !important; }
    header[data-testid="stHeader"] { background: transparent; }
    .main .block-container,
    div[data-testid="stMainBlockContainer"] {
        max-width: 1400px;
        padding: 2.4rem 2.4rem 4.5rem 2.4rem;
    }
    p, li { color: #34463b; line-height: 1.6; }
    strong { color: var(--forest); font-weight: 700; }
    ::selection { background: var(--gold); color: var(--forest-dk); }
    hr {
        border: 0 !important;
        border-top: 1px solid var(--line) !important;
        margin: 1.6rem 0 !important;
    }
    /* =====================================================================
       3. HEADER / BRAND
       ===================================================================== */
    h1 {
        color: var(--forest) !important;
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em !important;
        line-height: 1.1 !important;
        margin: 0 !important;
        padding: 1.5rem 9rem 1.6rem 1.8rem !important;
        border: 1px solid var(--line);
        border-radius: 22px;
        box-shadow: var(--shadow);
        background:
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 120'%3E%3Ccircle cx='235' cy='34' r='15' fill='%23F4C95D' fill-opacity='.75'/%3E%3Cpath d='M0 120L70 36l45 52 40-44 75 76z' fill='%232F7D75' fill-opacity='.30'/%3E%3Cpath d='M90 120l62-62 48 50 36-30 64 42z' fill='%23285943' fill-opacity='.30'/%3E%3C/svg%3E")
                right bottom / auto 100% no-repeat,
            linear-gradient(100deg, #E5F3E9 0%, #DCEFF8 62%, #FFF3C4 100%);
    }
    /* animated green + gold accent line above the brand name */
    div[data-testid="stMainBlockContainer"] h1::before,
    .main .block-container h1::before {
        content: "";
        display: block;
        width: 56px;
        height: 5px;
        border-radius: 999px;
        margin-bottom: 14px;
        background: linear-gradient(90deg, var(--forest) 0 60%, var(--gold) 60% 100%);
        transition: width 400ms ease;
    }
    div[data-testid="stMainBlockContainer"] h1:hover::before { width: 92px; }
    h5 {
        color: var(--teal) !important;
        font-weight: 650 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.01em !important;
        margin: 0.9rem 0 1.4rem 0.2rem !important;
    }
    h2, h3 {
        color: var(--forest) !important;
        font-weight: 750 !important;
        letter-spacing: -0.02em !important;
    }
    /* coloured section bars (default = teal -> green) */
    div[data-testid="stMainBlockContainer"] h3::before {
        content: "";
        display: inline-block;
        width: 6px;
        height: 1.05em;
        border-radius: 4px;
        margin-right: 10px;
        vertical-align: -0.17em;
        background: linear-gradient(180deg, var(--teal), var(--safe));
    }
    /* image columns: Original = sky/teal, AI Guidance = green */
    div[data-testid="stColumn"]:has(img):nth-child(1) h3::before { background: linear-gradient(180deg, var(--sky), var(--teal)) !important; }
    div[data-testid="stColumn"]:has(img):nth-child(2) h3::before { background: linear-gradient(180deg, var(--safe), var(--forest)) !important; }
    /* analysis columns: terrain / hazards = orange, recommendation = green */
    div[data-testid="stColumn"]:has([data-testid="stDataFrame"]):nth-child(1) h3::before { background: linear-gradient(180deg, var(--gold), var(--orange)) !important; }
    div[data-testid="stColumn"]:has([data-testid="stDataFrame"]):nth-child(2) h3::before { background: linear-gradient(180deg, var(--safe), var(--forest)) !important; }
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: var(--ink-2) !important;
        font-size: 0.82rem !important;
        line-height: 1.55;
    }
    /* =====================================================================
       4. SIDEBAR — FOREST-GREEN CONTROL PANEL
       ===================================================================== */
    section[data-testid="stSidebar"] {
        background:
            radial-gradient(260px 220px at 100% 0%, rgba(244, 201, 93, 0.16), transparent 70%),
            linear-gradient(180deg, #2f6a51 0%, var(--forest) 45%, var(--forest-dk) 100%);
        border-right: 3px solid var(--gold);
    }
    section[data-testid="stSidebar"] > div { background: transparent; }
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] { padding-top: 1.6rem; }
    section[data-testid="stSidebar"] h2 {
        color: var(--gold) !important;
        font-size: 0.82rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.16em !important;
        text-transform: uppercase;
        padding: 0 0 0.8rem 0 !important;
        margin-bottom: 0.6rem;
        border-bottom: 2px solid rgba(244, 201, 93, 0.55);
    }
    section[data-testid="stSidebar"] h3 {
        color: var(--gold) !important;
        font-size: 0.82rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.16em !important;
        text-transform: uppercase;
        margin-top: 1.8rem !important;
        padding: 1.2rem 0 0.8rem 0 !important;
        border-top: 1px solid rgba(255, 255, 255, 0.22);
        border-bottom: 2px solid rgba(244, 201, 93, 0.55);
    }
    section[data-testid="stSidebar"] h3::before { display: none !important; }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] label p,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #F4F8F5 !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #BFDCCB !important;
    }
    section[data-testid="stSidebar"] [data-testid="stTickBarMin"],
    section[data-testid="stSidebar"] [data-testid="stTickBarMax"] {
        color: #CFE5D6 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSliderThumbValue"] {
        color: var(--gold) !important;
        font-weight: 800;
    }
    section[data-testid="stSidebar"] svg { color: #F4F8F5; }
    /* inputs: soft mint, rounded, green border */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {
        background: var(--mint) !important;
        border-radius: var(--radius-sm) !important;
    }
    div[data-baseweb="input"] {
        border: 1.5px solid var(--safe) !important;
        transition: border-color 150ms ease, box-shadow 150ms ease;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 3px rgba(244, 201, 93, 0.40);
    }
    input { color: var(--ink) !important; font-weight: 600; }
    input::placeholder { color: #7f9a8a !important; font-weight: 400; }
    div[data-testid="stNumberInput"] button {
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        color: var(--forest) !important;
    }
    div[data-testid="stNumberInput"] button svg { color: var(--forest) !important; }
 
    /* slider: gold handle (track follows the theme primary colour) */
    div[data-baseweb="slider"] [role="slider"] {
        background: var(--gold) !important;
        border: 3px solid #fff !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    }
    /* checkbox */
    label[data-baseweb="checkbox"] > span:first-of-type { border-color: var(--gold) !important; }
    div[data-testid="stCheckbox"] label p { font-weight: 650; }
    /* =====================================================================
       5. METRIC CARDS
       ===================================================================== */
    div[data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--line);
        border-top: 5px solid var(--teal);
        border-radius: var(--radius);
        padding: 16px 22px 18px 22px;
        box-shadow: var(--shadow);
        transition: transform 180ms ease, box-shadow 180ms ease;

    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg);
    }
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] p {
        color: var(--forest) !important;
        opacity: 0.8;
        font-size: 0.72rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] div {
        color: var(--forest-dk) !important;
        font-size: 1.9rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
        font-variant-numeric: tabular-nums;
    }
    /* video-result metrics: mint / yellow / orange */
    div[data-testid="stColumn"]:nth-child(1) div[data-testid="stMetric"] { background: linear-gradient(180deg, var(--soft-green), #fff 85%); border-top-color: var(--safe); }
    div[data-testid="stColumn"]:nth-child(2) div[data-testid="stMetric"] { background: linear-gradient(180deg, var(--soft-yellow), #fff 85%); border-top-color: var(--gold); }
    div[data-testid="stColumn"]:nth-child(3) div[data-testid="stMetric"] { background: linear-gradient(180deg, var(--soft-orange), #fff 85%); border-top-color: var(--orange); }
    /* top row (marker added in main()): location = blue, destination = yellow, safety = green */
    :is(.element-container, [data-testid="stElementContainer"]):has(.ts-top-metrics) { display: none; }
 
    :is(.element-container, [data-testid="stElementContainer"]):has(.ts-top-metrics) + div div[data-testid="stColumn"]:nth-child(1) div[data-testid="stMetric"] {
        background: linear-gradient(180deg, var(--soft-blue), #fff 90%); border-top-color: var(--sky);
    }
    :is(.element-container, [data-testid="stElementContainer"]):has(.ts-top-metrics) + div div[data-testid="stColumn"]:nth-child(2) div[data-testid="stMetric"] {
        background: linear-gradient(180deg, var(--soft-yellow), #fff 90%); border-top-color: var(--gold);
    }
    :is(.element-container, [data-testid="stElementContainer"]):has(.ts-top-metrics) + div div[data-testid="stColumn"]:nth-child(3) div[data-testid="stMetric"] {
        background: linear-gradient(180deg, var(--safe-bg), #fff 90%); border-top-color: var(--safe);
        box-shadow: 0 10px 28px rgba(78, 155, 104, 0.25);
    }
    :is(.element-container, [data-testid="stElementContainer"]):has(.ts-top-metrics) + div div[data-testid="stColumn"]:nth-child(3) div[data-testid="stMetricValue"] div {
        font-size: 2.4rem !important;
        color: var(--safe) !important;
    }
    :is(.element-container, [data-testid="stElementContainer"]):has(.ts-top-metrics) + div div[data-testid="stColumn"]:nth-child(1) div[data-testid="stMetricLabel"] p::before { content: "📍 "; }
    :is(.element-container, [data-testid="stElementContainer"]):has(.ts-top-metrics) + div div[data-testid="stColumn"]:nth-child(2) div[data-testid="stMetricLabel"] p::before { content: "🎯 "; }
    :is(.element-container, [data-testid="stElementContainer"]):has(.ts-top-metrics) + div div[data-testid="stColumn"]:nth-child(3) div[data-testid="stMetricLabel"] p::before { content: "🛡️ "; }
    /* =====================================================================
       6. INPUT SELECTOR — SEGMENTED CONTROL
       ===================================================================== */
    div[role="radiogroup"] {
        gap: 0.5rem;
        margin: 0.3rem 0 1rem 0;
    }
    div[role="radiogroup"] > label {
        background: var(--mint);
        border: 1.5px solid rgba(40, 89, 67, 0.25);
        border-radius: 999px;
        padding: 0.4rem 1.6rem;
        margin: 0;
        cursor: pointer;
        transition: all 180ms ease;
    }
    div[role="radiogroup"] > label:hover {
        background: #cdebd8;
        border-color: var(--forest);
        transform: translateY(-1px);
    }
    div[role="radiogroup"] > label > div:first-child { display: none; }
    div[role="radiogroup"] > label p {
        color: var(--forest) !important;
        font-weight: 750;
        font-size: 0.86rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, var(--forest), var(--teal));
        border-color: var(--forest);
        box-shadow: 0 8px 18px rgba(40, 89, 67, 0.32);
    }
    div[role="radiogroup"] > label:has(input:checked) p { color: #fff !important; }
    /* =====================================================================
       7. FILE UPLOADER — "AI INPUT ZONE"
       ===================================================================== */
    div[data-testid="stFileUploaderDropzone"],
    section[data-testid="stFileUploaderDropzone"] {
        background: linear-gradient(135deg, var(--soft-blue) 0%, var(--mint) 100%);
        border: 2px dashed var(--teal);
        border-radius: 20px;
        padding: 1.7rem 1.4rem;
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }
    div[data-testid="stFileUploaderDropzone"]:hover,
    section[data-testid="stFileUploaderDropzone"]:hover {
        transform: translateY(-2px);
        border-color: var(--forest);
        box-shadow: var(--shadow-lg);
    }
    div[data-testid="stFileUploaderDropzoneInstructions"] span {
        color: var(--forest) !important;
        font-weight: 700;
    }
    div[data-testid="stFileUploaderDropzoneInstructions"] small {
        color: var(--ink-2) !important;
    }
    div[data-testid="stFileUploaderDropzone"] svg { color: var(--teal) !important; }
    div[data-testid="stFileUploader"] label p {
        color: var(--forest) !important;
        font-weight: 750;
    }
    div[data-testid="stFileUploaderDropzone"] button {
        background: var(--teal);
        color: #fff;
        border: 1px solid var(--teal);
        border-radius: var(--radius-sm);
        font-weight: 700;
        transition: all 160ms ease;
    }
    div[data-testid="stFileUploaderDropzone"] button:hover {
        background: var(--teal-dk);
        border-color: var(--teal-dk);
        color: #fff;
        transform: translateY(-1px);
    }
    div[data-testid="stFileUploaderFile"] {
        background: var(--soft-blue);
        border-radius: var(--radius-sm);
    }
    /* =====================================================================
       8. IMAGE & VIDEO FRAMES (containers only — pixels untouched)
       ===================================================================== */
    div[data-testid="stImage"] img,
    div[data-testid="stImageContainer"] img {
        border-radius: 20px;
        border: 3px solid var(--teal);
        box-shadow: var(--shadow);
        background: var(--card);
        transition: box-shadow 180ms ease;
    }
    div[data-testid="stImage"] img:hover { box-shadow: var(--shadow-lg); }
    /* Original = sky/teal frame, AI Guidance = green frame */
    div[data-testid="stColumn"]:has(img):nth-child(1) img { border-color: var(--sky); }
    div[data-testid="stColumn"]:has(img):nth-child(2) img {
        border-color: var(--safe);
        box-shadow: 0 10px 30px rgba(78, 155, 104, 0.28);
    }
    section[data-testid="stSidebar"] img { border: 0; box-shadow: none; }
    /* analyzed video = hero */
    div[data-testid="stVideo"] {
        padding: 10px;
        background: linear-gradient(135deg, var(--forest), var(--teal));
        border: 2px solid var(--forest);
        border-radius: 24px;
        box-shadow: 0 0 0 5px rgba(47, 125, 117, 0.14), 0 18px 44px rgba(40, 89, 67, 0.34);
    }
    div[data-testid="stVideo"] video,
    video {
        border-radius: 16px;
        border: 0;
        box-shadow: none;
        background: #16241d;
        width: 100%;
    }
    /* =====================================================================
       9. ALERTS — SUCCESS / WARNING / ERROR / INFO
       ===================================================================== */
    div[data-testid="stAlert"] > div {
        border-radius: var(--radius);
        padding: 0.95rem 1.2rem;
        border: 1px solid var(--line);
        border-left-width: 6px;
        box-shadow: var(--shadow);
        transition: transform 160ms ease, box-shadow 160ms ease;
    }
    div[data-testid="stAlert"] > div:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    div[data-testid="stAlert"] > div > div[data-baseweb="notification"] {
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
    }
    div[data-testid="stAlert"] p { font-weight: 600; line-height: 1.55; }
    /* success / safe */
    div[data-testid="stAlert"] > div:has([data-testid="stAlertContentSuccess"]),
    div[data-testid="stAlert"] > div[kind="positive"] {
        background: var(--safe-bg) !important;
        border-color: #bfe0c9; border-left-color: var(--safe);
    }
    div[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) p,
    div[data-testid="stAlert"] > div[kind="positive"] p {
        color: #1f5d37 !important;
        font-size: 1.12rem;
        font-weight: 750;
    }
    /* warning / caution */
    div[data-testid="stAlert"] > div:has([data-testid="stAlertContentWarning"]),
    div[data-testid="stAlert"] > div[kind="warning"] {
        background: var(--caution-bg) !important;
        border-color: #f0dba5; border-left-color: var(--caution);
    }
    div[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) p,
    div[data-testid="stAlert"] > div[kind="warning"] p { color: #7a5612 !important; }
    /* error / danger */
    div[data-testid="stAlert"] > div:has([data-testid="stAlertContentError"]),
    div[data-testid="stAlert"] > div[kind="negative"] {
        background: var(--danger-bg) !important;
        border-color: #f0c4c4; border-left-color: var(--danger);
    }
    div[data-testid="stAlert"]:has([data-testid="stAlertContentError"]) p,
    div[data-testid="stAlert"] > div[kind="negative"] p {
        color: #8f2f2f !important;
        font-size: 1.08rem;
        font-weight: 750;
    }
    /* info */
    div[data-testid="stAlert"] > div:has([data-testid="stAlertContentInfo"]),
    div[data-testid="stAlert"] > div[kind="info"] {
        background: var(--soft-blue) !important;
        border-color: #b9dcee; border-left-color: var(--sky);
    }
    div[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) p,
    div[data-testid="stAlert"] > div[kind="info"] p { color: #1f5f78 !important; }
    /* =====================================================================
       10. BUTTONS
       ===================================================================== */
    /* primary action = deep forest green */
    .stButton > button {
        background: linear-gradient(135deg, var(--forest), #347a5b);
        color: #fff;
        border: 1px solid var(--forest);
        border-radius: var(--radius-sm);
        font-weight: 700;
        padding: 0.5rem 1.2rem;
        box-shadow: 0 6px 14px rgba(40, 89, 67, 0.28);
        transition: all 170ms ease;
    }
    .stButton > button p { color: #fff !important; }
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--forest-dk), var(--forest));
        color: #fff;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(40, 89, 67, 0.36);
    }
    /* download = golden / orange */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--gold), var(--orange));
        color: #3b2a07;
        border: 1px solid #d9953f;
        border-radius: var(--radius-sm);
        font-weight: 800;
        padding: 0.5rem 1.2rem;
        box-shadow: 0 6px 14px rgba(232, 155, 74, 0.38);
        transition: all 170ms ease;
    }
    .stDownloadButton > button p { color: #3b2a07 !important; }
    .stDownloadButton > button:hover {
        filter: brightness(1.04);
        color: #3b2a07;
        border-color: #c9812e;
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(232, 155, 74, 0.5);
    }
    .stButton > button:active, .stDownloadButton > button:active { transform: translateY(0); }
    /* =====================================================================
       11. PROGRESS — "AI TERRAIN ANALYSIS PROGRESS"
       ===================================================================== */
    div[data-testid="stProgress"]::before {
        content: "AI Terrain Analysis Progress";
        display: block;
        margin-bottom: 8px;
        color: var(--teal);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }
    div[data-testid="stProgress"] > div > div,
    div[data-testid="stProgress"] div[role="progressbar"] {
        background: var(--mint) !important;
        border-radius: 999px;
        height: 12px;
    }
    div[data-testid="stProgress"] > div > div > div,
    div[data-testid="stProgress"] div[role="progressbar"] > div {
        background: linear-gradient(90deg, var(--forest), var(--teal), var(--sky)) !important;
        border-radius: 999px;
    }
    /* =====================================================================
       12. TABLES / CHARTS / EXPANDERS
       ===================================================================== */
    div[data-testid="stDataFrame"] {
        background: var(--card);
        border: 1.5px solid rgba(47, 125, 117, 0.35);
        border-radius: var(--radius);
        overflow: hidden;
        box-shadow: var(--shadow);
        padding: 2px;
        transition: box-shadow 180ms ease;
    }
    div[data-testid="stDataFrame"]:hover { box-shadow: var(--shadow-lg); }
    div[data-testid="stArrowVegaLiteChart"],
    div[data-testid="stVegaLiteChart"] {
        background: linear-gradient(180deg, var(--soft-green), #fff 70%);
        border: 1.5px solid rgba(47, 125, 117, 0.35);
        border-top: 5px solid var(--teal);
        border-radius: var(--radius);
        padding: 16px 12px 8px 12px;
        box-shadow: var(--shadow);
    }
    details, div[data-testid="stExpander"] {
        background: var(--card);
        border: 1px solid var(--line) !important;
        border-left: 5px solid var(--orange) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow);
        overflow: hidden;
    }
    details summary, div[data-testid="stExpander"] summary {
        color: var(--forest);
        font-weight: 700;
        transition: background 150ms ease;
    }
    details summary:hover, div[data-testid="stExpander"] summary:hover { background: var(--soft-yellow); }
    pre, code {
        background: var(--soft-green) !important;
        color: var(--forest-dk) !important;
        border-radius: 10px;
    }
    /* =====================================================================
       13. VOICE GUIDANCE (iframe card)
       ===================================================================== */
    iframe {
        border: 1px solid rgba(47, 125, 117, 0.30);
        border-radius: var(--radius);
        background: linear-gradient(135deg, #d9eeea, var(--soft-blue));
    }
    /* =====================================================================
       14. FOCUS / MOTION / RESPONSIVE
       ===================================================================== */
    button:focus-visible, input:focus-visible, summary:focus-visible {
        outline: 3px solid rgba(244, 201, 93, 0.85) !important;
        outline-offset: 2px;
    }
    @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
    @media (max-width: 1100px) {
        .main .block-container, div[data-testid="stMainBlockContainer"] { padding-left: 1.5rem; padding-right: 1.5rem; }
        h1 { font-size: 2rem !important; padding-right: 6rem !important; }
        div[data-testid="stMetricValue"] div { font-size: 1.6rem !important; }
    }
    @media (max-width: 768px) {
        .main .block-container, div[data-testid="stMainBlockContainer"] { padding: 1.4rem 1rem 3rem 1rem; }
        h1 { font-size: 1.6rem !important; padding: 1.1rem 1.1rem 1.2rem 1.2rem !important; }
        div[data-testid="stVideo"] { padding: 6px; border-radius: 18px; }
        .stApp::after { height: 140px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)
DISCLAIMER = (
    "⚠️ Safety Notice: TrekStep AI provides AI-assisted prototype guidance only. "
    "It does not guarantee that a predicted foothold is safe and is not a replacement "
    "for proper trekking equipment, professional guidance, or human judgment."
)
# ----------------------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------------------
FONT = cv2.FONT_HERSHEY_SIMPLEX
MAX_SIDE = 640            # max side used for inference / heuristics
NO_FOOTHOLD_THRESHOLD = 35  # best candidate below this score -> "no safe-looking foothold"
CATS = ["unknown", "sky", "water", "path", "sand", "rock", "slope",
        "ground", "grass", "vegetation", "structure"]
CAT_IDX = {c: i for i, c in enumerate(CATS)}
# Prototype "stability" prior per terrain category (NOT a physical measurement)
STAB = {
    "unknown": 0.50, "sky": 0.0, "water": 0.0, "path": 1.00, "sand": 0.55,
    "rock": 0.62, "slope": 0.35, "ground": 0.90, "grass": 0.75,
    "vegetation": 0.0, "structure": 0.0,
}
CATEGORY_KEYWORDS = [
    ("sky", {"sky"}),
    ("water", {"water", "sea", "river", "lake", "waterfall", "falls", "fountain",
               "pond", "swimming pool", "pool", "puddle", "stream"}),
    ("path", {"path", "road", "route", "dirt track", "track", "sidewalk", "pavement",
              "runway", "stairs", "stairway", "staircase", "steps", "step", "stair",
              "floor", "flooring", "trail"}),
    ("sand", {"sand", "beach"}),
    ("rock", {"rock", "stone", "boulder", "cliff"}),
    ("slope", {"mountain", "mount", "hill", "slope"}),
    ("ground", {"earth", "ground", "land", "soil", "dirt"}),
    ("grass", {"grass", "field", "lawn", "flower", "meadow"}),
    ("vegetation", {"tree", "plant", "flora", "palm", "bush", "shrub", "vegetation"}),
    ("structure", {"wall", "building", "edifice", "house", "hovel", "hut", "fence",
                   "railing", "tower", "bridge", "pole", "column", "pillar",
                   "skyscraper", "bannister", "signboard", "sign", "tent", "boat",
                   "ship", "bus", "car", "auto", "truck", "van", "minibike",
                   "bicycle", "person", "individual", "animal", "streetlight",
                   "awning", "booth", "pier", "stage"}),
] 
RED = (40, 40, 255)      # BGR
YELLOW = (0, 215, 255)
GREEN = (80, 220, 60)
DARK = (25, 25, 25)
WHITE = (255, 255, 255)
# ----------------------------------------------------------------------------

# SMALL HELPERS        

# ----------------------------------------------------------------------------
def safe_float(v, default=None):
    """Convert to float safely; handles None / NaN / inf / garbage."""
    try:
        if v is None:
            return default
        f = float(v)
        if np.isnan(f) or np.isinf(f):
            return default
        return f
    except Exception:
        return default
def odd(n):
    n = int(max(3, round(n)))
    return n if n % 2 == 1 else n + 1
def ell(k):
    k = odd(k)
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
def categorize_label(label):
    """Map an ADE20K label string to a coarse terrain category (unknown-safe)."""
    try:
        text = str(label if label is not None else "").lower().replace("_", " ").strip()
        if not text:
            return "unknown"
        parts = {p.strip() for p in text.split(",") if p.strip()}
        words = set(text.replace(",", " ").split())
        toks = parts | words
        for cat, kws in CATEGORY_KEYWORDS:
            if toks & kws:
                return cat
    except Exception:
        pass
    return "unknown"
def score_band(s):
    if s >= 90:
        return "Very Safe-Looking Candidate"
    if s >= 70:
        return "Relatively Safe-Looking"
    if s >= 40:
        return "Caution"
    return "Dangerous / Poor Candidate"
def fill_contour(raw, h, w):
    m = np.zeros((h, w), np.uint8)
    cv2.drawContours(m, [raw], -1, 1, -1)
    return m
def ring_mean(channel, bm, k):
    dil = cv2.dilate(bm, ell(k))
    ring = (dil > 0) & (bm == 0)
    if not ring.any():
        return None
    return float(channel[ring].mean()) 
def extract_blobs(mask, min_area, max_blobs=6, open_k=3, close_k=5):
    """Connected regions of a boolean mask -> list of contour dicts (largest first)."""
    m = mask.astype(np.uint8)
    if m.max() == 0:
        return []
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, ell(open_k))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, ell(close_k))
    res = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = res[0] if len(res) == 2 else res[1]
    out = []
    for c in cnts:
        a = cv2.contourArea(c)
        if a < min_area or len(c) < 3:
            continue
        eps = 0.008 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, eps, True)
        if len(approx) < 3:
            continue
        out.append({"area": float(a), "raw": c, "approx": approx})
    out.sort(key=lambda b: b["area"], reverse=True)
    return out[:max_blobs]

# ----------------------------------------------------------------------------

# MODEL 

# ----------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_segmentation_model():
    from transformers import pipeline
    device = -1
    try:
        import torch
        if torch.cuda.is_available():
            device = 0
    except Exception:
        pass
    terrain_model = pipeline(
        "image-segmentation",
        model="nvidia/segformer-b0-finetuned-ade-512-512",
        device=device,
    )

    return terrain_model
def get_model_safe():
    try:
        with st.spinner("Loading SegFormer terrain model (first run may download weights)..."):
            return load_segmentation_model(), None
    except Exception as e:
        return None, str(e) 
def run_segmentation(model, bgr_small):
    """Run SegFormer. Returns (layers, ok, error). Layers = [(label, score, bool_mask)]."""
    h, w = bgr_small.shape[:2]
    if model is None:
        return [], False, "Segmentation model unavailable"
    try:
        pil = Image.fromarray(cv2.cvtColor(bgr_small, cv2.COLOR_BGR2RGB))
        outputs = model(pil)
    except Exception as e:
        return [], False, str(e)
    if not outputs:
        return [], False, "Empty segmentation result"
    layers = []
    for item in outputs:
        try:
            if not isinstance(item, dict):
                continue
            mask = item.get("mask")
            if mask is None:
                continue
            label = item.get("label")
            label = "unknown" if label is None else str(label)
            score = safe_float(item.get("score"), None)  # may legitimately be None
            m = np.array(mask)
            if m.ndim == 3:
                m = m[..., 0]
            if m.dtype == bool:
                mb = m
            else:
                mb = m > (0 if m.max() <= 1 else 127)
            if mb.shape != (h, w):
                mb = cv2.resize(mb.astype(np.uint8), (w, h),
                                interpolation=cv2.INTER_NEAREST).astype(bool)
            if not mb.any():
                continue
            layers.append((label, score, mb))
        except Exception:
            continue
    return layers, bool(layers), ("" if layers else "No usable masks")

# ----------------------------------------------------------------------------

# SCENE ANALYSIS (SegFormer + prototype heuristics + foothold selection)

# ----------------------------------------------------------------------------
def select_foothold(h, w, walkable, danger, caution, blocked, terr_map,
                    edges_bin, std, foot_scale, narrow):
    """Search candidate footholds in the lower-middle walking area."""
    r = max(5, int(round(0.045 * w * foot_scale)))
    safe_core = (walkable & (danger == 0)).astype(np.uint8)
    dist = cv2.distanceTransform(safe_core, cv2.DIST_L2, 5)
    dist = np.minimum(dist, 6.0 * r)
    pk = odd(2 * r + 1)
    wk = odd(6 * r + 1)
    f_danger = cv2.blur(danger.astype(np.float32), (pk, pk))
    f_caution = cv2.blur(caution.astype(np.float32), (pk, pk))
    f_walk = cv2.blur(walkable.astype(np.float32), (pk, pk))
    f_block = cv2.blur((blocked | (danger > 0)).astype(np.float32), (wk, wk))
    f_tex = cv2.blur(edges_bin, (pk, pk))
    f_std = cv2.blur(std.astype(np.float32), (pk, pk))
    f_terr = cv2.blur(terr_map, (pk, pk))
    eroded = (dist >= 0.7 * r).astype(np.uint8)
    _, labels, stats, _ = cv2.connectedComponentsWithStats(eroded, connectivity=8)
    areas = stats[:, cv2.CC_STAT_AREA]
    ys = np.linspace(0.56 * h, 0.93 * h, 11)
    xs = np.linspace(0.10 * w, 0.90 * w, 21)
    best = None
    n_eval = 0
    n_valid = 0
    for yv in ys:
        for xv in xs:
            yi, xi = int(yv), int(xv)
            n_eval += 1
            if not eroded[yi, xi]:
                continue
            if f_danger[yi, xi] > 0.02:
                continue
            if f_walk[yi, xi] < 0.90:
                continue
            terr = float(f_terr[yi, xi])
            if terr < 0.28:
                continue
            n_valid += 1
            clear_s = float(np.clip((min(dist[yi, xi], 3 * r) - 0.7 * r) / (2.3 * r), 0, 1))
            comp_area = float(areas[labels[yi, xi]]) if labels[yi, xi] > 0 else 0.0
            size_s = float(np.clip(comp_area / (0.08 * h * w), 0, 1))
            lateral = abs(xv - w / 2.0) / (0.5 * w)
            center_s = 1.0 - 0.85 * (lateral ** 1.3)
            forward_s = float(np.exp(-(((yv - 0.78 * h) / (0.20 * h)) ** 2)))
            pos_s = 0.65 * center_s + 0.35 * forward_s
            tex_s = 1.0 - float(np.clip(f_tex[yi, xi] / 0.25, 0, 1))
            std_s = 1.0 - float(np.clip(f_std[yi, xi] / 45.0, 0, 1))
            stab_s = 0.6 * tex_s + 0.4 * std_s
            terr_s = float(np.clip(terr, 0, 1))
            cau_frac = float(f_caution[yi, xi])
            cau_s = 1.0 - float(np.clip(cau_frac * 1.5, 0, 1))
            obs_s = 1.0 - float(np.clip(f_block[yi, xi] * 1.8, 0, 1))
            total = 100.0 * (0.20 * clear_s + 0.12 * size_s + 0.15 * pos_s +
                             0.18 * stab_s + 0.15 * terr_s + 0.12 * cau_s + 0.08 * obs_s)
            total *= (1.0 - 0.30 * cau_frac)
            if narrow:
                total *= 0.95
            total = float(np.clip(total, 0, 100))
            if best is None or total > best["score"]:
                rx = r * (0.9 + 0.5 * (yv / h)) * 1.25
                best = {
                    "x": float(xv), "y": float(yv), "rx": float(rx), "ry": float(rx * 0.55),
                    "score": total,
                    "factors": {
                        "Clearance from boundaries": clear_s,
                        "Continuous region size": size_s,
                        "Centered / forward position": pos_s,
                        "Visual stability (texture)": stab_s,
                        "Terrain type prior": terr_s,
                        "Low caution overlap": cau_s,
                        "Obstacle distance": obs_s,
                    }    },
                
    return best, n_eval, n_valid
def analyze_scene(bgr, seg_model, foot_scale=1.0):
    """Analyze a single BGR frame independently. Returns a result dict."""
    if bgr is None or bgr.size == 0:
        raise ValueError("Empty frame")
    if bgr.ndim == 2:
        bgr = cv2.cvtColor(bgr, cv2.COLOR_GRAY2BGR)
    H0, W0 = bgr.shape[:2]
    s = min(1.0, MAX_SIDE / float(max(H0, W0)))
    if s < 1.0:
        small = cv2.resize(bgr, (max(32, int(W0 * s)), max(32, int(H0 * s))),
                           interpolation=cv2.INTER_AREA)
    else:
        small = bgr
    h, w = small.shape[:2]
    area_px = float(h * w)
    # ---- 1) SegFormer scene segmentation -> category map ----
    layers, seg_ok, seg_err = run_segmentation(seg_model, small)
    cat = np.zeros((h, w), np.uint8)
    terrain_rows = []
    label_area = {}
    for label, score, mb in layers:
        c = categorize_label(label)
        cat[mb] = CAT_IDX[c]
        pct = float(mb.mean() * 100.0)
        label_area[label] = (c, pct, score)
    for label, (c, pct, score) in sorted(label_area.items(), key=lambda kv: -kv[1][1])[:10]:
        terrain_rows.append({
            "Segmentation label": label,
            "Terrain category": c,
            "Area (%)": round(pct, 1),
            "Model confidence": "n/a" if score is None else round(score, 3),
        })
    def isc(name):
        return cat == CAT_IDX[name]
    sky, water, veg, struct = isc("sky"), isc("water"), isc("vegetation"), isc("structure")
    rock, slope, sand = isc("rock"), isc("slope"), isc("sand")
    walkable = ~(sky | water | veg | struct)
    blocked = veg | struct | water
    # ---- 2) Low-level cues (prototype heuristics) ----
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    gray_f = gray.astype(np.float32)
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    Hh, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    gx = cv2.Sobel(blur, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(blur, cv2.CV_32F, 0, 1, ksize=3)
    grad = cv2.magnitude(gx, gy)
    edges = cv2.Canny(blur, 60, 140)
    edges_bin = (edges > 0).astype(np.float32)
    ek = odd(0.04 * w)
    edge_density = cv2.blur(edges_bin, (ek, ek))
    sk = odd(0.025 * w)
    mean = cv2.blur(gray_f, (sk, sk))
    sq = cv2.blur(gray_f * gray_f, (sk, sk))
    std = np.sqrt(np.maximum(sq - mean * mean, 0))
    hz = np.zeros((h, w), bool)          # hazard consideration zone (lower 60%)
    hz[int(0.40 * h):, :] = True
    lower = np.zeros((h, w), bool)
    lower[int(0.55 * h):, :] = True
    ref = walkable & lower
    if ref.sum() < 0.01 * area_px:
        ref = walkable
    if ref.sum() < 50:
        ref = np.ones((h, w), bool)
    med_v = max(1.0, float(np.median(V[ref])))
    med_g = max(1.0, float(np.median(gray[ref])))
    hazards = []
    def add(kind, level, blob):
        hazards.append({"kind": kind, "level": level, "raw": blob["raw"],
                        "approx": blob["approx"], "area": blob["area"]})
    spec = (V > 205) & (S < 55) & walkable & hz
    # ---- water (segmentation) ----
    for label, score, mb in layers:
        if categorize_label(label) == "water":
            ll = label.lower()
            kind = "flowing water" if any(k in ll for k in ("river", "waterfall", "falls", "stream")) \
                else "standing water"
            for b in extract_blobs(mb & hz, 0.004 * area_px, 3):
                add(kind, "danger", b)
    # ---- dangerous edge / drop-off (sky visible low in frame next to ground) ----
    sky_low = sky.copy()
    sky_low[:int(0.52 * h), :] = False
    if sky_low.sum() > 0.015 * area_px:
        band = cv2.dilate(sky_low.astype(np.uint8), ell(0.06 * w)) > 0
        edge_zone = band & walkable & hz
        for b in extract_blobs(edge_zone, 0.004 * area_px, 2, close_k=9):
            add("drop-off edge", "danger", b)
    # ---- pothole / hole / depression ----
    pothole_mask = np.zeros((h, w), np.uint8)
    K = odd(0.2 * w)
    bg = cv2.blur(gray_f, (K, K))
    dark = (gray_f < bg - 28) & (gray_f < 0.8 * med_g) & walkable & hz
    dark[:int(0.45 * h), :] = False
    for b in extract_blobs(dark, 0.0015 * area_px, 5, close_k=7):
        frac = b["area"] / area_px
        if frac > 0.10:
            continue
        bm = fill_contour(b["raw"], h, w)
        hull_a = cv2.contourArea(cv2.convexHull(b["raw"]))
        solidity = b["area"] / hull_a if hull_a > 0 else 0
        (_, _), (rw, rh), _ = cv2.minAreaRect(b["raw"])
        aspect = max(rw, rh) / (min(rw, rh) + 1e-6)
        rm = ring_mean(gray_f, bm, 0.03 * w)
        blob_g = float(gray_f[bm > 0].mean())
        contrast = (rm - blob_g) if rm is not None else 0
        bnd = cv2.morphologyEx(bm, cv2.MORPH_GRADIENT, ell(3)) > 0
        bstrength = float(grad[bnd].mean()) if bnd.any() else 0
        if solidity > 0.80 and aspect < 3.2 and contrast > 25 and bstrength > 15:
            pothole_mask |= bm
            if frac >= 0.004:
                add("pothole / hole", "danger", b)
            else:
                add("small depression", "caution", b)
    # ---- puddles / standing water (smooth, reflective, brighter than surroundings) ----
    puddle_mask = np.zeros((h, w), np.uint8)
    blue = (Hh >= 90) & (Hh <= 130) & (S >= 25)
    pud = (std < 9) & walkable & hz & (blue | spec) & (pothole_mask == 0)
    for b in extract_blobs(pud, 0.003 * area_px, 3, close_k=7):
        bm = fill_contour(b["raw"], h, w)
        mean_v = float(V[bm > 0].mean())
        ring_v = ring_mean(V, bm, 0.03 * w)
        blue_frac = float(blue[bm > 0].mean())
        if ring_v is None:
            continue
        if (mean_v - ring_v) > 20 or (blue_frac > 0.5 and abs(mean_v - ring_v) > 8):
            puddle_mask |= bm
            add("puddle / standing water", "danger", b)
    # ---- mud (brown + darker than surrounding ground + smooth) ----
    mud_mask = np.zeros((h, w), np.uint8)
    brown = (Hh >= 3) & (Hh <= 28) & (S >= 40) & (S <= 215)
    mud = brown & (V < 0.8 * med_v) & (std < 16) & walkable & hz & (~rock) & (pothole_mask == 0)
    for b in extract_blobs(mud, 0.003 * area_px, 4, close_k=7):
        bm = fill_contour(b["raw"], h, w)
        mud_mask |= bm
        frac = b["area"] / area_px
        near = cv2.dilate(bm, ell(0.03 * w)) > 0
        spec_near = float((spec & near).sum()) / max(1.0, b["area"])
        mean_v = float(V[bm > 0].mean())
        if spec_near > 0.02:
            add("greasy mud", "danger", b)
        elif mean_v < 0.55 * med_v and frac > 0.02:
            add("deep mud", "danger", b)
        else:
            add("mud", "caution", b)
    # ---- wet / slippery-looking smooth glare areas ----
    wet = ((cv2.dilate(spec.astype(np.uint8), ell(0.03 * w)) > 0) & (std < 14) &
           walkable & hz & (mud_mask == 0) & (puddle_mask == 0))
    for b in extract_blobs(wet, 0.004 * area_px, 3, close_k=7):
        add("wet / slippery surface", "caution", b)
    # ---- gravel / loose rocks / uneven texture ----
    rugged = (edge_density > 0.18) & (std > 16) & walkable & hz & (~rock) & (~slope)
    for b in extract_blobs(rugged, 0.012 * area_px, 3, close_k=9):
        add("gravel / loose rocks", "caution", b)
    # ---- rock / steep slope regions ----
    rock_like = (rock | slope) & hz & walkable
    for b in extract_blobs(rock_like, 0.015 * area_px, 4, close_k=9):
        bm = fill_contour(b["raw"], h, w)
        frac = b["area"] / area_px
        rug = float(edge_density[bm > 0].mean())
        is_slope = int((slope & (bm > 0)).sum()) > int((rock & (bm > 0)).sum())
        cy = float(np.mean(b["raw"][:, 0, 1]))
        if rug > 0.26 and frac > 0.03 and cy > 0.5 * h:
            add("steep rocky area" if is_slope else "unstable rocky ground", "danger", b)
        else:
            add("steep slope" if is_slope else "rocky / uneven ground", "caution", b)
    # ---- sand ----
    for b in extract_blobs(sand & hz, 0.02 * area_px, 2, close_k=9):
        add("sand / loose surface", "caution", b)
    # ---- obstacles intruding into the lower walking area ----
    for b in extract_blobs((veg | struct) & hz, 0.01 * area_px, 3, close_k=7):
        ymax = float(np.max(b["raw"][:, 0, 1]))
        if ymax > 0.65 * h:
            add("obstacle", "caution", b)
    # ---- exposed roots (thin dark brown elongated shapes) ----
    root = (V < 120) & (Hh >= 5) & (Hh <= 25) & (S > 40) & walkable & hz
    for b in extract_blobs(root, 0.0005 * area_px, 8, open_k=3, close_k=3):
        if b["area"] > 0.012 * area_px:
            continue
        (_, _), (rw, rh), _ = cv2.minAreaRect(b["raw"])
        if max(rw, rh) / (min(rw, rh) + 1e-6) >= 3.5:
            add("exposed root", "caution", b)
            if sum(1 for hh in hazards if hh["kind"] == "exposed root") >= 3:
                break
    # ---- compose danger / caution masks (danger first, caution filtered) ----
    danger_mask = np.zeros((h, w), np.uint8)
    for hh in hazards:
        if hh["level"] == "danger":
            cv2.drawContours(danger_mask, [hh["raw"]], -1, 1, -1)
    kept = [hh for hh in hazards if hh["level"] == "danger"]
    caution_mask = np.zeros((h, w), np.uint8)
    for hh in hazards:
        if hh["level"] != "caution":
            continue
        fm = fill_contour(hh["raw"], h, w)
        tot = float(fm.sum())
        if tot <= 0:
            continue
        if float((fm & danger_mask).sum()) / tot > 0.5:
            continue
        caution_mask |= fm
        kept.append(hh)
    danger_sel = cv2.dilate(danger_mask, ell(0.012 * w))  # margin used for selection
    # ---- narrow trail heuristic ----
    rows = slice(int(0.70 * h), max(int(0.92 * h), int(0.70 * h) + 1))
    safe_core_full = (walkable & (danger_sel == 0))
    free_frac = float(safe_core_full[rows].mean())
    block_frac = float((blocked | (danger_sel > 0))[rows].mean())
    narrow = bool(free_frac < 0.22 and block_frac > 0.35)
    # ---- 3) foothold selection ----
    stab_arr = np.array([STAB[c] for c in CATS], np.float32)
    terr_map = stab_arr[cat]
    best, n_eval, n_valid = select_foothold(
        h, w, walkable, danger_sel, caution_mask, blocked, terr_map,
        edges_bin, std, foot_scale, narrow)
    foothold = None
    score = 0
    factors = {}
    if best is not None:
        score = int(round(best["score"]))
        factors = {k: round(float(v), 3) for k, v in best["factors"].items()}
        if best["score"] >= NO_FOOTHOLD_THRESHOLD:
            foothold = {k: best[k] for k in ("x", "y", "rx", "ry")}
            foothold["score"] = score
    if foothold is not None:
        dx = (foothold["x"] - w / 2.0) / (w / 2.0)
        if dx < -0.5:
            dkey, dtext = "left", "Move left"
        elif dx < -0.12:
            dkey, dtext = "left", "Move slightly left"
        elif dx > 0.5:
            dkey, dtext = "right", "Move right"
        elif dx > 0.12:
            dkey, dtext = "right", "Move slightly right"
        else:
            dkey, dtext = "center", "Move forward"
    else:
        dkey, dtext = "none", "No safe-looking foothold"
    # ---- output hazards (compact, in analysis coordinates) ----
    def pack(hh):
        c = hh["approx"].reshape(-1, 2).astype(np.float32)
        return {"kind": hh["kind"], "level": hh["level"],
                "area_frac": float(hh["area"] / area_px),
                "contour": c, "cy": float(c[:, 1].mean())}
    dangers = sorted([hh for hh in kept if hh["level"] == "danger"],
                     key=lambda x: -x["area"])[:6]
    cautions = sorted([hh for hh in kept if hh["level"] == "caution"],
                      key=lambda x: -x["area"])[:6]
    hazards_out = [pack(x) for x in dangers + cautions]
    res = {
        "aw": w, "ah": h, "seg_ok": seg_ok, "seg_error": seg_err,
        "hazards": hazards_out, "foothold": foothold, "score": score,
        "band": score_band(score), "direction": dkey, "direction_text": dtext,
        "terrain": terrain_rows, "narrow": narrow, "factors": factors,
        "candidates_evaluated": n_eval, "candidates_valid": n_valid,
    }
    res["voice"] = make_voice(res)
    return res
def make_voice(res):
    if res.get("foothold") is None:
        return "No safe-looking foothold detected."
    mapping = {
        "Move slightly left": "Move slightly to the left.",
        "Move left": "Move to the left.",
        "Move slightly right": "Move slightly to the right.",
        "Move right": "Move to the right.",
        "Move forward": "Move forward.",
    }
    parts = [mapping.get(res["direction_text"], "Move forward."),
             "Place your next step on the green area."]
    ah = res.get("ah", 1)
    if any(hz["level"] == "danger" and hz["cy"] > 0.5 * ah for hz in res["hazards"]):
        parts.append("Avoid the red area.")
    return " ".join(parts)
# ----------------------------------------------------------------------------
# OVERLAY DRAWING (clean, minimal AR-style)
# ----------------------------------------------------------------------------
def put_label(img, text, x, y, bg, fg=WHITE, scale=0.55, thick=1):
    """Small label with translucent background, centered at (x, y). '•' is drawn as a dot."""
    H, W = img.shape[:2]
    parts = [p.strip() for p in text.split("•")]
    sizes = [cv2.getTextSize(p, FONT, scale, thick)[0] for p in parts]
    gap = int(16 * scale / 0.55)
    tw = sum(s[0] for s in sizes) + gap * (len(parts) - 1)
    th = max(s[1] for s in sizes)
    pad = int(7 * scale / 0.55)
    x1 = int(x - tw / 2) - pad
    x2 = x1 + tw + 2 * pad
    y1 = int(y - th / 2) - pad
    y2 = y1 + th + 2 * pad
    shift_x = max(0, 2 - x1) - max(0, x2 - (W - 2))
    shift_y = max(0, 2 - y1) - max(0, y2 - (H - 2))
    x1 += shift_x
    x2 += shift_x
    y1 += shift_y
    y2 += shift_y
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(W, x2), min(H, y2)
    if x2 <= x1 or y2 <= y1:
        return
    roi = img[y1:y2, x1:x2]
    roi[:] = (roi.astype(np.float32) * 0.40 + np.array(bg, np.float32) * 0.60).astype(np.uint8)
    cx = x1 + pad
    base_y = y1 + pad + th
    for i, p in enumerate(parts):
        cv2.putText(img, p, (cx, base_y), FONT, scale, fg, thick, cv2.LINE_AA)
        cx += sizes[i][0]
        if i < len(parts) - 1:
            cv2.circle(img, (cx + gap // 2, base_y - th // 2), max(2, int(3 * scale / 0.55)),
                       fg, -1, cv2.LINE_AA)
            cx += gap
def new_ease():
    return {"pos": None, "rx": None, "ry": None}
def draw_guidance(frame, res, ease):
    """Draw the AI guidance directly on a frame (in place)."""
    H, W = frame.shape[:2]
    sx, sy = W / float(res["aw"]), H / float(res["ah"])
    base = max(0.6, min(W, H) / 720.0)
    th = max(1, int(round(2 * base)))
    fscale = 0.55 * base
    def scaled(c):
        return (c * np.array([sx, sy], np.float32)).astype(np.int32).reshape(-1, 1, 2)
    dangers = [h for h in res["hazards"] if h["level"] == "danger"][:3]
    cautions = [h for h in res["hazards"] if h["level"] == "caution"][:3]
    # thin outlines only
    for hz in cautions:
        cv2.polylines(frame, [scaled(hz["contour"])], True, YELLOW, th, cv2.LINE_AA)
    for hz in dangers:
        cv2.polylines(frame, [scaled(hz["contour"])], True, RED, th, cv2.LINE_AA)
    for hz in dangers[:2]:
        c = hz["contour"]
        i = int(np.argmin(c[:, 1]))
        lx, ly = c[i, 0] * sx, c[i, 1] * sy - 14 * base
        put_label(frame, "DANGER: " + hz["kind"], lx, ly, RED, scale=fscale * 0.8)
    fh = res.get("foothold")
    if fh is not None:
        tgt = np.array([fh["x"] * sx, fh["y"] * sy], np.float32)
        trx, try_ = fh["rx"] * sx, fh["ry"] * sy
        if ease["pos"] is None:
            ease["pos"], ease["rx"], ease["ry"] = tgt, trx, try_
        else:
            a = 0.45
            ease["pos"] = ease["pos"] + a * (tgt - ease["pos"])
            ease["rx"] += a * (trx - ease["rx"])
            ease["ry"] += a * (try_ - ease["ry"])
        px, py = float(ease["pos"][0]), float(ease["pos"][1])
        rx, ry = max(6, int(ease["rx"])), max(4, int(ease["ry"]))
        # translucent foothold region (ROI blend only)
        x1, y1 = max(0, int(px - rx - 2)), max(0, int(py - ry - 2))
        x2, y2 = min(W, int(px + rx + 3)), min(H, int(py + ry + 3))
        if x2 > x1 and y2 > y1:
            m = np.zeros((y2 - y1, x2 - x1), np.uint8)
            cv2.ellipse(m, (int(px) - x1, int(py) - y1), (rx, ry), 0, 0, 360, 255, -1)
            roi = frame[y1:y2, x1:x2]
            mb = m > 0
            roi[mb] = (roi[mb].astype(np.float32) * 0.62 +
                       np.array(GREEN, np.float32) * 0.38).astype(np.uint8)
        cv2.ellipse(frame, (int(px), int(py)), (rx, ry), 0, 0, 360, GREEN, th + 1, cv2.LINE_AA)
        # single clean arrow from trekker position to the foothold
        start = np.array([W * 0.5, H * 0.93], np.float32)
        v = np.array([px, py], np.float32) - start
        L = float(np.linalg.norm(v))
        short = max(ry, rx * 0.5) * 1.1
        if L - short > 25 * base:
            end = np.array([px, py], np.float32) - v / L * short
            tip = float(min(0.35, 26 * base / max(1.0, L - short)))
            p0, p1 = (int(start[0]), int(start[1])), (int(end[0]), int(end[1]))
            cv2.arrowedLine(frame, p0, p1, DARK, th + 3, cv2.LINE_AA, tipLength=tip)
            cv2.arrowedLine(frame, p0, p1, GREEN, th + 1, cv2.LINE_AA, tipLength=tip)
        put_label(frame, "STEP HERE • %d/100" % fh["score"], px, py - ry - 20 * base,
                  (40, 130, 30), scale=fscale)
        put_label(frame, res["direction_text"], W * 0.5, H - 22 * base, DARK, scale=fscale)
    else:
        ease["pos"] = None
        put_label(frame, "NO SAFE-LOOKING FOOTHOLD", W * 0.5 + 12 * base, 0.08 * H,
                  (0, 0, 200), scale=fscale * 1.05)
        # small red warning triangle
        cx, cy = int(W * 0.5 - 150 * base), int(0.08 * H)
        t = int(11 * base)
        pts = np.array([[cx, cy - t], [cx - t, cy + t], [cx + t, cy + t]], np.int32)
        cv2.fillPoly(frame, [pts], RED, cv2.LINE_AA)
        cv2.putText(frame, "!", (cx - int(3 * base), cy + int(t * 0.8)), FONT,
                    0.45 * base, WHITE, 1, cv2.LINE_AA)
        put_label(frame, "Stop and reassess", W * 0.5, H - 22 * base, DARK, scale=fscale)
    return frame
# ----------------------------------------------------------------------------
# VIDEO PIPELINE
# ----------------------------------------------------------------------------
def find_ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None
def open_writer(tmp_dir, fps, size):
    for name in ("avc1", "H264", "mp4v"):
        p = os.path.join(tmp_dir, "raw_%s.mp4" % name)
        try:
            wr = cv2.VideoWriter(p, cv2.VideoWriter_fourcc(*name), fps, size)
            if wr.isOpened():
                return wr, name, p
            wr.release()
        except Exception:
            pass
    p = os.path.join(tmp_dir, "raw_mjpg.avi")
    wr = cv2.VideoWriter(p, cv2.VideoWriter_fourcc(*"MJPG"), fps, size)
    if wr.isOpened():
        return wr, "MJPG", p
    raise RuntimeError("No usable video codec found in this OpenCV build.")
def finalize_video(raw_path, codec, src_path, tmp_dir):
    """Try to produce a browser-friendly H.264 MP4 (keeping original audio if present)."""
    is_h264 = codec in ("avc1", "H264")
    final_path = os.path.join(tmp_dir, "trekstep_analyzed.mp4")
    ffmpeg = find_ffmpeg()
    if ffmpeg:
        vcodec = ["-c:v", "copy"] if is_h264 else \
            ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p"]
        attempts = [
            [ffmpeg, "-y", "-loglevel", "error", "-i", raw_path, "-i", src_path,
             "-map", "0:v:0", "-map", "1:a:0?", *vcodec, "-c:a", "aac", "-shortest",
             "-movflags", "+faststart", final_path],
            [ffmpeg, "-y", "-loglevel", "error", "-i", raw_path, "-map", "0:v:0",
             *vcodec, "-an", "-movflags", "+faststart", final_path],
        ]
        for cmd in attempts:
            try:
                r = subprocess.run(cmd, capture_output=True, timeout=1200)
                if r.returncode == 0 and os.path.exists(final_path) and \
                        os.path.getsize(final_path) > 1024:
                    return final_path, "video/mp4", True
            except Exception:
                pass
            try:
                if os.path.exists(final_path):
                    os.remove(final_path)
            except Exception:
                pass
    if raw_path.endswith(".mp4"):
        return raw_path, "video/mp4", is_h264
    return raw_path, "video/x-msvideo", False
def build_key_moments(timeline):
    moments, last_text, last_t = [], None, -99.0
    for e in timeline:
        if e["voice"] != last_text and e["t"] - last_t >= 1.5:
            moments.append({"t": round(e["t"], 1), "text": e["voice"]})
            last_text, last_t = e["voice"], e["t"]
        if len(moments) >= 40:
            break
    return moments
def process_video(src_path, seg_model, rate, max_seconds, foot_scale, progress, status):
    cap = cv2.VideoCapture(src_path)
    if not cap.isOpened():
        raise ValueError("Could not open the video. It may be corrupt or use an unsupported codec.")
    fps = safe_float(cap.get(cv2.CAP_PROP_FPS), 0.0) or 0.0
    if fps < 1 or fps > 240:
        fps = 30.0
    total = int(safe_float(cap.get(cv2.CAP_PROP_FRAME_COUNT), 0) or 0)
    ok, frame = cap.read()
    if not ok or frame is None:
        cap.release()
        raise ValueError("No readable frames were found in the video.")
    H, W = frame.shape[:2]
    pad_r, pad_b = W % 2, H % 2
    size_out = (W + pad_r, H + pad_b)
    tmp_dir = tempfile.mkdtemp(prefix="trekstep_out_")
    try:
        writer, codec, raw_path = open_writer(tmp_dir, fps, size_out)
    except Exception:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        cap.release()
        raise
    stride = max(1, int(round(fps / float(max(1, rate)))))
    max_frames = int(fps * max_seconds)
    total_eff = min(total, max_frames) if total > 0 else 0
    timeline = []
    last_res = None
    ease = new_ease()
    idx = 0
    truncated = False
    analysis_errors = 0
    last_error = ""
    try:
        while True:
            if idx >= max_frames:
                truncated = True
                break
            if frame.shape[:2] != (H, W):
                frame = cv2.resize(frame, (W, H))
            if idx % stride == 0:
                try:
                    last_res = analyze_scene(frame, seg_model, foot_scale)
                    timeline.append({
                        "t": idx / fps, "frame": idx, "score": last_res["score"],
                        "band": last_res["band"], "direction": last_res["direction"],
                        "direction_text": last_res["direction_text"],
                        "has_foothold": last_res["foothold"] is not None,
                        "danger": sorted({h["kind"] for h in last_res["hazards"]
                                          if h["level"] == "danger"}),
                        "caution": sorted({h["kind"] for h in last_res["hazards"]
                                           if h["level"] == "caution"}),
                        "voice": last_res["voice"],
                        "narrow": last_res["narrow"],
                    })
                except Exception as e:
                    analysis_errors += 1
                    last_error = str(e)
                if total_eff:
                    progress.progress(min(1.0, (idx + 1) / total_eff))
                    status.text("Analyzing frame %d / %d" % (idx + 1, total_eff))
                else:
                    status.text("Analyzing frame %d" % (idx + 1))
            if last_res is not None:
                try:
                    draw_guidance(frame, last_res, ease)
                except Exception:
                    pass
            out = frame
            if pad_r or pad_b:
                out = cv2.copyMakeBorder(frame, 0, pad_b, 0, pad_r, cv2.BORDER_REPLICATE)
            writer.write(np.ascontiguousarray(out))
            idx += 1
            ok, frame = cap.read()
            misses = 0
            while (not ok or frame is None) and misses < 3 and (total <= 0 or idx < total):
                ok, frame = cap.read()
                misses += 1
            if not ok or frame is None:
                break
    finally:
        cap.release()
        writer.release()
    if idx == 0 or not timeline:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise RuntimeError("Video analysis failed: no frame could be analyzed. %s" % last_error)
    if not os.path.exists(raw_path) or os.path.getsize(raw_path) < 1024:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise RuntimeError("The output video could not be written (codec problem).")
    progress.progress(1.0)
    final_path, mime, playable = finalize_video(raw_path, codec, src_path, tmp_dir)
    with open(final_path, "rb") as f:
        data = f.read()
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return {
        "video_bytes": data, "mime": mime, "playable": playable, "codec": codec,
        "timeline": timeline, "fps": fps, "frames": idx, "stride": stride,
        "truncated": truncated, "analysis_errors": analysis_errors,
        "last_error": last_error, "width": W, "height": H,
        "ffmpeg": find_ffmpeg() is not None,
        "key_moments": build_key_moments(timeline),
    }
# ----------------------------------------------------------------------------
# VOICE (browser text-to-speech; not real-time microphone communication)
# ----------------------------------------------------------------------------
def voice_widget(cues, timed=True, height=110):
    safe = json.dumps(cues).replace("</", "<\\/")
    html = """
<div style="font-family:Inter,'Segoe UI',-apple-system,BlinkMacSystemFont,Arial,sans-serif;font-size:14px;">
  <button id="seq" style="padding:7px 14px;margin:2px;cursor:pointer;background:#285943;color:#fff;border:1px solid #285943;border-radius:10px;font-weight:600;font-size:13px;">🔊 Speak guidance</button>
  __TIMED__
  <button id="stop" style="padding:7px 14px;margin:2px;cursor:pointer;background:#D95D5D;color:#fff;border:1px solid #D95D5D;border-radius:10px;font-weight:600;font-size:13px;">⏹ Stop</button>
  <div id="msg" style="margin-top:8px;color:#66756C;font-size:13px;"></div>
</div>
<script>
const cues = __CUES__;
const synth = window.speechSynthesis;
let timers = [];
const msg = document.getElementById('msg');
function say(t){ const u = new SpeechSynthesisUtterance(t); u.rate = 0.95; synth.speak(u); }
function stopAll(){ timers.forEach(clearTimeout); timers = []; if (synth) synth.cancel(); }
if (!synth) { msg.textContent = 'Speech synthesis is not supported in this browser.'; }
document.getElementById('seq').onclick = function(){
  if (!synth) return; stopAll(); cues.forEach(c => say(c.text)); msg.textContent = 'Speaking key-moment guidance...';
};
const tb = document.getElementById('timed');
if (tb) tb.onclick = function(){
  if (!synth) return; stopAll();
  cues.forEach(c => { timers.push(setTimeout(() => say(c.text), c.t * 1000)); });
  msg.textContent = 'Timed cues started. Press Play on the video at the same moment.';
};
document.getElementById('stop').onclick = function(){ stopAll(); msg.textContent = 'Stopped.'; };
</script>
"""
    timed_btn = ('<button id="timed" style="padding:7px 14px;margin:2px;cursor:pointer;'
                 'background:#2F7D75;color:#fff;border:1px solid #2F7D75;border-radius:10px;'
                 'font-weight:600;font-size:13px;">'
                 '⏱ Start timed cues (press together with video Play)</button>') if timed else ""
    html = html.replace("__CUES__", safe).replace("__TIMED__", timed_btn)
    components.html(html, height=height)
# ----------------------------------------------------------------------------
# UI SECTIONS
# ----------------------------------------------------------------------------
def render_hazard_table(res):
    rows = []
    for hz in res["hazards"]:
        rows.append({"Heuristic finding": hz["kind"],
                     "Level": "DANGER (red)" if hz["level"] == "danger" else "Caution (yellow)",
                     "Frame area (%)": round(hz["area_frac"] * 100, 1)})
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.caption("No hazard heuristics triggered in this frame.")
def image_mode(seg_model, foot_scale, voice_on, score_ph):
    up = st.file_uploader("Upload a trekking image", type=["jpg", "jpeg", "png", "bmp", "webp"],
                          key="img_up")
    if up is None:
        st.info("Upload a trekking image to get terrain-aware footstep guidance.")
        return
    try:
        pil = Image.open(up)
        pil = ImageOps.exif_transpose(pil).convert("RGB")
    except Exception as e:
        st.error("Invalid or unsupported image: %s" % e)
        return
    if max(pil.size) > 1600:
        pil.thumbnail((1600, 1600))
    bgr = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    with st.spinner("Analyzing terrain..."):
        try:
            res = analyze_scene(bgr, seg_model, foot_scale)
        except Exception as e:
            st.error("Analysis failed: %s" % e)
            return
    out = bgr.copy()
    draw_guidance(out, res, new_ease())
    score_ph.metric("Safety Score", "%d/100" % res["score"] if res["foothold"] else "No safe step")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Original Image")
        st.image(np.array(pil), use_container_width=True)
    with c2:
        st.subheader("AI Guidance Image")
        st.image(cv2.cvtColor(out, cv2.COLOR_BGR2RGB), use_container_width=True)
    t1, t2 = st.columns(2)
    with t1:
        st.subheader("Terrain Information")
        if not res["seg_ok"]:
            st.warning("Segmentation returned no usable regions (%s). Using heuristics only."
                       % (res["seg_error"] or "unknown reason"))
        if res["terrain"]:
            st.caption("SegFormer scene labels (real model output):")
            st.dataframe(res["terrain"], use_container_width=True, hide_index=True)
        st.caption("Prototype computer-vision heuristics (texture / colour / shape / position):")
        render_hazard_table(res)
        if res["narrow"]:
            st.warning("Narrow trail section detected (heuristic).")
    with t2:
        st.subheader("Recommended Next Step")
        if res["foothold"]:
            st.success("%s — STEP HERE • %d/100 (%s)" % (res["direction_text"], res["score"],
                                                         res["band"]))
            if res["factors"]:
                st.caption("Prototype score factors (0–1):")
                st.dataframe([{"Factor": k, "Value": v} for k, v in res["factors"].items()],
                             use_container_width=True, hide_index=True)
        else:
            st.error("NO SAFE-LOOKING FOOTHOLD (best candidate score: %d/100)" % res["score"])
        st.caption("The score is a prototype heuristic and never a guarantee of physical safety.")
        if voice_on:
            st.markdown("**Voice guidance:** " + res["voice"])
            voice_widget([{"t": 0, "text": res["voice"]}], timed=False, height=80)
def video_mode(seg_model, foot_scale, voice_on, rate, max_seconds, score_ph):
    up = st.file_uploader("Upload Video", type=["mp4", "mov", "avi", "mkv", "webm", "m4v"],
                          key="vid_up")
    if up is None:
        st.info("Upload a trekking video. TrekStep AI will analyze it over time and draw the "
                "guidance directly on the video.")
        return
    file_sig = (up.name, up.size)
    settings = (int(rate), int(max_seconds), round(float(foot_scale), 3))
    stored = st.session_state.get("video_result")
    need = stored is None or stored.get("file_sig") != file_sig
    if not need and stored.get("settings") != settings:
        st.info("Analysis settings changed since the last run.")
        if st.button("🔄 Re-analyze with new settings"):
            need = True
    if need:
        suffix = os.path.splitext(up.name)[1] or ".mp4"
        tmp_in = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tf:
                tf.write(up.getbuffer())
                tmp_in = tf.name
        except Exception as e:
            st.error("Could not store the uploaded video temporarily: %s" % e)
            return
        st.subheader("Processing Progress")
        progress = st.progress(0.0)
        status = st.empty()
        try:
            result = process_video(tmp_in, seg_model, rate, max_seconds, foot_scale,
                                   progress, status)
            result["file_sig"] = file_sig
            result["settings"] = settings
            st.session_state["video_result"] = result
            status.empty()
            st.success("✅ Trek analysis completed")
        except Exception as e:
            st.error("Video processing failed: %s" % e)
            with st.expander("Technical details"):
                st.code(traceback.format_exc())
            return
        finally:
            try:
                if tmp_in and os.path.exists(tmp_in):
                    os.remove(tmp_in)
            except Exception:
                pass
        stored = st.session_state["video_result"]
    r = stored
    timeline = r["timeline"]
    if r["truncated"]:
        st.warning("Only the first %d seconds were processed (see sidebar limit)." % max_seconds)
    if r["analysis_errors"]:
        st.warning("%d sampled frame(s) could not be analyzed; the previous recommendation was "
                   "reused for them. Last error: %s" % (r["analysis_errors"], r["last_error"]))
    st.subheader("Analyzed Video")
    st.video(r["video_bytes"], format=r["mime"])
    if not r["playable"]:
        st.warning(
            "The video was encoded with a codec that some browsers cannot play "
            "(codec: %s%s). If playback is blank, download the file below, or install "
            "`imageio-ffmpeg` / FFmpeg so the app can re-encode to H.264 automatically."
            % (r["codec"], "" if r["ffmpeg"] else ", FFmpeg not found"))
    fname = "trekstep_analyzed.mp4" if r["mime"] == "video/mp4" else "trekstep_analyzed.avi"
    st.download_button("⬇️ Download analyzed video", data=r["video_bytes"], file_name=fname,
                       mime=r["mime"])
    st.caption("%d frames • %dx%d • %.1f FPS • AI re-analyzed every %d frame(s) "
               "(%d analyses); the latest recommendation is carried between analyses."
               % (r["frames"], r["width"], r["height"], r["fps"], r["stride"], len(timeline)))
    st.subheader("Current Recommendation")
    scores = [e["score"] for e in timeline]
    if len(timeline) > 1:
        i = st.slider("Inspect analysis checkpoint", 0, len(timeline) - 1, 0,
                      help="Move through the analyzed moments of the video.")
    else:
        i = 0
    e = timeline[i]
    score_ph.metric("Safety Score", "%d/100" % e["score"] if e["has_foothold"] else "No safe step")
    st.markdown("**Time %.1f s (frame %d):** %s" % (e["t"], e["frame"], e["direction_text"]))
    if e["has_foothold"]:
        st.success("STEP HERE • %d/100 — %s" % (e["score"], e["band"]))
    else:
        st.error("NO SAFE-LOOKING FOOTHOLD at this moment")
    if e["danger"]:
        st.markdown("🔴 **Danger:** " + ", ".join(e["danger"]))
    if e["caution"]:
        st.markdown("🟡 **Caution:** " + ", ".join(e["caution"]))
    if e["narrow"]:
        st.markdown("↔️ Narrow trail section (heuristic)")
    m1, m2, m3 = st.columns(3)
    m1.metric("Average prototype score", "%.0f/100" % float(np.mean(scores)))
    m2.metric("Lowest score", "%d/100" % min(scores))
    no_safe = sum(1 for x in timeline if not x["has_foothold"])
    m3.metric("Moments without safe foothold", "%d / %d" % (no_safe, len(timeline))) 
    st.subheader("Safety Score")
    if len(scores) > 1:
        st.line_chart({"Prototype safety score": scores})
    st.dataframe(
        [{"Time (s)": round(x["t"], 1), "Direction": x["direction_text"], "Score": x["score"],
          "Band": x["band"], "Danger": ", ".join(x["danger"]), "Caution": ", ".join(x["caution"])}
         for x in timeline],
        use_container_width=True, hide_index=True) 
    if voice_on:
        st.subheader("Voice Guidance (key moments)")
        st.caption("Browser text-to-speech generated from analyzed key moments of the "
                   "prerecorded video. It is not real-time microphone communication and is not "
                   "automatically synchronized with the player.")
        moments = r["key_moments"]
        st.dataframe([{"Time (s)": m["t"], "Voice cue": m["text"]} for m in moments],
                     use_container_width=True, hide_index=True)
        voice_widget(moments, timed=True, height=110) 
# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
def main():
    st.title("🥾 TrekStep AI")
    st.markdown("##### AI-Powered Terrain-Aware Footstep Guidance")
    st.sidebar.header("⚙️ Trekking Controls")
    destination = st.sidebar.text_input("Destination", value="", placeholder="e.g. Base camp")
    voice_on = st.sidebar.checkbox("Voice Guidance", value=False)
    height_cm = st.sidebar.number_input("Your height (cm) – optional", min_value=0, max_value=250,
                                        value=0, step=1)
    leg_cm = st.sidebar.number_input("Leg length (cm) – optional", min_value=0, max_value=150,
                                     value=0, step=1)
    st.sidebar.caption("Height / leg length only scale the size of the stepping footprint "
                       "used when searching for footholds.")
    st.sidebar.subheader("Video analysis")
    rate = st.sidebar.slider("AI analyses per second of video", 1, 10, 3)
    max_seconds = st.sidebar.slider("Max video length to process (seconds)", 5, 300, 120)
    parts = []
    if height_cm > 0:
        parts.append(float(np.clip(height_cm / 170.0, 0.85, 1.2)))
    if leg_cm > 0:
        parts.append(float(np.clip(leg_cm / 90.0, 0.85, 1.2)))
    foot_scale = float(np.mean(parts)) if parts else 1.0
    # styling hook only (hidden by CSS): lets the theme emphasise the Safety Score card
    st.markdown('<span class="ts-top-metrics"></span>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Current Location", "Not Available")
    m2.metric("Destination", destination.strip() or "Not set")
    score_ph = m3.empty()
    score_ph.metric("Safety Score", "—")
    st.warning(DISCLAIMER)
    mode = st.radio("Input", ["Image", "Video"], horizontal=True)
    seg_model, load_err = get_model_safe()
    if seg_model is None:
        st.error("The SegFormer model could not be loaded (%s). The app will continue with "
                 "computer-vision heuristics only, which is less reliable." % load_err)
    try:
        if mode == "Image":
            image_mode(seg_model, foot_scale, voice_on, score_ph)
        else:
            video_mode(seg_model, foot_scale, voice_on, rate, max_seconds, score_ph)
    except Exception as e:
        st.error("Unexpected error: %s" % e)
        with st.expander("Technical details"):
            st.code(traceback.format_exc())
    st.caption("Prototype notes: SegFormer provides scene/terrain segmentation only. Mud, wet "
               "surfaces, puddles, potholes, edges, loose rocks and 'stability' are estimated "
               "with prototype computer-vision heuristics (colour, texture, shape, region size, "
               "position and surrounding terrain).")
main()