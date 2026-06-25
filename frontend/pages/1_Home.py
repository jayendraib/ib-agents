import streamlit as st
import sys
import base64
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from theme import full_css, sidebar_toggle, theme_tokens, glass_background_html, role_indicator_html

# ========== AUTH GUARD ==========
if not st.session_state.get("authenticated", False):
    st.switch_page("app.py")

st.set_page_config(
    page_title="Home | India Bonds AI Automation",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>[data-testid="stSidebarNav"] { display: none !important; }</style>
""", unsafe_allow_html=True)

# ========== THEME ==========
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

st.markdown(full_css(st.session_state.theme), unsafe_allow_html=True)
t = theme_tokens(st.session_state.theme)
st.markdown(role_indicator_html(st.session_state.get("role", "user")), unsafe_allow_html=True)

# ========== FULL AI GLASS THEME ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ===== ROOT BACKGROUND ===== */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #020c09 !important;
        overflow-x: hidden;
    }

    .main .block-container {
        background: transparent !important;
        padding-top: 1.5rem;
        position: relative;
        z-index: 2;
    }

    /* ===== IB WATERMARK BACKGROUND ===== */
    .ib-bg-watermark {
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    }

    /* Large IB logo text watermark */
    .ib-bg-watermark::before {
        content: 'IB';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 42vw;
        font-weight: 900;
        color: transparent;
        -webkit-text-stroke: 1px rgba(16, 185, 129, 0.04);
        letter-spacing: -0.05em;
        line-height: 1;
        font-family: 'Inter', sans-serif;
        user-select: none;
    }

    /* IndiaBonds text below */
    .ib-bg-watermark::after {
        content: 'INDIABONDS';
        position: absolute;
        top: calc(50% + 18vw);
        left: 50%;
        transform: translateX(-50%);
        font-size: 4.5vw;
        font-weight: 800;
        color: transparent;
        -webkit-text-stroke: 1px rgba(16, 185, 129, 0.06);
        letter-spacing: 0.4em;
        font-family: 'Inter', sans-serif;
        white-space: nowrap;
        user-select: none;
    }

    /* ===== AMBIENT RADIAL GLOWS ===== */
    .ib-glow-1 {
        position: fixed;
        top: -10%;
        left: -10%;
        width: 60vw;
        height: 60vw;
        background: radial-gradient(circle, rgba(16,185,129,0.07) 0%, transparent 65%);
        pointer-events: none;
        z-index: 0;
        animation: drift1 18s ease-in-out infinite alternate;
    }
    .ib-glow-2 {
        position: fixed;
        bottom: -10%;
        right: -10%;
        width: 55vw;
        height: 55vw;
        background: radial-gradient(circle, rgba(6,182,212,0.06) 0%, transparent 65%);
        pointer-events: none;
        z-index: 0;
        animation: drift2 22s ease-in-out infinite alternate;
    }
    .ib-glow-3 {
        position: fixed;
        top: 30%;
        right: 20%;
        width: 30vw;
        height: 30vw;
        background: radial-gradient(circle, rgba(52,211,153,0.04) 0%, transparent 65%);
        pointer-events: none;
        z-index: 0;
        animation: drift3 14s ease-in-out infinite alternate;
    }

    @keyframes drift1 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(5%, 8%) scale(1.1); }
    }
    @keyframes drift2 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(-6%, -5%) scale(1.08); }
    }
    @keyframes drift3 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(3%, 6%) scale(1.05); }
    }

    /* ===== SCAN-LINE GRID OVERLAY ===== */
    .ib-grid-overlay {
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background-image:
            linear-gradient(rgba(16,185,129,0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(16,185,129,0.02) 1px, transparent 1px);
        background-size: 60px 60px;
        mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
    }

    /* ===== HEADER ===== */
    .dashboard-header {
        position: relative;
        z-index: 2;
        margin-bottom: 2rem;
    }

    .dashboard-label {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 500;
        color: #34d399;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        margin-bottom: 1rem;
        padding: 0.35rem 1rem;
        background: rgba(16,185,129,0.08);
        border: 1px solid rgba(16,185,129,0.2);
        border-radius: 9999px;
        backdrop-filter: blur(8px);
    }

    .dashboard-label .pulse {
        width: 6px;
        height: 6px;
        background: #34d399;
        border-radius: 50%;
        animation: pulse-glow 2s ease-in-out infinite;
        box-shadow: 0 0 8px #34d399;
    }

    @keyframes pulse-glow {
        0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 8px #34d399; }
        50% { opacity: 0.4; transform: scale(0.75); box-shadow: 0 0 3px #34d399; }
    }

    .dashboard-title {
        font-size: 3rem;
        font-weight: 900;
        color: #f0fdf4;
        margin: 0;
        letter-spacing: -0.04em;
        line-height: 1.05;
    }

    .dashboard-title .grad {
        background: linear-gradient(135deg, #34d399 0%, #22d3ee 60%, #6ee7b7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .dashboard-subtitle {
        font-size: 1rem;
        color: #6b7280;
        font-weight: 400;
        margin-top: 0.75rem;
        max-width: 520px;
        line-height: 1.7;
    }

    /* ===== SECTION DIVIDER ===== */
    .section-divider {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 2rem 0 1.75rem;
        color: #374151;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-family: 'JetBrains Mono', monospace;
        position: relative;
        z-index: 2;
    }

    .section-divider::before,
    .section-divider::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(16,185,129,0.3), transparent);
    }

    /* ===== GLASS MIRROR CARD ===== */
    .tool-card-mirror {
        background: linear-gradient(
            135deg,
            rgba(16,185,129,0.07) 0%,
            rgba(6,182,212,0.04) 50%,
            rgba(16,185,129,0.06) 100%
        ) !important;
        backdrop-filter: blur(28px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
        border: 1px solid rgba(52,211,153,0.18) !important;
        border-radius: 1.5rem;
        padding: 2rem;
        height: 100%;
        position: relative;
        overflow: hidden;
        transition: all 0.45s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 2;
        box-shadow:
            0 4px 24px rgba(0,0,0,0.5),
            inset 0 1px 0 rgba(52,211,153,0.12),
            inset 0 -1px 0 rgba(52,211,153,0.05);
    }

    /* Top mirror highlight */
    .tool-card-mirror::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 5%, rgba(52,211,153,0.7) 50%, transparent 95%);
        z-index: 4;
    }

    /* Moving shine sweep */
    .tool-card-mirror::after {
        content: '';
        position: absolute;
        top: -200%;
        left: -60%;
        width: 40%;
        height: 500%;
        background: linear-gradient(
            105deg,
            transparent 40%,
            rgba(52,211,153,0.06) 50%,
            rgba(34,211,238,0.04) 55%,
            transparent 65%
        );
        transform: skewX(-15deg);
        animation: card-sweep 7s ease-in-out infinite;
        pointer-events: none;
        z-index: 3;
    }

    @keyframes card-sweep {
        0%   { left: -60%; opacity: 0; }
        10%  { opacity: 1; }
        60%  { left: 120%; opacity: 1; }
        61%  { opacity: 0; }
        100% { left: 120%; opacity: 0; }
    }

    .tool-card-mirror:hover {
        transform: translateY(-8px) scale(1.01);
        border-color: rgba(52,211,153,0.45) !important;
        background: linear-gradient(
            135deg,
            rgba(16,185,129,0.13) 0%,
            rgba(6,182,212,0.08) 50%,
            rgba(16,185,129,0.11) 100%
        ) !important;
        box-shadow:
            0 30px 60px -12px rgba(0,0,0,0.8),
            0 0 50px rgba(16,185,129,0.18),
            0 0 100px rgba(6,182,212,0.08),
            inset 0 1px 0 rgba(52,211,153,0.2);
    }

    /* ===== TOOL ICON WITH CHARACTER ANIMATION ===== */
    .tool-icon-wrap {
        width: 3.75rem;
        height: 3.75rem;
        border-radius: 1.1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 5;
        flex-shrink: 0;
        transition: transform 0.3s ease;
        cursor: default;
    }

    .tool-icon-wrap:hover {
        transform: scale(1.15) rotate(-5deg);
    }

    /* Character orbit ring */
    .tool-icon-wrap .orbit-ring {
        position: absolute;
        inset: -8px;
        border-radius: 50%;
        border: 1px solid transparent;
        animation: orbit-spin 4s linear infinite;
    }

    .tool-icon-wrap.sebi .orbit-ring {
        border-top-color: rgba(52,211,153,0.7);
        border-right-color: rgba(52,211,153,0.2);
        box-shadow: 0 0 10px rgba(52,211,153,0.3);
    }

    .tool-icon-wrap.compare .orbit-ring {
        border-top-color: rgba(6,182,212,0.7);
        border-right-color: rgba(6,182,212,0.2);
        box-shadow: 0 0 10px rgba(6,182,212,0.3);
    }

    .tool-icon-wrap.coming .orbit-ring {
        border-top-color: rgba(245,158,11,0.5);
        border-right-color: rgba(245,158,11,0.15);
        animation-duration: 6s;
    }

    @keyframes orbit-spin {
        from { transform: rotate(0deg); }
        to   { transform: rotate(360deg); }
    }

    /* Counter-orbit dot */
    .tool-icon-wrap .orbit-dot {
        position: absolute;
        inset: -10px;
        border-radius: 50%;
        animation: orbit-spin-reverse 3s linear infinite;
    }

    .tool-icon-wrap.sebi .orbit-dot::before {
        content: '';
        position: absolute;
        top: 4px; left: 50%;
        width: 5px; height: 5px;
        background: #34d399;
        border-radius: 50%;
        box-shadow: 0 0 6px #34d399;
        transform: translateX(-50%);
    }

    .tool-icon-wrap.compare .orbit-dot::before {
        content: '';
        position: absolute;
        top: 4px; left: 50%;
        width: 5px; height: 5px;
        background: #22d3ee;
        border-radius: 50%;
        box-shadow: 0 0 6px #22d3ee;
        transform: translateX(-50%);
    }

    .tool-icon-wrap.coming .orbit-dot::before {
        content: '';
        position: absolute;
        top: 4px; left: 50%;
        width: 4px; height: 4px;
        background: #f59e0b;
        border-radius: 50%;
        box-shadow: 0 0 5px #f59e0b;
        transform: translateX(-50%);
        animation: flicker 1.5s ease-in-out infinite;
    }

    @keyframes orbit-spin-reverse {
        from { transform: rotate(360deg); }
        to   { transform: rotate(0deg); }
    }

    @keyframes flicker {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    /* Icon glow backgrounds */
    .tool-icon-wrap.sebi {
        background: linear-gradient(135deg, rgba(16,185,129,0.22), rgba(6,182,212,0.15));
        border: 1px solid rgba(16,185,129,0.4);
        box-shadow: 0 0 30px rgba(16,185,129,0.25), 0 0 60px rgba(16,185,129,0.08), inset 0 1px 0 rgba(255,255,255,0.1);
        animation: icon-breathe-green 3s ease-in-out infinite;
    }

    .tool-icon-wrap.compare {
        background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(59,130,246,0.12));
        border: 1px solid rgba(6,182,212,0.35);
        box-shadow: 0 0 25px rgba(6,182,212,0.2), 0 0 50px rgba(6,182,212,0.06), inset 0 1px 0 rgba(255,255,255,0.08);
        animation: icon-breathe-cyan 3.5s ease-in-out infinite;
    }

    .tool-icon-wrap.coming {
        background: linear-gradient(135deg, rgba(245,158,11,0.12), rgba(239,68,68,0.08));
        border: 1px solid rgba(245,158,11,0.25);
        box-shadow: 0 0 20px rgba(245,158,11,0.12), inset 0 1px 0 rgba(255,255,255,0.06);
    }

    @keyframes icon-breathe-green {
        0%, 100% { box-shadow: 0 0 30px rgba(16,185,129,0.25), 0 0 60px rgba(16,185,129,0.08), inset 0 1px 0 rgba(255,255,255,0.1); }
        50% { box-shadow: 0 0 45px rgba(16,185,129,0.45), 0 0 90px rgba(16,185,129,0.15), inset 0 1px 0 rgba(255,255,255,0.15); }
    }

    @keyframes icon-breathe-cyan {
        0%, 100% { box-shadow: 0 0 25px rgba(6,182,212,0.2), 0 0 50px rgba(6,182,212,0.06), inset 0 1px 0 rgba(255,255,255,0.08); }
        50% { box-shadow: 0 0 40px rgba(6,182,212,0.38), 0 0 80px rgba(6,182,212,0.12), inset 0 1px 0 rgba(255,255,255,0.12); }
    }

    /* ===== CARD TEXT ===== */
    .tool-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f9fafb;
        margin-bottom: 0.6rem;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 5;
    }

    .tool-desc {
        font-size: 0.875rem;
        color: #9ca3af;
        line-height: 1.75;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 5;
    }

    .feature-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 5;
    }

    .feature-tag {
        background: rgba(16,185,129,0.08);
        color: #6ee7b7;
        padding: 0.25rem 0.75rem;
        border-radius: 0.4rem;
        font-size: 0.7rem;
        font-weight: 600;
        border: 1px solid rgba(16,185,129,0.15);
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.05em;
        transition: all 0.2s ease;
    }

    .feature-tag:hover {
        background: rgba(16,185,129,0.18);
        border-color: rgba(16,185,129,0.35);
        color: #a7f3d0;
    }

    /* compare card tags */
    .tool-card-mirror:nth-child(2) .feature-tag {
        background: rgba(6,182,212,0.08);
        color: #67e8f9;
        border-color: rgba(6,182,212,0.15);
    }

    /* ===== FLOATING CHAR PARTICLES (canvas-less CSS version) ===== */
    .char-float {
        position: absolute;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 500;
        color: rgba(52,211,153,0.25);
        pointer-events: none;
        z-index: 1;
        animation: char-drift linear infinite;
        user-select: none;
    }

    @keyframes char-drift {
        0%   { transform: translateY(0) rotate(0deg); opacity: 0; }
        10%  { opacity: 1; }
        90%  { opacity: 0.6; }
        100% { transform: translateY(-120px) rotate(20deg); opacity: 0; }
    }

    /* ===== STATS BAR ===== */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        position: relative;
        z-index: 2;
    }

    .stat-card {
        background: rgba(10,20,16,0.7);
        border: 1px solid rgba(16,185,129,0.12);
        border-radius: 1rem;
        padding: 1.1rem 1.35rem;
        display: flex;
        align-items: center;
        gap: 0.9rem;
        flex: 1;
        backdrop-filter: blur(16px);
        transition: border-color 0.3s ease;
    }

    .stat-card:hover {
        border-color: rgba(16,185,129,0.28);
    }

    .stat-icon {
        width: 2.4rem;
        height: 2.4rem;
        border-radius: 0.7rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        background: rgba(16,185,129,0.1);
        border: 1px solid rgba(16,185,129,0.2);
        flex-shrink: 0;
    }

    .stat-label {
        font-size: 0.65rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }

    .stat-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e5e7eb;
        margin-top: 0.1rem;
    }

    /* ===== LAUNCH BUTTONS ===== */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton > button,
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button,
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) .stButton > button {
        background: linear-gradient(135deg, #065f46 0%, #0e7490 100%) !important;
        color: #d1fae5 !important;
        border: 1px solid rgba(52,211,153,0.35) !important;
        border-radius: 0.8rem !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(6,182,212,0.25), inset 0 1px 0 rgba(255,255,255,0.08) !important;
        position: relative;
        z-index: 5;
    }

    div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton > button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(16,185,129,0.4), 0 0 20px rgba(6,182,212,0.2), inset 0 1px 0 rgba(255,255,255,0.12) !important;
        border-color: rgba(52,211,153,0.6) !important;
        filter: brightness(1.15) !important;
    }

    /* ===== MARKETING ICON ===== */
    .tool-icon-wrap.marketing {
        background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(168,85,247,0.12));
        border: 1px solid rgba(139,92,246,0.35);
        box-shadow: 0 0 25px rgba(139,92,246,0.2), 0 0 50px rgba(139,92,246,0.06), inset 0 1px 0 rgba(255,255,255,0.08);
        animation: icon-breathe-purple 3.5s ease-in-out infinite;
    }

    .tool-icon-wrap.marketing .orbit-ring {
        border-top-color: rgba(139,92,246,0.7);
        border-right-color: rgba(139,92,246,0.2);
        box-shadow: 0 0 10px rgba(139,92,246,0.3);
    }

    .tool-icon-wrap.marketing .orbit-dot::before {
        content: '';
        position: absolute;
        top: 4px; left: 50%;
        width: 5px; height: 5px;
        background: #a78bfa;
        border-radius: 50%;
        box-shadow: 0 0 6px #a78bfa;
        transform: translateX(-50%);
    }

    @keyframes icon-breathe-purple {
        0%, 100% { box-shadow: 0 0 25px rgba(139,92,246,0.2), 0 0 50px rgba(139,92,246,0.06), inset 0 1px 0 rgba(255,255,255,0.08); }
        50%       { box-shadow: 0 0 40px rgba(139,92,246,0.38), 0 0 80px rgba(139,92,246,0.12), inset 0 1px 0 rgba(255,255,255,0.12); }
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: rgba(5,15,11,0.92) !important;
        border-right: 1px solid rgba(16,185,129,0.1) !important;
        backdrop-filter: blur(20px) !important;
    }

    /* ===== FOOTER ===== */
    .footer {
        margin-top: 3rem;
        padding: 1.5rem 0;
        border-top: 1px solid rgba(16,185,129,0.08);
        text-align: center;
        position: relative;
        z-index: 2;
    }

    .footer-text {
        color: #374151;
        font-size: 0.72rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.1em;
    }

    .footer-text .accent { color: #10b981; }

    .stDeployButton, footer { display: none !important; }

    /* ===== MINI BOT (header) ===== */
    .bot-scene{position:relative;width:160px;height:248px;cursor:pointer;filter:drop-shadow(0 0 28px rgba(16,185,129,0.28));transition:all 0.3s ease;}
    .bot-scene:hover{filter:drop-shadow(0 0 55px rgba(16,185,129,0.6));}
    .bot-antenna{position:absolute;top:0;left:50%;transform:translateX(-50%);width:4px;height:26px;background:linear-gradient(180deg,#34d399,rgba(52,211,153,0.3));border-radius:2px;}
    .bot-antenna::after{content:'';position:absolute;top:-8px;left:50%;transform:translateX(-50%);width:14px;height:14px;background:#34d399;border-radius:50%;box-shadow:0 0 12px #34d399,0 0 28px rgba(52,211,153,0.6);animation:ant-pulse 1.8s ease-in-out infinite;}
    @keyframes ant-pulse{0%,100%{transform:translateX(-50%) scale(1);}50%{transform:translateX(-50%) scale(1.5);}}
    .bot-head{position:absolute;top:24px;left:50%;transform:translateX(-50%);width:124px;height:100px;background:linear-gradient(135deg,rgba(16,185,129,0.22),rgba(6,182,212,0.18));border:2px solid rgba(52,211,153,0.52);border-radius:22px;backdrop-filter:blur(12px);box-shadow:0 0 25px rgba(16,185,129,0.2),inset 0 1px 0 rgba(255,255,255,0.1);animation:bot-bob 3s ease-in-out infinite;overflow:hidden;}
    .bot-head::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(52,211,153,0.85),transparent);}
    @keyframes bot-bob{0%,100%{transform:translateX(-50%) translateY(0);}50%{transform:translateX(-50%) translateY(-6px);}}
    .bot-eyes{display:flex;gap:20px;justify-content:center;padding-top:22px;}
    .bot-eye{width:22px;height:22px;background:radial-gradient(circle,#fff 20%,#34d399 60%,rgba(52,211,153,0.3) 100%);border-radius:50%;box-shadow:0 0 14px #34d399,0 0 28px rgba(52,211,153,0.5);animation:eye-blink 4s ease-in-out infinite;}
    @keyframes eye-blink{0%,88%,100%{transform:scaleY(1);}93%{transform:scaleY(0.08);}}
    .bot-mouth{width:52px;height:15px;border:2px solid rgba(52,211,153,0.7);border-top:none;border-radius:0 0 26px 26px;margin:12px auto 0;background:rgba(52,211,153,0.12);}
    .bot-body{position:absolute;top:131px;left:50%;transform:translateX(-50%);width:104px;height:82px;background:linear-gradient(135deg,rgba(16,185,129,0.2),rgba(6,182,212,0.14));border:2px solid rgba(52,211,153,0.42);border-radius:18px;backdrop-filter:blur(12px);display:flex;align-items:center;justify-content:center;animation:bot-bob 3s ease-in-out infinite;}
    .bot-chest-txt{font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:700;color:#34d399;letter-spacing:0.08em;text-shadow:0 0 12px #34d399,0 0 24px rgba(52,211,153,0.4);}
    .bot-arm-l{position:absolute;top:138px;left:16px;width:18px;height:54px;background:linear-gradient(180deg,rgba(16,185,129,0.28),rgba(6,182,212,0.18));border:2px solid rgba(52,211,153,0.4);border-radius:10px;animation:bot-bob 3s ease-in-out infinite;}
    .bot-arm-r{position:absolute;top:133px;right:14px;width:18px;height:54px;background:linear-gradient(180deg,rgba(16,185,129,0.28),rgba(6,182,212,0.18));border:2px solid rgba(52,211,153,0.4);border-radius:10px;transform-origin:50% 0%;animation:wave-arm 0.65s ease-in-out infinite;}
    @keyframes wave-arm{0%,100%{transform:rotate(-65deg);}50%{transform:rotate(-95deg);}}
    .bot-leg-l{position:absolute;bottom:0;left:50%;margin-left:-21px;width:18px;height:32px;background:linear-gradient(180deg,rgba(16,185,129,0.25),rgba(6,182,212,0.15));border:2px solid rgba(52,211,153,0.38);border-radius:10px;}
    .bot-leg-r{position:absolute;bottom:0;left:50%;margin-left:3px;width:18px;height:32px;background:linear-gradient(180deg,rgba(16,185,129,0.25),rgba(6,182,212,0.15));border:2px solid rgba(52,211,153,0.38);border-radius:10px;}
    .bot-pt{position:absolute;width:5px;height:5px;background:#34d399;border-radius:50%;box-shadow:0 0 6px #34d399;animation:float-pt linear infinite;opacity:0;}
    @keyframes float-pt{0%{transform:translateY(0) scale(0);opacity:0;}10%{opacity:1;transform:scale(1);}90%{opacity:0.5;}100%{transform:translateY(-80px) scale(0.3);opacity:0;}}

    @media (max-width: 768px) {
        .dashboard-title { font-size: 2.2rem; }
        .stats-container { flex-direction: column; }
        .tool-card-mirror { padding: 1.5rem; }
        .ib-bg-watermark::before { font-size: 55vw; }
        .ib-bg-watermark::after { font-size: 7vw; }
    }
</style>

""", unsafe_allow_html=True)

