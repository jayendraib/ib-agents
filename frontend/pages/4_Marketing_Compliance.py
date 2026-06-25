import streamlit as st
import sys
import os
import tempfile
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from theme import full_css, theme_tokens, glass_css, glass_background_html, role_indicator_html
import marketing as marketing_mod
from marketing import evaluate_script, read_script_file, report_to_json, Severity, Verdict

# ========== AUTH GUARD ==========
if not st.session_state.get("authenticated", False):
    st.switch_page("app.py")

st.set_page_config(
    page_title="OBPP Compliance | India Bonds AI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
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
    /* ── Verdict badges ── */
    .verdict-compliant {
        display:inline-block; padding:0.45rem 1.25rem; border-radius:9999px;
        background:rgba(16,185,129,0.15); border:1px solid rgba(52,211,153,0.45);
        color:#34d399; font-weight:700; font-size:0.95rem; letter-spacing:0.03em;
    }
    .verdict-noncompliant {
        display:inline-block; padding:0.45rem 1.25rem; border-radius:9999px;
        background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.4);
        color:#f87171; font-weight:700; font-size:0.95rem; letter-spacing:0.03em;
    }
    .verdict-exempt {
        display:inline-block; padding:0.45rem 1.25rem; border-radius:9999px;
        background:rgba(6,182,212,0.12); border:1px solid rgba(6,182,212,0.4);
        color:#22d3ee; font-weight:700; font-size:0.95rem; letter-spacing:0.03em;
    }

    /* ── Severity chips ── */
    .sev-critical { color:#f87171; background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.3); }
    .sev-high     { color:#fb923c; background:rgba(249,115,22,0.12); border:1px solid rgba(249,115,22,0.3); }
    .sev-medium   { color:#fbbf24; background:rgba(251,191,36,0.12); border:1px solid rgba(251,191,36,0.3); }
    .sev-low      { color:#a3e635; background:rgba(163,230,53,0.1);  border:1px solid rgba(163,230,53,0.25);}
    .sev-chip {
        display:inline-block; padding:0.2rem 0.6rem; border-radius:0.4rem;
        font-family:'JetBrains Mono',monospace; font-size:0.7rem; font-weight:700;
        letter-spacing:0.06em;
    }

    /* ── Violation card ── */
    .violation-card {
        background:rgba(10,20,16,0.6); border:1px solid rgba(239,68,68,0.18);
        border-left:3px solid rgba(239,68,68,0.55); border-radius:0.75rem;
        padding:1rem 1.25rem; margin-bottom:0.75rem;
    }
    .violation-rule { font-size:0.8rem; color:#9ca3af; font-family:'JetBrains Mono',monospace; margin-bottom:0.3rem; }
    .violation-msg  { font-size:0.95rem; color:#f9fafb; font-weight:600; margin-bottom:0.5rem; }
    .violation-found { font-size:0.82rem; color:#f87171; font-style:italic; margin-bottom:0.5rem; }
    .violation-fix  { font-size:0.85rem; color:#6ee7b7; }

    /* ── Score ring (CSS-only) ── */
    .score-block {
        display:flex; align-items:center; gap:1.5rem;
        background:rgba(10,20,16,0.55); border:1px solid rgba(16,185,129,0.15);
        border-radius:1rem; padding:1.25rem 1.5rem; margin-bottom:1.25rem;
    }
    .score-number {
        font-size:3rem; font-weight:900; font-family:'Inter',sans-serif;
        background:linear-gradient(135deg,#34d399,#22d3ee);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        background-clip:text; line-height:1;
    }
    .score-label { font-size:0.72rem; color:#6b7280; font-family:'JetBrains Mono',monospace;
                   text-transform:uppercase; letter-spacing:0.12em; margin-top:0.25rem; }

    /* ── Passed rule pill ── */
    .passed-pill {
        display:inline-block; margin:0.2rem 0.3rem 0.2rem 0;
        padding:0.2rem 0.75rem; border-radius:9999px;
        background:rgba(16,185,129,0.08); border:1px solid rgba(52,211,153,0.2);
        color:#6ee7b7; font-size:0.78rem; font-family:'JetBrains Mono',monospace;
    }

    .stDeployButton, footer { display:none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(glass_background_html(), unsafe_allow_html=True)
t = theme_tokens(st.session_state.theme)

# ========== TEMP FILE HELPERS ==========
def _save_upload_to_temp(uploaded_file) -> str:
    """Save an uploaded file to a named temp file; return its path."""
    suffix = Path(uploaded_file.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        return tmp.name

def _cleanup_temp():
    """Delete the temp file tracked in session state, if it exists."""
    path = st.session_state.get("marketing_tmp_path")
    if path:
        try:
            if os.path.exists(path):
                os.unlink(path)
        except Exception:
            pass
        st.session_state.marketing_tmp_path = None
        st.session_state.marketing_tmp_name = None

# ========== SESSION STATE ==========
for key, default in [
    ("compliance_report",  None),
    ("compliance_done",    False),
    ("compliance_json",    None),
    ("marketing_tmp_path", None),
    ("marketing_tmp_name", None),
    ("compliance_logs",    []),
    ("uploader_key",       0),
]:
    if key not in st.session_state:
        st.session_state[key] = default

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
        <div style="padding:1rem 0;">
            <div style="font-size:1rem; font-weight:700; color:#f9fafb; margin-bottom:0.25rem; font-family:'Inter',sans-serif;">
                👤 {st.session_state.get('username', 'User')}
            </div>
            <div style="font-size:0.72rem; color:#10b981; font-family:'JetBrains Mono',monospace; letter-spacing:0.08em;">
                ● {"ADMIN ACCESS" if st.session_state.get("role") == "admin" else "USER ACCESS"}
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)

    if st.button("🏠 Back to Home", use_container_width=True):
        _cleanup_temp()
        st.switch_page("pages/1_Home.py")

    if st.button("🚪 Logout", use_container_width=True):
        _cleanup_temp()
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

# ========== HEADER ==========
st.markdown("""
    <div style="margin-bottom:1.5rem; position:relative; z-index:2;">
        <div style="display:inline-flex; align-items:center; gap:0.5rem;
                    font-family:'JetBrains Mono',monospace; font-size:0.72rem; font-weight:500;
                    color:#34d399; text-transform:uppercase; letter-spacing:0.18em;
                    margin-bottom:0.75rem; padding:0.35rem 1rem;
                    background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);
                    border-radius:9999px; backdrop-filter:blur(8px);">
            <span style="width:6px;height:6px;background:#34d399;border-radius:50%;
                         box-shadow:0 0 8px #34d399;display:inline-block;"></span>
            SEBI OBPP
        </div>
        <h1 style="margin:0; font-size:2.5rem; font-weight:900; color:#f0fdf4;
                   font-family:'Inter',sans-serif; letter-spacing:-0.03em;">
            📋 Marketing <span style="background:linear-gradient(135deg,#34d399,#22d3ee);
                -webkit-background-clip:text; background-clip:text;
                -webkit-text-fill-color:transparent;">Compliance</span>
        </h1>
        <p style="color:#6b7280; margin-top:0.5rem; font-size:0.95rem;">
            Upload your marketing script → AI evaluates against SEBI OBPP Advertisement Code
        </p>
    </div>
""", unsafe_allow_html=True)

# ========== RULEBOOK STATUS ==========
rulebook_ok = Path(marketing_mod.RULEBOOK_PATH).exists()
if not rulebook_ok:
    st.error(
        f"Rulebook not found at `{marketing_mod.RULEBOOK_PATH}`. "
        "Set the `OBPP_RULEBOOK_PATH` environment variable to point to your Advertisement Code file."
    )
    st.stop()

# ========== TABS ==========
tab_upload, tab_report = st.tabs(["📤 Upload & Evaluate", "📊 Report"])

# ==================== TAB 1: UPLOAD ====================
with tab_upload:
    st.markdown('<div class="section-title">Step 1 — Upload Script</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop your marketing script here",
        type=["txt", "md", "docx", "pdf"],
        help="Supported formats: .txt, .md, .docx, .pdf",
        key=f"script_upload_{st.session_state.uploader_key}",
    )

    if uploaded:
        if st.session_state.get("marketing_tmp_name") != uploaded.name:
            _cleanup_temp()
            tmp_path = _save_upload_to_temp(uploaded)
            st.session_state.marketing_tmp_path = tmp_path
            st.session_state.marketing_tmp_name = uploaded.name
        st.success(f"✅ {uploaded.name} ({uploaded.size / 1024:.1f} KB) ready")
    else:
        if st.session_state.get("marketing_tmp_path"):
            _cleanup_temp()

    st.markdown("")
    run_disabled = st.session_state.get("marketing_tmp_path") is None
    if st.button("🚀 Run Compliance Check", type="primary", use_container_width=True, disabled=run_disabled):
        tmp_path = st.session_state.marketing_tmp_path
        #logs: list = []
        #st.session_state.compliance_logs = logs
        #st.session_state.compliance_done = False

        log_box = st.empty()

        #def _log(msg: str):
            #logs.append(msg)
            #log_box.code("\n".join(logs), language=None)

        try:
            #_log(f"Reading file: {st.session_state.marketing_tmp_name}")
            script_text = read_script_file(tmp_path)
            #_log(f"File read OK — {len(script_text)} chars extracted.")

            #_log("Loading SEBI OBPP rulebook...")
            report = evaluate_script(
                script_text=script_text,
                #log_callback=_log,
            )
            st.session_state.compliance_report = report
            st.session_state.compliance_json   = report_to_json(report)
            st.session_state.compliance_done   = True
            #_log(f"Done. Verdict: {report.verdict.value} | Score: {report.score:.0f}/100 | Violations: {len(report.violations)}")

            # Reset uploader so user can easily run another file
            _cleanup_temp()
            st.session_state.uploader_key += 1

        except Exception as e:
            import traceback
            err_detail = traceback.format_exc()
            #_log(f"❌ FATAL ERROR: {type(e).__name__}: {e}")
            #_log(err_detail)
            st.error(f"❌ Evaluation failed: {e}")
            st.session_state.compliance_done = False

        if st.session_state.compliance_done:
            st.success("✅ Evaluation complete! See the Report tab.")

    # Show logs from last run (persists across rerenders)
    # if st.session_state.compliance_logs:
    #     with st.expander("📋 Evaluation Logs", expanded=not st.session_state.compliance_done):
    #         st.code("\n".join(st.session_state.compliance_logs), language=None)

# ==================== TAB 2: REPORT ====================
with tab_report:
    if not st.session_state.compliance_done:
        st.info("👆 Go to 'Upload & Evaluate', upload a script, and run the check to see the report here.")
        st.stop()

    report = st.session_state.compliance_report

    # ── Verdict + Score ──────────────────────────────────────────────
    verdict_class = {
        Verdict.COMPLIANT:     "verdict-compliant",
        Verdict.NON_COMPLIANT: "verdict-noncompliant",
        Verdict.EXEMPT:        "verdict-exempt",
    }.get(report.verdict, "verdict-compliant")

    st.markdown(
        f'<div class="{verdict_class}">{report.verdict.value}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    st.markdown(f"""
        <div class="score-block">
            <div>
                <div class="score-number">{report.score:.0f}</div>
                <div class="score-label">/ 100 score</div>
            </div>
            <div style="color:#9ca3af; font-size:0.9rem; line-height:1.7;">{report.summary}</div>
        </div>
    """, unsafe_allow_html=True)

    # ── Violations ───────────────────────────────────────────────────
    if report.violations:
        st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; font-weight:600;
                        color:#9ca3af; text-transform:uppercase; letter-spacing:0.15em;
                        margin:1.5rem 0 0.75rem; padding-bottom:0.5rem;
                        border-bottom:1px solid rgba(239,68,68,0.2);">
                Violations ({len(report.violations)})
            </div>
        """, unsafe_allow_html=True)

        sev_order = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]
        sev_css   = {
            Severity.CRITICAL: "sev-critical",
            Severity.HIGH:     "sev-high",
            Severity.MEDIUM:   "sev-medium",
            Severity.LOW:      "sev-low",
        }

        for sev in sev_order:
            group = [v for v in report.violations if v.severity == sev]
            for v in group:
                st.markdown(f"""
                    <div class="violation-card">
                        <div class="violation-rule">
                            <span class="sev-chip {sev_css[sev]}">{v.severity.value}</span>
                            &nbsp; Rule {v.rule_id} — {v.rule_name}
                        </div>
                        <div class="violation-msg">{v.message}</div>
                        <div class="violation-found">Found: &ldquo;{v.found_text}&rdquo;</div>
                        <div class="violation-fix">💡 {v.suggestion}</div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="color:#34d399; font-size:0.95rem; padding:1rem 0;">
                ✅ No violations found across all rulebook sections.
            </div>
        """, unsafe_allow_html=True)

    # ── Passed Rules ─────────────────────────────────────────────────
    if report.passed:
        st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; font-weight:600;
                        color:#9ca3af; text-transform:uppercase; letter-spacing:0.15em;
                        margin:1.5rem 0 0.75rem; padding-bottom:0.5rem;
                        border-bottom:1px solid rgba(52,211,153,0.15);">
                Passed ({len(report.passed)})
            </div>
        """, unsafe_allow_html=True)
        pills = "".join(f'<span class="passed-pill">{p}</span>' for p in sorted(report.passed))
        st.markdown(f'<div style="line-height:2.2;">{pills}</div>', unsafe_allow_html=True)

    # ── Export ───────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    st.download_button(
        label     = "📥 Download Report (JSON)",
        data      = st.session_state.compliance_json,
        file_name = "compliance_report.json",
        mime      = "application/json",
        use_container_width=True,
    )
