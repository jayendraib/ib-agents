"""Shared theme CSS for all pages."""

# ── Color tokens ───────────────────────────────────────────────────────
DARK = {
    "page_bg":        "#0f172a",
    "card_bg":        "#1e293b",
    "card_hover":     "#263045",
    "border":         "#334155",
    "text":           "#f1f5f9",
    "text_sec":       "#94a3b8",
    "text_muted":     "#64748b",
    "accent":         "#3b82f6",
    # stat boxes
    "stat_neutral_bg": "#1e293b",  "stat_neutral_txt": "#f1f5f9",
    "stat_green_bg":   "#064e3b",  "stat_green_txt":   "#6ee7b7",
    "stat_red_bg":     "#450a0a",  "stat_red_txt":     "#fca5a5",
    # banners
    "success_bg":     "#064e3b",  "success_border":   "#065f46",  "success_txt": "#6ee7b7",
    "error_bg":       "#450a0a",  "error_border":     "#7f1d1d",  "error_txt":   "#fca5a5",
    # download box
    "dl_bg":          "#1e3a5f",  "dl_border":        "#3b82f6",  "dl_txt":      "#93c5fd",  "dl_sub": "#bfdbfe",
    # api card
    "api_bg":         "#1e293b",  "api_border":       "#334155",
    "api_ok_accent":  "#22c55e",  "api_fail_accent":  "#ef4444",
    "api_ok_badge_bg":"#064e3b",  "api_ok_badge_txt": "#6ee7b7",
    "api_fail_badge_bg":"#450a0a","api_fail_badge_txt":"#fca5a5",
    "api_label":      "#64748b",  "api_val":          "#f1f5f9",
    # param box
    "param_bg":       "#263045",  "param_label":      "#64748b",  "param_val": "#f1f5f9",
    # badges
    "badge_bg":       "#1d3a8a",  "badge_txt":        "#93c5fd",
    # summary card
    "sumcard_bg":     "#1e293b",  "sumcard_border":   "#334155",
    "status_ok_bg":   "#064e3b",  "status_ok_txt":    "#6ee7b7",
    "status_err_bg":  "#450a0a",  "status_err_txt":   "#fca5a5",
    # section title
    "stitle_color":   "#94a3b8",  "stitle_border":    "#334155",
}

GREEN = {
    "page_bg":        "#f3f4f6",
    "card_bg":        "#ffffff",
    "card_hover":     "#f9fafb",
    "border":         "#e5e7eb",
    "text":           "#111827",
    "text_sec":       "#6b7280",
    "text_muted":     "#9ca3af",
    "accent":         "#166534",
    # stat boxes (featured = dark green, found = light green, missing = light red)
    "stat_neutral_bg": "#f9fafb",  "stat_neutral_txt": "#111827",
    "stat_green_bg":   "#166534",  "stat_green_txt":   "#ffffff",
    "stat_red_bg":     "#fef2f2",  "stat_red_txt":     "#991b1b",
    # banners
    "success_bg":     "#f0fdf4",  "success_border":   "#86efac",  "success_txt": "#166534",
    "error_bg":       "#fef2f2",  "error_border":     "#fca5a5",  "error_txt":   "#991b1b",
    # download box
    "dl_bg":          "#f0fdf4",  "dl_border":        "#166534",  "dl_txt":      "#166534",  "dl_sub": "#4b7c61",
    # api card
    "api_bg":         "#ffffff",  "api_border":       "#e5e7eb",
    "api_ok_accent":  "#16a34a",  "api_fail_accent":  "#ef4444",
    "api_ok_badge_bg":"#dcfce7",  "api_ok_badge_txt": "#166534",
    "api_fail_badge_bg":"#fee2e2","api_fail_badge_txt":"#991b1b",
    "api_label":      "#9ca3af",  "api_val":          "#111827",
    # param box
    "param_bg":       "#f9fafb",  "param_label":      "#6b7280",  "param_val": "#111827",
    # badges
    "badge_bg":       "#dcfce7",  "badge_txt":        "#166534",
    # summary card
    "sumcard_bg":     "#ffffff",  "sumcard_border":   "#e5e7eb",
    "status_ok_bg":   "#dcfce7",  "status_ok_txt":    "#166534",
    "status_err_bg":  "#fee2e2",  "status_err_txt":   "#991b1b",
    # section title
    "stitle_color":   "#374151",  "stitle_border":    "#166534",
}


