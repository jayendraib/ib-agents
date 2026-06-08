import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from io import BytesIO

sys.path.append(str(Path(__file__).parent.parent))
from theme import full_css, sidebar_toggle, theme_tokens, glass_css, glass_background_html, role_indicator_html
import ibucc

# ========== AUTH GUARD ==========
if not st.session_state.get("authenticated", False):
    st.switch_page("app.py")

st.set_page_config(
    page_title="IB UCC Compare | India Bonds AI Automation",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>[data-testid="stSidebarNav"] { display: none !important; }</style>
""", unsafe_allow_html=True)


def clear_tool_state():
    for key in ["compare_result", "compare_done", "ib_file_persist",
                "ucc_file_persist", "reset_result", "reset_done", "compare_excel_bytes"]:
        st.session_state.pop(key, None)


# ========== THEME ==========
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

st.markdown(full_css(st.session_state.theme), unsafe_allow_html=True)
st.markdown(glass_css(), unsafe_allow_html=True)
st.markdown(role_indicator_html(st.session_state.get("role", "user")), unsafe_allow_html=True)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    .stApp {
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
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > section,
    [data-testid="stMain"] {
        background: #020c09 !important;
    }
</style>
""", unsafe_allow_html=True)
st.markdown(glass_background_html(), unsafe_allow_html=True)
t = theme_tokens(st.session_state.theme)

_role = st.session_state.get("role", "admin")
_role_label = "ADMIN ACCESS" if _role == "admin" else "USER ACCESS"
_auth_url  = ibucc.QA_AUTH_URL    if _role == "admin" else ibucc.PROD_AUTH_URL
_reset_url = ibucc.QA_RESET_URL   if _role == "admin" else ibucc.PROD_RESET_URL

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] > div:first-child {
                background: rgba(5,15,11,0.97) !important;
                border-right: 1px solid rgba(16,185,129,0.12) !important;
            }
            [data-testid="stSidebarUserContent"] {
                display: flex; flex-direction: column;
                min-height: calc(100vh - 3rem);
            }
            [data-testid="stSidebarUserContent"] > div:has(.sidebar-spacer) { flex: 1; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="padding: 1rem 0;">
            <div style="font-size:1rem; font-weight:700; color:#f9fafb; margin-bottom:0.25rem; font-family:'Inter',sans-serif;">
                👤 {st.session_state.get('username', 'User')}
            </div>
            <div style="font-size:0.72rem; color:#10b981; font-family:'JetBrains Mono',monospace; letter-spacing:0.08em;">
                ● {_role_label}
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)

    if st.button("🏠 Back to Dashboard", use_container_width=True):
        clear_tool_state()
        st.switch_page("pages/1_Home.py")
    if st.button("🚪 Logout", use_container_width=True):
        clear_tool_state()
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

# ========== HEADER ==========
st.markdown("""
    <div style="margin-bottom:1.5rem; position:relative; z-index:2;">
        <div style="display:inline-flex; align-items:center; gap:0.5rem;
                    font-family:'JetBrains Mono',monospace; font-size:0.72rem; font-weight:500;
                    color:#22d3ee; text-transform:uppercase; letter-spacing:0.18em;
                    margin-bottom:0.75rem; padding:0.35rem 1rem;
                    background:rgba(6,182,212,0.08); border:1px solid rgba(6,182,212,0.2);
                    border-radius:9999px; backdrop-filter:blur(8px);">
            <span style="width:6px;height:6px;background:#22d3ee;border-radius:50%;
                         box-shadow:0 0 8px #22d3ee;display:inline-block;"></span>
            PAN RECONCILIATION
        </div>
        <h1 style="margin:0; font-size:2.5rem; font-weight:900; color:#f0fdf4;
                   font-family:'Inter',sans-serif; letter-spacing:-0.03em;">
            🔍 IB UCC <span style="display:inline-block;background:linear-gradient(135deg,#22d3ee,#34d399);
                -webkit-background-clip:text; background-clip:text;
                -webkit-text-fill-color:transparent; color:transparent;">Compare</span>
        </h1>
        <p style="color:#6b7280; margin-top:0.5rem; font-size:0.95rem;">
            Upload IB &amp; UCC files → Compare PANs → Find missing records → Auto-reset UCC status
        </p>
    </div>
""", unsafe_allow_html=True)

# ========== STATIC CONFIG ==========
IB_COLUMN = "PAN"
UCC_COLUMN = "PAN No."
IB_CLIENT_ID_COLUMN = "Client ID"

