import streamlit as st
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from theme import full_css, glass_css, glass_background_html

# ========== CONFIG ==========
st.set_page_config(
    page_title="Login | India Bonds AI",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""<style>
[data-testid="stSidebarNav"]{display:none!important;}
[data-testid="stSidebar"]{display:none!important;}
[data-testid="stHeader"]{display:none!important;}
.block-container{padding-top:2.5rem!important;padding-bottom:2rem!important;max-width:500px!important;}
.stDeployButton,footer{display:none!important;}
</style>""", unsafe_allow_html=True)

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

st.markdown(full_css(st.session_state.theme), unsafe_allow_html=True)
st.markdown(glass_css(), unsafe_allow_html=True)
st.markdown(glass_background_html(), unsafe_allow_html=True)

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Bot scene ────────────────────────────────── */
.bot-outer{display:flex;flex-direction:column;align-items:center;gap:1.5rem;margin-bottom:1.75rem;position:relative;z-index:2;}
.bot-scene{position:relative;width:160px;height:248px;cursor:pointer;filter:drop-shadow(0 0 28px rgba(16,185,129,0.28));transition:all 0.3s ease;margin:0 auto;}
.bot-scene:hover{filter:drop-shadow(0 0 55px rgba(16,185,129,0.6));transform:translateY(-8px);}
.bot-antenna{position:absolute;top:0;left:50%;transform:translateX(-50%);width:4px;height:26px;background:linear-gradient(180deg,#34d399,rgba(52,211,153,0.3));border-radius:2px;}
.bot-antenna::after{content:'';position:absolute;top:-8px;left:50%;transform:translateX(-50%);width:14px;height:14px;background:#34d399;border-radius:50%;box-shadow:0 0 12px #34d399,0 0 28px rgba(52,211,153,0.6);animation:ant-pulse 1.8s ease-in-out infinite;}
@keyframes ant-pulse{0%,100%{transform:translateX(-50%) scale(1);box-shadow:0 0 12px #34d399,0 0 28px rgba(52,211,153,0.6);}50%{transform:translateX(-50%) scale(1.5);box-shadow:0 0 24px #34d399,0 0 52px rgba(52,211,153,0.9);}}
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

.bot-bubble{background:linear-gradient(135deg,rgba(16,185,129,0.1),rgba(6,182,212,0.07));border:1px solid rgba(52,211,153,0.22);border-radius:1.1rem;padding:0.9rem 1.4rem;text-align:center;backdrop-filter:blur(12px);width:100%;}
.bot-bubble-ttl{font-family:'Inter',sans-serif;font-size:1.1rem;font-weight:700;color:#f0fdf4;letter-spacing:-0.02em;margin-bottom:0.25rem;}
.bot-bubble-sub{font-family:'Inter',sans-serif;font-size:0.82rem;color:#6b7280;line-height:1.6;}
.bot-bubble-sub .hl{color:#34d399;font-weight:500;}

/* ── Logo + headings ──────────────────────────── */
.login-logo{text-align:center;margin-bottom:1.2rem;}
.login-title{font-family:'Inter',sans-serif;font-size:1.5rem;font-weight:700;color:#f0fdf4;letter-spacing:-0.02em;text-align:center;margin-bottom:0.25rem;}
.login-sub{font-family:'Inter',sans-serif;font-size:0.82rem;color:#6b7280;text-align:center;margin-bottom:1.4rem;letter-spacing:0.02em;}

/* ── Form glass card ──────────────────────────── */
[data-testid="stForm"]{background:linear-gradient(135deg,rgba(16,185,129,0.09) 0%,rgba(6,182,212,0.05) 50%,rgba(16,185,129,0.07) 100%)!important;border:1px solid rgba(52,211,153,0.22)!important;border-radius:1.4rem!important;padding:2rem 1.75rem!important;backdrop-filter:blur(28px) saturate(180%)!important;-webkit-backdrop-filter:blur(28px) saturate(180%)!important;box-shadow:0 8px 40px rgba(0,0,0,0.55),inset 0 1px 0 rgba(52,211,153,0.18)!important;position:relative!important;overflow:hidden!important;}
[data-testid="stForm"]::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent 5%,rgba(52,211,153,0.65) 50%,transparent 95%);pointer-events:none;}

/* ── Inputs ───────────────────────────────────── */
.stTextInput>div>div>input{background:rgba(8,18,14,0.75)!important;border:1px solid rgba(52,211,153,0.22)!important;color:#e5e7eb!important;border-radius:0.75rem!important;font-family:'Inter',sans-serif!important;font-size:0.93rem!important;transition:border-color 0.2s,box-shadow 0.2s!important;}
.stTextInput>div>div>input:focus{border-color:rgba(52,211,153,0.55)!important;box-shadow:0 0 0 3px rgba(52,211,153,0.12)!important;}
.stTextInput>div>div>input::placeholder{color:#374151!important;}
.stTextInput label,.stTextInput>label{color:#9ca3af!important;font-family:'Inter',sans-serif!important;font-size:0.82rem!important;font-weight:500!important;letter-spacing:0.03em!important;}

/* ── Submit button ────────────────────────────── */
.stFormSubmitButton>button,[data-testid="stFormSubmitButton"]>button{background:linear-gradient(135deg,#065f46 0%,#0e7490 100%)!important;border:1px solid rgba(52,211,153,0.45)!important;color:#d1fae5!important;border-radius:0.75rem!important;font-weight:600!important;font-size:0.93rem!important;font-family:'Inter',sans-serif!important;letter-spacing:0.04em!important;width:100%!important;box-shadow:0 4px 24px rgba(6,182,212,0.3),inset 0 1px 0 rgba(255,255,255,0.08)!important;transition:all 0.3s ease!important;}
.stFormSubmitButton>button:hover{filter:brightness(1.2)!important;box-shadow:0 8px 32px rgba(16,185,129,0.45)!important;transform:translateY(-1px)!important;}

[data-testid="stAlert"]{background:rgba(10,20,16,0.75)!important;border-color:rgba(52,211,153,0.3)!important;border-radius:0.75rem!important;backdrop-filter:blur(10px)!important;color:#e5e7eb!important;}
</style>""", unsafe_allow_html=True)

# ========== CREDENTIALS ==========
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user":  {"password": "user123",  "role": "user"},
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

if st.session_state.authenticated:
    st.switch_page("pages/1_Home.py")


# ========== LOGO (centered) ==========
logo_path = Path(__file__).parent / "india-bonds-white-logo.png"
_, logo_col, _ = st.columns([1, 3, 1])
with logo_col:
    st.image(str(logo_path), use_container_width=True)

# ========== HEADINGS ==========
st.markdown('<div class="login-title" style="margin-top:1.2rem;">Sign in to your account</div>', unsafe_allow_html=True)
st.markdown('<div class="login-sub">India Bonds AI Automation Platform</div>', unsafe_allow_html=True)

# ========== LOGIN FORM ==========
with st.form("login_form"):
    username = st.text_input("Username", placeholder="Enter username")
    password = st.text_input("Password", type="password", placeholder="Enter password")
    submit = st.form_submit_button("Sign In  →", use_container_width=True, type="primary")

    if submit:
        user = USERS.get(username)
        if user and password == user["password"]:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = user["role"]
            st.success("Login successful! Redirecting...")
            time.sleep(0.8)
            st.rerun()
        else:
            st.error("Invalid username or password")





            