st.markdown(glass_background_html(), unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("""
        <style>
            /* Glass sidebar background */
            [data-testid="stSidebar"] > div:first-child {
                background: rgba(5,15,11,0.97) !important;
                border-right: 1px solid rgba(16,185,129,0.12) !important;
            }
            /* Push logout to bottom */
            [data-testid="stSidebarUserContent"] {
                display: flex;
                flex-direction: column;
                min-height: calc(100vh - 3rem);
            }
            [data-testid="stSidebarUserContent"] > div:has(.sidebar-spacer) {
                flex: 1;
            }
        </style>
    """, unsafe_allow_html=True)

    # User info (top)
    st.markdown(f"""
        <div style="padding: 1rem 0;">
            <div style="font-size: 1rem; font-weight: 700; color: #f9fafb; margin-bottom: 0.25rem; font-family: 'Inter', sans-serif;">
                👤 {st.session_state.get('username', 'User')}
            </div>
            <div style="font-size: 0.72rem; color: #10b981; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.08em;">
                ● {"ADMIN ACCESS" if st.session_state.get("role", "admin") == "admin" else "USER ACCESS"}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Flex spacer — pushes logout to bottom
    st.markdown('<div class="sidebar-spacer" style="flex:1; min-height:40px;"></div>', unsafe_allow_html=True)

    # Logout button (bottom)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

# ========== HEADER ==========
st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-label">
            <div class="pulse"></div>
            AI AUTOMATION
        </div>
    </div>
""", unsafe_allow_html=True)

_logo_b64 = base64.b64encode(
    (Path(__file__).parent.parent / "indiabonds_logo.jpg").read_bytes()
).decode()
st.markdown(
    f'<div style="display:flex;align-items:center;gap:1rem;position:relative;z-index:2;">'
    f'<img src="data:image/jpeg;base64,{_logo_b64}" style="width:82px;height:82px;object-fit:contain;border-radius:14px;flex-shrink:0;" />'
    f'<h1 style="margin:0;font-size:2.75rem;font-weight:900;color:#f0fdf4;'
    f'font-family:Inter,sans-serif;letter-spacing:-0.04em;line-height:1.05;">'
    f'IndiaBonds&nbsp;<span style="background:linear-gradient(135deg,#34d399 0%,#22d3ee 60%,#6ee7b7 100%);'
    f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">AI</span>'
    f'</h1>'
    f'<div style="flex-shrink:0;zoom:0.52;line-height:0;align-self:flex-end;margin-bottom:-8px;">'
    f'<div class="bot-scene" style="margin:0;">'
    f'<div class="bot-antenna"></div>'
    f'<div class="bot-head">'
    f'<div class="bot-eyes"><div class="bot-eye"></div><div class="bot-eye"></div></div>'
    f'<div class="bot-mouth"></div>'
    f'</div>'
    f'<div class="bot-arm-l"></div>'
    f'<div class="bot-arm-r"></div>'
    f'<div class="bot-body"><span class="bot-chest-txt">AI</span></div>'
    f'<div class="bot-leg-l"></div>'
    f'<div class="bot-leg-r"></div>'
    f'<div class="bot-pt" style="left:22%;top:58%;animation-duration:3.2s;animation-delay:0s;"></div>'
    f'<div class="bot-pt" style="left:72%;top:52%;animation-duration:4s;animation-delay:1.1s;"></div>'
    f'<div class="bot-pt" style="left:50%;top:68%;animation-duration:2.8s;animation-delay:0.6s;"></div>'
    f'</div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown("""
    <p class="dashboard-subtitle" style="margin-top:0.5rem;">
        Intelligent Agent Automation orchestration from IndiaBonds AI.
    </p>
""", unsafe_allow_html=True)



# Section Title
st.markdown('<div class="section-divider">Available Agents</div>', unsafe_allow_html=True)

# ========== TOOLS GRID ==========
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="tool-card-mirror">
            <!-- Floating characters -->
            <span class="char-float" style="left:12%;bottom:20%;animation-duration:5s;animation-delay:0s;">Σ</span>
            <span class="char-float" style="left:25%;bottom:15%;animation-duration:6.5s;animation-delay:1.2s;">∂</span>
            <span class="char-float" style="left:60%;bottom:25%;animation-duration:4.8s;animation-delay:0.5s;">λ</span>
            <span class="char-float" style="left:78%;bottom:18%;animation-duration:7s;animation-delay:2s;">∞</span>
            <span class="char-float" style="left:45%;bottom:12%;animation-duration:5.5s;animation-delay:3s;">01</span>
            <!-- Icon with orbit animation -->
            <div class="tool-icon-wrap sebi">
                <div class="orbit-ring"></div>
                <div class="orbit-dot"></div>
                📊
            </div>
            <div class="tool-title">SEBI Debard</div>
            <div class="tool-desc">Automated Excel/ZIP ingestion pipeline with intelligent PAN-based deduplication and master table synthesis.</div>
            <div class="feature-tags">
                <span class="feature-tag">EXCEL</span>
                <span class="feature-tag">DEDUP</span>
                <span class="feature-tag">PIPELINE</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("▶  Launch Agent", key="btn_sebi", use_container_width=True):
        for k in ["uploaded_files", "pipeline_result", "processing_done", "master_df", "excel_bytes", "processed_at"]:
            st.session_state.pop(k, None)
        st.switch_page("pages/2_sebi_automate.py")

with col2:
    st.markdown("""
        <div class="tool-card-mirror">
            <!-- Floating characters -->
            <span class="char-float" style="left:10%;bottom:22%;animation-duration:6s;animation-delay:0.3s;color:rgba(34,211,238,0.25);">⊕</span>
            <span class="char-float" style="left:30%;bottom:16%;animation-duration:5.2s;animation-delay:1.8s;color:rgba(34,211,238,0.25);">∆</span>
            <span class="char-float" style="left:65%;bottom:28%;animation-duration:7.5s;animation-delay:0.8s;color:rgba(34,211,238,0.25);">≠</span>
            <span class="char-float" style="left:80%;bottom:14%;animation-duration:4.5s;animation-delay:2.5s;color:rgba(34,211,238,0.25);">∩</span>
            <span class="char-float" style="left:50%;bottom:10%;animation-duration:6.8s;animation-delay:1s;color:rgba(34,211,238,0.25);">⊗</span>
            <!-- Icon with orbit -->
            <div class="tool-icon-wrap compare">
                <div class="orbit-ring"></div>
                <div class="orbit-dot"></div>
                🔍
            </div>
            <div class="tool-title">IB UCC Compare</div>
            <div class="tool-desc">Cross-reference IB & UCC datasets to identify missing PANs and auto-trigger UCC status reconciliation.</div>
            <div class="feature-tags">
                <span class="feature-tag">COMPARE</span>
                <span class="feature-tag">MISSING</span>
                <span class="feature-tag">RESET</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("▶  Launch Agent", key="btn_compare", use_container_width=True):
        st.switch_page("pages/3_IB_UCC_Compare.py")

with col3:
    st.markdown("""
        <div class="tool-card-mirror">
            <!-- Floating characters (violet) -->
            <span class="char-float" style="left:14%;bottom:20%;animation-duration:5.5s;animation-delay:0s;color:rgba(139,92,246,0.25);">§</span>
            <span class="char-float" style="left:35%;bottom:14%;animation-duration:7s;animation-delay:1.4s;color:rgba(139,92,246,0.25);">⚖</span>
            <span class="char-float" style="left:62%;bottom:26%;animation-duration:6s;animation-delay:0.7s;color:rgba(139,92,246,0.25);">✓</span>
            <span class="char-float" style="left:80%;bottom:16%;animation-duration:8s;animation-delay:2.2s;color:rgba(139,92,246,0.25);">∅</span>
            <!-- Icon with orbit -->
            <div class="tool-icon-wrap marketing">
                <div class="orbit-ring"></div>
                <div class="orbit-dot"></div>
                📋
            </div>
            <div class="tool-title">Marketing Compliance</div>
            <div class="tool-desc">AI-powered SEBI OBPP advertisement code checker. Evaluate marketing scripts for regulatory compliance instantly.</div>
            <div class="feature-tags">
                <span class="feature-tag" style="background:rgba(139,92,246,0.08);color:#c4b5fd;border-color:rgba(139,92,246,0.15);">SEBI</span>
                <span class="feature-tag" style="background:rgba(139,92,246,0.08);color:#c4b5fd;border-color:rgba(139,92,246,0.15);">OBPP</span>
                <span class="feature-tag" style="background:rgba(139,92,246,0.08);color:#c4b5fd;border-color:rgba(139,92,246,0.15);">AI</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("▶  Launch Agent", key="btn_marketing", use_container_width=True):
        st.switch_page("pages/4_Marketing_Compliance.py")

# ========== FOOTER ==========
st.markdown("""
    <div class="footer">
        <div class="footer-text">
            <span class="accent">◆</span>&nbsp; INDIA BONDS AI AUTOMATION &nbsp;<span class="accent">◆</span>&nbsp; v2.0.1
        </div>
    </div>
""", unsafe_allow_html=True)