def get_streamlit_overrides(t: dict) -> str:
    """CSS that overrides Streamlit's native widget colors."""
    return f"""
    /* ─── Streamlit base overrides ─────────────────────────────────── */
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {t["page_bg"]} !important;
    }}
    .main .block-container {{
        background-color: {t["page_bg"]} !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        background-color: {t["card_bg"]} !important;
        border-right: 1px solid {t["border"]} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {t["text"]} !important;
    }}
    [data-testid="stHeader"] {{
        background-color: {t["page_bg"]} !important;
    }}
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {t["card_bg"]} !important;
        border-bottom: 2px solid {t["border"]} !important;
        gap: 0;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {t["text_sec"]} !important;
        background-color: transparent !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: {t["accent"]} !important;
        border-bottom: 2px solid {t["accent"]} !important;
    }}
    /* Buttons */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {{
        background-color: {t["accent"]} !important;
        border-color: {t["accent"]} !important;
        color: #ffffff !important;
    }}
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {{
        background-color: transparent !important;
        border-color: {t["accent"]} !important;
        color: {t["accent"]} !important;
    }}
    /* Download button */
    .stDownloadButton > button {{
        background-color: {t["accent"]} !important;
        border-color: {t["accent"]} !important;
        color: #ffffff !important;
    }}
    /* Metrics */
    [data-testid="metric-container"] {{
        background-color: {t["card_bg"]} !important;
        border: 1px solid {t["border"]} !important;
        border-radius: 10px;
        padding: 1rem;
    }}
    [data-testid="stMetricValue"] {{ color: {t["text"]} !important; }}
    [data-testid="stMetricLabel"] {{ color: {t["text_sec"]} !important; }}
    /* Alerts */
    [data-testid="stAlert"] {{
        background-color: {t["success_bg"]} !important;
        border-color: {t["success_border"]} !important;
        color: {t["text"]} !important;
    }}
    /* Divider */
    hr {{ border-color: {t["border"]} !important; }}
    /* Caption */
    .stCaptionContainer p, small {{ color: {t["text_muted"]} !important; }}
    /* Markdown text */
    .stMarkdown p, .stMarkdown li {{ color: {t["text"]} !important; }}
    /* File uploader */
    [data-testid="stFileUploaderDropzone"] {{
        background-color: {t["card_bg"]} !important;
        border-color: {t["border"]} !important;
    }}
    [data-testid="stFileUploaderDropzoneInstructions"] p,
    [data-testid="stFileUploaderDropzoneInstructions"] small {{
        color: {t["text_sec"]} !important;
    }}
    /* Text inputs */
    .stTextInput input {{
        background-color: {t["card_bg"]} !important;
        color: {t["text"]} !important;
        border-color: {t["border"]} !important;
    }}
    .stTextInput label {{ color: {t["text"]} !important; }}
    .stFileUploader label {{ color: {t["text"]} !important; }}
    /* Spinner */
    [data-testid="stSpinner"] > div {{
        border-top-color: {t["accent"]} !important;
    }}
    /* Dataframe */
    [data-testid="stDataFrameResizable"] {{
        background-color: {t["card_bg"]} !important;
        border-color: {t["border"]} !important;
    }}
    """