# ========== SESSION STATE ==========
for key, default in [
    ("compare_result", None),
    ("compare_done", False),
    ("reset_result", None),
    ("reset_done", False),
    ("compare_excel_bytes", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ========== TABS ==========
tab_upload, tab_results = st.tabs(["📤 Upload & Compare", "📋 Results"])

# ==================== TAB 1: UPLOAD ====================
with tab_upload:
    st.markdown('<div class="section-title">Step 1 — Upload Files</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        ib_file = st.file_uploader(
            "📄 Upload IB File",
            type=["xlsx", "xls", "csv"],
            key="ib_uploader",
            help="Must contain 'RegistrationCode' and 'PAN' columns"
        )
    with col2:
        ucc_file = st.file_uploader(
            "📄 Upload UCC File",
            type=["xlsx", "xls", "csv"],
            key="ucc_uploader",
            help="Must contain 'PAN No.' column"
        )

    st.markdown('<div class="section-title">Step 2 — Configuration (Fixed)</div>', unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        st.markdown(f"""
            <div class="param-box">
                <div class="param-label">IB Column</div>
                <div class="param-value">{IB_COLUMN}</div>
            </div>
        """, unsafe_allow_html=True)
    with pc2:
        st.markdown(f"""
            <div class="param-box">
                <div class="param-label">UCC Column</div>
                <div class="param-value">{UCC_COLUMN}</div>
            </div>
        """, unsafe_allow_html=True)
    with pc3:
        st.markdown(f"""
            <div class="param-box">
                <div class="param-label">IB Client ID Column</div>
                <div class="param-value">{IB_CLIENT_ID_COLUMN}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Step 3 — Run Comparison</div>', unsafe_allow_html=True)

    compare_disabled = ib_file is None or ucc_file is None
    if st.button("🔍 Compare PANs", type="primary", use_container_width=True, disabled=compare_disabled):
        st.session_state.reset_result = None
        st.session_state.reset_done = False
        st.session_state.compare_excel_bytes = None

        with st.spinner("⏳ Comparing PANs... Please wait"):
            try:
                result = ibucc.compare_pans(
                    ib_file=ib_file,
                    ucc_file=ucc_file,
                    ib_column=IB_COLUMN,
                    ucc_column=UCC_COLUMN,
                    ib_client_id_column=IB_CLIENT_ID_COLUMN
                )
                st.session_state.compare_result = result
                st.session_state.compare_done = True

                if result and result.get("success") and result.get("data"):
                    buf = BytesIO()
                    pd.DataFrame(result["data"]).to_excel(buf, index=False, engine="openpyxl")
                    buf.seek(0)
                    st.session_state.compare_excel_bytes = buf.getvalue()

                if result and result.get("success"):
                    st.success("✅ Comparison completed successfully!")
                else:
                    st.error(f"❌ {result.get('error', 'Comparison failed')}")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.compare_done = False

    # ── Step 4: Download missing PANs (appears after comparison) ────
    if (
        st.session_state.compare_done
        and st.session_state.compare_result
        and st.session_state.compare_result.get("success")
        and st.session_state.get("compare_excel_bytes")
    ):
        result = st.session_state.compare_result
        missing_count = len(result.get("data", []))
        stats = result.get("stats", {})

        st.markdown('<div class="section-title">Step 4 — Download Missing PANs</div>', unsafe_allow_html=True)
        st.markdown('<div class="download-box">', unsafe_allow_html=True)
        dl_col, info_col = st.columns([1, 2])

        with dl_col:
            st.download_button(
                label="📥 Download Missing PANs (.xlsx)",
                data=st.session_state.compare_excel_bytes,
                file_name="missing_pans.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary",
                key="dl_missing_upload_tab"   # ← unique key
            )
        with info_col:
            st.markdown(f"""
                <p style="font-weight:600; color:{t['dl_txt']};">✅ File ready!</p>
                <p style="color:{t['dl_sub']}; font-size:0.9rem;">
                    Missing PANs: <b>{missing_count}</b> &nbsp;|&nbsp;
                    Total checked: <b>{stats.get('total_checked', 0)}</b>
                </p>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Step 5: Reset UCC Status ────────────────────────────────────
    if (
        st.session_state.compare_done
        and st.session_state.compare_result
        and st.session_state.compare_result.get("success")
        and st.session_state.compare_result.get("data")
    ):
        st.markdown('<div class="section-title">Step 5 — Reset UCC Status</div>', unsafe_allow_html=True)
        missing_count = len(st.session_state.compare_result["data"])
        st.info(f"⚠️ {missing_count} missing PAN(s) found. Click below to reset their UCC status via external API.")

        if st.button("🔄 Reset UCC Status for Missing Records", type="primary", use_container_width=True):
            with st.spinner("⏳ Calling ResetUCCStatusToPending API... Please wait"):
                try:
                    reset_result = ibucc.reset_ucc_for_missing(
                        st.session_state.compare_result["data"],
                        auth_url=_auth_url,
                        reset_url=_reset_url
                    )
                    st.session_state.reset_result = reset_result
                    st.session_state.reset_done = True

                    if reset_result and reset_result.get("success"):
                        st.success("✅ UCC Reset API call completed successfully!")
                    else:
                        st.error(f"❌ API Error: {reset_result.get('error', 'Reset failed')}")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.reset_done = False

# ==================== TAB 2: RESULTS ====================
with tab_results:
    st.markdown('<div class="section-title">Comparison Results</div>', unsafe_allow_html=True)

    if not st.session_state.compare_done:
        st.info("👆 Go to 'Upload & Compare', upload both files, and click 'Compare PANs' to see results.")
    else:
        result = st.session_state.compare_result

        if result and result.get("success"):
            st.markdown(f"""
                <div class="success-banner">
                    <span style="font-size:1.2rem; font-weight:600; color:{t['success_txt']};">✅ Comparison Successful</span>
                </div>
            """, unsafe_allow_html=True)

            # ── Stats ────────────────────────────────────────────────
            stats = result.get("stats", {})
            total_checked = stats.get("total_checked", 0)
            total_found   = stats.get("total_found", 0)
            total_missing = stats.get("total_missing", 0)

            s1, s2, s3 = st.columns(3)
            with s1:
                st.markdown(f"""
                    <div class="stat-box" style="background:{t['stat_neutral_bg']};">
                        <div class="stat-number" style="color:{t['stat_neutral_txt']};">{total_checked}</div>
                        <div class="stat-label">Total Checked</div>
                    </div>
                """, unsafe_allow_html=True)
            with s2:
                st.markdown(f"""
                    <div class="stat-box" style="background:{t['stat_green_bg']};">
                        <div class="stat-number" style="color:{t['stat_green_txt']};">{total_found}</div>
                        <div class="stat-label">Found in UCC</div>
                    </div>
                """, unsafe_allow_html=True)
            with s3:
                st.markdown(f"""
                    <div class="stat-box" style="background:{t['stat_red_bg']};">
                        <div class="stat-number" style="color:{t['stat_red_txt']};">{total_missing}</div>
                        <div class="stat-label">Missing PANs</div>
                    </div>
                """, unsafe_allow_html=True)

            st.divider()

            # ── Download (also in results tab) ───────────────────────
            if st.session_state.get("compare_excel_bytes") and total_missing > 0:
                st.markdown('<div class="download-box">', unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Missing PANs (.xlsx)",
                    data=st.session_state.compare_excel_bytes,
                    file_name="missing_pans.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    type="primary",
                    key="dl_missing_results_tab"   # ← unique key (different from upload tab)
                )
                st.markdown('</div>', unsafe_allow_html=True)
            elif total_missing == 0:
                st.success("🎉 All PANs found! No missing records.")

            st.divider()

            # ── Reset API result ─────────────────────────────────────
            if st.session_state.reset_done and st.session_state.reset_result:
                ext = st.session_state.reset_result
                st.markdown("### 🔌 Reset UCC Status — API Result")

                api_success      = ext.get("success", False)
                status_code      = ext.get("resetApiStatusCode", "N/A")
                reset_resp       = ext.get("resetApiResponse") or {}
                if not isinstance(reset_resp, dict):
                    reset_resp = {}
                processed        = reset_resp.get("processed", 0)
                failed           = reset_resp.get("failed", [])
                clients_processed = ext.get("clientsProcessed", 0)

                card_cls   = "api-success" if api_success else "api-fail"
                icon       = "✅" if api_success else "❌"
                badge_bg   = t["api_ok_badge_bg"]  if api_success else t["api_fail_badge_bg"]
                badge_txt  = t["api_ok_badge_txt"] if api_success else t["api_fail_badge_txt"]
                proc_color = t["api_ok_badge_txt"] if api_success else t["api_fail_badge_txt"]

                st.markdown(f"""
                    <div class="api-card {card_cls}">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                            <span style="font-weight:600; font-size:1.1rem; color:{t['api_val']};">
                                {icon} Reset UCC Status API
                            </span>
                            <span style="background:{badge_bg}; color:{badge_txt}; padding:4px 12px; border-radius:20px; font-size:0.85rem; font-weight:600;">
                                HTTP {status_code}
                            </span>
                        </div>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
                            <div>
                                <div style="font-size:0.85rem; color:{t['api_label']};">Clients Processed</div>
                                <div style="font-size:1.25rem; font-weight:700; color:{t['api_val']};">{clients_processed}</div>
                            </div>
                            <div>
                                <div style="font-size:0.85rem; color:{t['api_label']};">Processed Successfully</div>
                                <div style="font-size:1.25rem; font-weight:700; color:{proc_color};">{processed}</div>
                            </div>
                        </div>
                        {f'<div style="margin-top:0.75rem; color:{t["stat_red_txt"]}; font-size:0.9rem;">Failed: {len(failed)} record(s)</div>' if failed else ''}
                    </div>
                """, unsafe_allow_html=True)

            elif total_missing > 0 and not st.session_state.reset_done:
                st.info("⬆️ Go to 'Upload & Compare' → Step 5 to trigger the UCC reset API.")

        else:
            err_msg = result.get("error", "Unknown error") if result else "No result"
            st.markdown(f"""
                <div class="fail-banner">
                    <span style="font-size:1.2rem; font-weight:600; color:{t['error_txt']};">❌ Comparison Failed</span>
                    <p style="margin:0.5rem 0 0 0; color:{t['error_txt']}; opacity:0.8;">{err_msg}</p>
                </div>
            """, unsafe_allow_html=True)
