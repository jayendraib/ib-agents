import streamlit as st
import pandas as pd
import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime
from io import BytesIO

sys.path.append(str(Path(__file__).parent.parent))
from theme import full_css, sidebar_toggle, theme_tokens, glass_css, glass_background_html, role_indicator_html
import debarred as debarred_mod
from debarred import run_pipeline

# ========== AUTH GUARD ==========
if not st.session_state.get("authenticated", False):
    st.switch_page("app.py")

st.set_page_config(
    page_title="SEBI Debarred | Tool",
    page_icon="📊",
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

# ========== ROLE / URL ==========
_role = st.session_state.get("role", "admin")
_api_url = debarred_mod.QA_API_URL   if _role == "admin" else debarred_mod.PROD_API_URL
_api_key = debarred_mod.QA_API_KEY   if _role == "admin" else debarred_mod.PROD_API_KEY
_role_label = "ADMIN ACCESS" if _role == "admin" else "USER ACCESS"

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

    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("pages/1_Home.py")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

# ========== HEADER ==========
st.markdown("""
    <div class="glass-theme" style="margin-bottom:1.5rem; position:relative; z-index:2;">
        <div style="display:inline-flex; align-items:center; gap:0.5rem;
                    font-family:'JetBrains Mono',monospace; font-size:0.72rem; font-weight:500;
                    color:#34d399; text-transform:uppercase; letter-spacing:0.18em;
                    margin-bottom:0.75rem; padding:0.35rem 1rem;
                    background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);
                    border-radius:9999px; backdrop-filter:blur(8px);">
            <span style="width:6px;height:6px;background:#34d399;border-radius:50%;
                         box-shadow:0 0 8px #34d399;display:inline-block;"></span>
            SEBI AUTOMATION
        </div>
        <h1 style="margin:0; font-size:2.5rem; font-weight:900; color:#f0fdf4;
                   font-family:'Inter',sans-serif; letter-spacing:-0.03em;">
            📊 SEBI Debarred <span style="display:inline-block;background:linear-gradient(135deg,#34d399,#22d3ee);
                -webkit-background-clip:text; background-clip:text;
                -webkit-text-fill-color:transparent; color:transparent;">Tool</span>
        </h1>
        <p style="color:#6b7280; margin-top:0.5rem; font-size:0.95rem;">
            Upload your data files → Pipeline processes → Download master table
        </p>
    </div>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
for key, default in [
    ("uploaded_files", []),
    ("pipeline_result", None),
    ("processing_done", False),
    ("master_df", None),
    ("excel_bytes", None),
    ("processed_at", None),
    ("pan_fix_stopped", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ========== TABS ==========
tab_upload, tab_summary = st.tabs(["📤 Upload & Process", "📋 Summary"])

# ==================== TAB 1: UPLOAD & PROCESS ====================
with tab_upload:
    st.markdown('<div class="section-title">Step 1 — Upload Files</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop your files here (Excel, ZIP, or CSV)",
        type=["xlsx", "xls", "zip", "csv"],
        accept_multiple_files=True,
        help="Upload Excel files, ZIP archives, or CSV files."
    )

    if uploaded:
        st.session_state.uploaded_files = uploaded
        st.success(f"✅ {len(uploaded)} file(s) ready for processing")
        for f in uploaded:
            st.caption(f"📄 {f.name} ({f.size/1024:.1f} KB)")

    st.markdown('<div class="section-title">Step 2 — Run Pipeline</div>', unsafe_allow_html=True)

    proceed_disabled = len(st.session_state.uploaded_files) == 0
    if st.button("🚀 Proceed to Pipeline", type="primary", use_container_width=True, disabled=proceed_disabled):

        with tempfile.TemporaryDirectory() as tmpdir:
            for uploaded_file in st.session_state.uploaded_files:
                file_path = os.path.join(tmpdir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

            output_dir = os.path.join(tmpdir, "outputs")
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, "SEBIDebarred_Format.xlsx")

            with st.spinner("⏳ Processing through pipeline... Please wait"):
                try:
                    st.session_state.pan_fix_stopped = False
                    result = run_pipeline(paths=[tmpdir], output_path=output_file, api_url=_api_url, api_key=_api_key)

                    st.session_state.pipeline_result = result
                    st.session_state.processing_done = True
                    st.session_state.processed_at = datetime.now().strftime("%H:%M:%S")

                    if os.path.exists(output_file):
                        st.session_state.master_df = pd.read_excel(output_file)
                        with open(output_file, "rb") as f:
                            st.session_state.excel_bytes = f.read()
                    else:
                        st.session_state.master_df = None
                        st.session_state.excel_bytes = None

                    st.success("✅ Pipeline completed successfully!")

                except Exception as e:
                    st.error(f"❌ Pipeline failed: {str(e)}")
                    st.session_state.processing_done = False

    # ── Step 3: Download (appears after successful run) ─────────────
    if st.session_state.processing_done and st.session_state.get("excel_bytes"):
        st.markdown('<div class="section-title">Step 3 — Download Output</div>', unsafe_allow_html=True)

        df = st.session_state.master_df
        total_rows = len(df) if df is not None else 0

        st.markdown('<div class="download-box">', unsafe_allow_html=True)
        dl_col, info_col = st.columns([1, 2])

        with dl_col:
            st.download_button(
                label="📥 Download Master Table (.xlsx)",
                data=st.session_state.excel_bytes,
                file_name="SEBIDebarred_Format.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary",
                key="dl_master_upload_tab"
            )
        with info_col:
            st.markdown(f"""
                <p style="font-weight:600; color:{t['dl_txt']};">✅ File is ready!</p>
                <p style="color:{t['dl_sub']}; font-size:0.9rem;">
                    Total rows: <b>{total_rows}</b> &nbsp;|&nbsp; Generated at: <b>{st.session_state.processed_at}</b>
                </p>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Step 4: Handle invalid PANs (only if errors exist) ──────
        result = st.session_state.pipeline_result
        if result and result.get("needs_filter") and result.get("error_file"):
            st.markdown('<div class="section-title">Step 4 — Handle Invalid PANs</div>', unsafe_allow_html=True)
            err_count = len(result.get("errors", []))
            st.error(f"⚠️ {err_count} invalid PAN(s) detected.")

            ec1, ec2, ec3 = st.columns([1, 1, 2])
            with ec1:
                st.download_button(
                    "📥 Download Error File",
                    data=result["error_file"],
                    file_name="SEBIDebarred_Format_Errors.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="dl_error_file"
                )
            if not st.session_state.pan_fix_stopped:
                with ec2:
                    if st.button("✅ Remove Invalid & Re-upload", type="primary", use_container_width=True):
                        with st.spinner("Filtering and re-uploading..."):
                            from debarred import filter_and_reupload
                            final = filter_and_reupload(result["error_file"], api_url=_api_url, api_key=_api_key)
                            if final["final_status"] == "OK":
                                st.success(f"✅ {final['final_message']} — Removed {final['removed_count']} invalid PAN(s)")
                                st.download_button(
                                    "📥 Download Clean File",
                                    data=final["clean_bytes"],
                                    file_name="SEBIDebarred_Format.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key="dl_clean_file"
                                )
                            else:
                                st.error(f"❌ Re-upload failed: {final['final_message']}")
                with ec3:
                    if st.button("❌ Stop Here", use_container_width=True):
                        st.session_state.pan_fix_stopped = True
                        st.rerun()
            else:
                with ec2:
                    st.warning("⛔ Stopped. Fix invalid PANs manually and re-upload.")

# ==================== TAB 2: SUMMARY ====================
with tab_summary:
    st.markdown('<div class="section-title">Pipeline Summary</div>', unsafe_allow_html=True)

    if not st.session_state.processing_done:
        st.info("👆 Go to 'Upload & Process', upload files, and run the pipeline to see the summary here.")
    else:
        result = st.session_state.pipeline_result
        df = st.session_state.master_df

        # ── Metrics ─────────────────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Rows",    len(df) if df is not None else 0)
        c2.metric("Total Columns", len(df.columns) if df is not None else 0)
        c3.metric("PAN Column",    "✅ Found" if df is not None and "PAN No" in df.columns else "N/A")
        c4.metric("Processed At",  st.session_state.processed_at or "—")

        st.divider()

        # ── Status summary card ──────────────────────────────────────
        if result:
            api_status  = result.get("api_status", "—")
            api_message = result.get("api_message", "—")
            errors      = result.get("errors", [])
            has_errors  = result.get("needs_filter", False)

            status_tag = (
                f'<span class="status-ok">✅ OK</span>'
                if api_status == "OK"
                else f'<span class="status-err">❌ {api_status}</span>'
            )

            st.markdown(f"""
                <div class="summary-card">
                    <div class="stat-row">
                        <span class="stat-key">API Status</span>
                        <span class="stat-val">{status_tag}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-key">Message</span>
                        <span class="stat-val">{api_message}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-key">Invalid PANs</span>
                        <span class="stat-val">{len(errors) if has_errors else 0}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-key">Output File</span>
                        <span class="stat-val">SEBIDebarred_Format.xlsx</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ── Download button in summary tab ───────────────────────────
        if st.session_state.get("excel_bytes"):
            st.markdown('<div class="download-box">', unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Master Table (.xlsx)",
                data=st.session_state.excel_bytes,
                file_name="SEBIDebarred_Format.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary",
                key="dl_master_summary_tab"
            )
            st.markdown('</div>', unsafe_allow_html=True)