def get_page_css(t: dict) -> str:
    """CSS for all custom HTML component classes used across pages."""
    return f"""
    /* ─── Custom component classes ─────────────────────────────────── */
    /* Tool cards (Home) */
    .tool-card {{
        background: {t["card_bg"]};
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid {t["border"]};
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }}
    .tool-card:hover {{
        border-color: {t["accent"]};
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }}
    .tool-title  {{ font-size: 1.25rem; font-weight: 600; color: {t["text"]}; margin-bottom: 0.25rem; }}
    .tool-desc   {{ color: {t["text_sec"]}; font-size: 0.9rem; }}
    .tool-badge  {{ display:inline-block; background:{t["badge_bg"]}; color:{t["badge_txt"]};
                   padding:2px 10px; border-radius:12px; font-size:0.75rem; font-weight:500; margin-top:0.75rem; }}
    /* Section titles */
    .section-title {{
        font-size: 1.05rem;
        font-weight: 600;
        color: {t["stitle_color"]};
        margin: 1.5rem 0 0.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {t["stitle_border"]};
    }}
    /* Param boxes (IB UCC) */
    .param-box   {{ background:{t["param_bg"]}; border-radius:8px; padding:1rem; margin:0.5rem 0; border:1px solid {t["border"]}; }}
    .param-label {{ font-size:0.85rem; color:{t["param_label"]}; margin-bottom:0.25rem; }}
    .param-value {{ font-size:1rem; font-weight:600; color:{t["param_val"]}; }}
    /* Banners */
    .success-banner {{ background:{t["success_bg"]}; border:1px solid {t["success_border"]}; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1rem; }}
    .fail-banner    {{ background:{t["error_bg"]};   border:1px solid {t["error_border"]};   border-radius:10px; padding:1rem 1.5rem; margin-bottom:1rem; }}
    /* Download box */
    .download-box {{ background:{t["dl_bg"]}; border:2px solid {t["dl_border"]}; border-radius:12px; padding:1.5rem; margin:1rem 0; }}
    .download-box p {{ color:{t["dl_txt"]} !important; margin:0; }}
    .download-box b {{ color:{t["dl_sub"]} !important; }}
    /* Stat boxes */
    .stat-box {{ text-align:center; padding:1.25rem 1rem; border-radius:10px; }}
    .stat-number {{ font-size:2.2rem; font-weight:700; line-height:1; }}
    .stat-label  {{ font-size:0.9rem; color:{t["text_sec"]}; margin-top:0.4rem; }}
    /* API card */
    .api-card    {{ background:{t["api_bg"]}; border:1px solid {t["api_border"]}; border-radius:10px; padding:1.25rem; margin:1rem 0; }}
    .api-success {{ border-left:4px solid {t["api_ok_accent"]}; }}
    .api-fail    {{ border-left:4px solid {t["api_fail_accent"]}; }}
    /* Summary card (SEBI) */
    .summary-card {{ background:{t["sumcard_bg"]}; border:1px solid {t["sumcard_border"]}; border-radius:12px; padding:1.25rem 1.5rem; margin:0.5rem 0; }}
    .stat-row  {{ display:flex; justify-content:space-between; align-items:center; padding:0.5rem 0; border-bottom:1px solid {t["border"]}; }}
    .stat-row:last-child {{ border-bottom:none; }}
    .stat-key  {{ color:{t["text_sec"]}; font-size:0.9rem; }}
    .stat-val  {{ color:{t["text"]}; font-weight:600; font-size:1rem; }}
    .status-ok  {{ display:inline-block; background:{t["status_ok_bg"]};  color:{t["status_ok_txt"]};  padding:3px 12px; border-radius:20px; font-size:0.85rem; font-weight:600; }}
    .status-err {{ display:inline-block; background:{t["status_err_bg"]}; color:{t["status_err_txt"]}; padding:3px 12px; border-radius:20px; font-size:0.85rem; font-weight:600; }}
    /* Login card */
    .login-card  {{ max-width:420px; margin:4rem auto 0 auto; padding:2.5rem 2rem; border-radius:16px;
                   background:{t["card_bg"]}; border:1px solid {t["border"]}; box-shadow:0 8px 32px rgba(0,0,0,0.15); }}
    .login-title    {{ text-align:center; font-size:2rem; font-weight:700; color:{t["text"]}; margin-bottom:0.35rem; }}
    .login-subtitle {{ text-align:center; color:{t["text_sec"]}; margin-bottom:1.75rem; font-size:0.95rem; }}
    .login-hint     {{ text-align:center; margin-top:1.5rem; color:{t["text_muted"]}; font-size:0.8rem; line-height:1.6; }}
    .login-hint b   {{ color:{t["text_sec"]}; }}
    """


def full_css(theme_name: str) -> str:
    t = GREEN if theme_name == "green" else DARK
    return f"<style>{get_streamlit_overrides(t)}{get_page_css(t)}</style>"


def glass_css() -> str:
    """AI glass dark theme — overlay on top of full_css() for all pages."""
    return """<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > section,
    [data-testid="stMain"] {
        font-family: 'Inter', sans-serif;
        background: #020c09 !important;
        overflow-x: hidden;
    }
    .main .block-container,
    [data-testid="stMainBlockContainer"] {
        background: transparent !important;
        padding-top: 1.5rem;
        position: relative;
        z-index: 2;
    }
    .ib-bg-watermark {
        position: fixed; inset: 0; z-index: 0;
        pointer-events: none; overflow: hidden;
    }
    .ib-bg-watermark::before {
        content: 'IB';
        position: absolute; top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        font-size: 42vw; font-weight: 900;
        color: transparent;
        -webkit-text-stroke: 1px rgba(16,185,129,0.04);
        letter-spacing: -0.05em; line-height: 1;
        font-family: 'Inter', sans-serif; user-select: none;
    }
    .ib-bg-watermark::after {
        content: 'INDIABONDS';
        position: absolute; top: calc(50% + 18vw); left: 50%;
        transform: translateX(-50%);
        font-size: 4.5vw; font-weight: 800;
        color: transparent;
        -webkit-text-stroke: 1px rgba(16,185,129,0.06);
        letter-spacing: 0.4em; font-family: 'Inter', sans-serif;
        white-space: nowrap; user-select: none;
    }
    .ib-glow-1 {
        position: fixed; top: -10%; left: -10%;
        width: 60vw; height: 60vw;
        background: radial-gradient(circle, rgba(16,185,129,0.07) 0%, transparent 65%);
        pointer-events: none; z-index: 0;
        animation: drift1 18s ease-in-out infinite alternate;
    }
    .ib-glow-2 {
        position: fixed; bottom: -10%; right: -10%;
        width: 55vw; height: 55vw;
        background: radial-gradient(circle, rgba(6,182,212,0.06) 0%, transparent 65%);
        pointer-events: none; z-index: 0;
        animation: drift2 22s ease-in-out infinite alternate;
    }
    .ib-glow-3 {
        position: fixed; top: 30%; right: 20%;
        width: 30vw; height: 30vw;
        background: radial-gradient(circle, rgba(52,211,153,0.04) 0%, transparent 65%);
        pointer-events: none; z-index: 0;
        animation: drift3 14s ease-in-out infinite alternate;
    }
    @keyframes drift1 {
        0%   { transform: translate(0,0) scale(1); }
        100% { transform: translate(5%,8%) scale(1.1); }
    }
    @keyframes drift2 {
        0%   { transform: translate(0,0) scale(1); }
        100% { transform: translate(-6%,-5%) scale(1.08); }
    }
    @keyframes drift3 {
        0%   { transform: translate(0,0) scale(1); }
        100% { transform: translate(3%,6%) scale(1.05); }
    }
    .ib-grid-overlay {
        position: fixed; inset: 0; z-index: 0; pointer-events: none;
        background-image:
            linear-gradient(rgba(16,185,129,0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(16,185,129,0.02) 1px, transparent 1px);
        background-size: 60px 60px;
        mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
    }
    [data-testid="stSidebar"] {
        background: rgba(5,15,11,0.92) !important;
        border-right: 1px solid rgba(16,185,129,0.1) !important;
        backdrop-filter: blur(20px) !important;
    }
    [data-testid="stSidebar"] * { color: #e5e7eb !important; }
    /* Glass section titles */
    .glass-section-title {
        display: flex; align-items: center; gap: 1rem;
        margin: 2rem 0 1.25rem; color: #374151;
        font-size: 0.72rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.15em;
        font-family: 'JetBrains Mono', monospace;
        position: relative; z-index: 2;
    }
    .glass-section-title::before, .glass-section-title::after {
        content: ''; flex: 1; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(16,185,129,0.3), transparent);
    }
    /* Glass card for tool pages */
    .glass-page-card {
        background: linear-gradient(135deg,
            rgba(16,185,129,0.07) 0%,
            rgba(6,182,212,0.04) 50%,
            rgba(16,185,129,0.06) 100%) !important;
        backdrop-filter: blur(28px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
        border: 1px solid rgba(52,211,153,0.18) !important;
        border-radius: 1.25rem; padding: 1.75rem;
        position: relative; overflow: hidden; z-index: 2;
        box-shadow: 0 4px 24px rgba(0,0,0,0.5),
            inset 0 1px 0 rgba(52,211,153,0.12),
            inset 0 -1px 0 rgba(52,211,153,0.05);
    }
    .glass-page-card::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent 5%, rgba(52,211,153,0.5) 50%, transparent 95%);
        z-index: 4;
    }
    /* Override section-title for glass pages */
    .section-title {
        font-family: 'JetBrains Mono', monospace !important;
        color: #6ee7b7 !important;
        border-bottom-color: rgba(52,211,153,0.25) !important;
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
    }
    /* Override download-box for glass */
    .download-box {
        background: rgba(16,185,129,0.06) !important;
        border-color: rgba(52,211,153,0.3) !important;
    }
    /* Override summary-card, api-card for glass */
    .summary-card, .api-card {
        background: rgba(10,20,16,0.7) !important;
        border-color: rgba(52,211,153,0.15) !important;
        backdrop-filter: blur(16px);
    }
    .stat-row { border-bottom-color: rgba(52,211,153,0.1) !important; }
    .stat-key { color: #6b7280 !important; }
    .stat-val { color: #e5e7eb !important; }
    /* Tabs glass */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(10,20,16,0.7) !important;
        border-bottom-color: rgba(52,211,153,0.15) !important;
        backdrop-filter: blur(16px);
    }
    .stTabs [data-baseweb="tab"] { color: #6b7280 !important; }
    .stTabs [aria-selected="true"] {
        color: #34d399 !important;
        border-bottom-color: #34d399 !important;
    }
    /* Buttons glass */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"],
    .stDownloadButton > button {
        background: linear-gradient(135deg, #065f46 0%, #0e7490 100%) !important;
        border-color: rgba(52,211,153,0.4) !important;
        color: #d1fae5 !important;
        box-shadow: 0 4px 20px rgba(6,182,212,0.25) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button:hover {
        border-color: rgba(52,211,153,0.65) !important;
        filter: brightness(1.15) !important;
        box-shadow: 0 8px 30px rgba(16,185,129,0.4) !important;
    }
    /* Metrics glass */
    [data-testid="metric-container"] {
        background: rgba(10,20,16,0.7) !important;
        border-color: rgba(52,211,153,0.12) !important;
        backdrop-filter: blur(16px);
    }
    [data-testid="stMetricValue"] { color: #e5e7eb !important; }
    [data-testid="stMetricLabel"] { color: #6b7280 !important; }
    /* File uploader glass */
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(10,20,16,0.6) !important;
        border-color: rgba(52,211,153,0.2) !important;
    }
    /* Param box glass */
    .param-box {
        background: rgba(10,20,16,0.6) !important;
        border-color: rgba(52,211,153,0.15) !important;
    }
    .param-label { color: #6b7280 !important; }
    .param-value { color: #e5e7eb !important; }
    /* Stat boxes glass */
    .stat-box { backdrop-filter: blur(8px); }
    /* Login glass card */
    .login-glass-card {
        max-width: 420px; margin: 0 auto;
        padding: 2.5rem 2rem; border-radius: 1.5rem;
        background: linear-gradient(135deg,
            rgba(16,185,129,0.09) 0%,
            rgba(6,182,212,0.05) 50%,
            rgba(16,185,129,0.07) 100%);
        border: 1px solid rgba(52,211,153,0.2);
        box-shadow: 0 8px 40px rgba(0,0,0,0.6),
            inset 0 1px 0 rgba(52,211,153,0.15);
        backdrop-filter: blur(28px) saturate(180%);
        position: relative; z-index: 2;
    }
    .login-glass-card::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent 5%, rgba(52,211,153,0.6) 50%, transparent 95%);
        border-radius: 1.5rem 1.5rem 0 0;
    }
    .login-glass-subtitle {
        text-align: center; font-size: 0.9rem;
        color: #6b7280; margin-bottom: 1.75rem;
        font-family: 'Inter', sans-serif;
    }
    /* Login form inputs */
    .login-glass-card .stTextInput input {
        background: rgba(10,20,16,0.6) !important;
        border-color: rgba(52,211,153,0.2) !important;
        color: #e5e7eb !important; border-radius: 0.7rem !important;
    }
    .login-glass-card .stTextInput label { color: #9ca3af !important; }
    .login-glass-card .stButton > button {
        background: linear-gradient(135deg, #065f46 0%, #0e7490 100%) !important;
        border-color: rgba(52,211,153,0.4) !important;
        color: #d1fae5 !important; border-radius: 0.7rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 20px rgba(6,182,212,0.3) !important;
    }
    .stDeployButton, footer { display: none !important; }
    </style>"""


def glass_background_html() -> str:
    """Returns the HTML overlay divs for the glass background effect."""
    return """
<div class="ib-bg-watermark"></div>
<div class="ib-glow-1"></div>
<div class="ib-glow-2"></div>
<div class="ib-glow-3"></div>
<div class="ib-grid-overlay"></div>
"""


def sidebar_toggle(current_theme: str) -> str:
    """Returns the opposite theme name after the user clicks toggle."""
    return "green" if current_theme == "dark" else "dark"


def theme_tokens(theme_name: str) -> dict:
    return GREEN if theme_name == "green" else DARK


def role_indicator_html(role: str) -> str:
    """Fixed top-right dot: green = user/prod, red = admin/QA."""
    is_admin = role == "admin"
    color = "#ef4444" if is_admin else "#22c55e"
    label = "QA" if is_admin else "PROD"
    return f"""
<div style="
    position:fixed;top:12px;right:16px;z-index:99999;
    display:flex;align-items:center;gap:6px;
    background:rgba(2,12,9,0.55);
    border:1px solid rgba(255,255,255,0.07);
    border-radius:20px;padding:4px 10px 4px 7px;
    backdrop-filter:blur(8px);
    font-family:'Inter',sans-serif;font-size:11px;
    color:rgba(255,255,255,0.45);letter-spacing:0.04em;
">
    <span style="
        width:8px;height:8px;border-radius:50%;
        background:{color};box-shadow:0 0 7px {color};
        display:inline-block;animation:_role-pulse 2.4s ease-in-out infinite;
    "></span>
    {label}
</div>
<style>
@keyframes _role-pulse{{0%,100%{{opacity:1}}50%{{opacity:0.45}}}}
</style>"""
