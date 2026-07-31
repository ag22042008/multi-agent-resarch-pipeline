"""
Inkling — UI for the multi-agent research pipeline.

Drop this file (app.py) in the same folder as main_pipeline.py, agents.py,
tools.py, .env, etc. Then run:

    streamlit run app.py
"""

import traceback

import streamlit as st

from main_pipeline import run_resarch_pipeline

# ----------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Inkling — Research Pipeline",
    page_icon="🖋️",
    layout="wide",
)

# ----------------------------------------------------------------------
# Style — one deep ink-plum theme, top to bottom. No white anywhere:
# text is warm ivory, panels are shades of plum, the only accent is a
# lit-candle amber. Every Streamlit element gets an explicit color so
# nothing can inherit a theme default and go invisible.
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');

    :root {
        --bg: #16132B;
        --panel: #1E1938;
        --panel-alt: #241F44;
        --code-bg: #100D22;
        --text: #F1EDE4;
        --muted: #A79FC2;
        --accent: #E8A33D;
        --accent-soft: rgba(232, 163, 61, 0.16);
        --border: rgba(241, 237, 228, 0.12);
    }

    /* ---- blanket reset so nothing can render invisible ---- */
    .stApp, .stApp * { color: var(--text) !important; }
    .stApp { background: var(--bg) !important; }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    ::selection { background: var(--accent-soft); }

    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--panel-alt); border-radius: 6px; }

    h1, h2, h3 { font-family: 'Fraunces', serif !important; letter-spacing: -0.01em; }
    hr { border-color: var(--border) !important; }

    /* ---- rail (first column) ---- */
    [data-testid="stColumn"]:nth-of-type(1) {
        background: radial-gradient(120% 90% at 20% 0%, var(--panel-alt) 0%, var(--panel) 60%);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.8rem 1.4rem;
        min-height: 560px;
    }
    [data-testid="stColumn"]:nth-of-type(1) [data-testid="stButton"] button {
        background: transparent !important;
        border: 1px solid var(--border) !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        padding: 0.35rem 0.7rem !important;
        text-align: left !important;
    }
    [data-testid="stColumn"]:nth-of-type(1) [data-testid="stButton"] button:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }

    /* ---- canvas (second column) ---- */
    [data-testid="stColumn"]:nth-of-type(2) {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 2rem 2.2rem;
    }

    .brand-mark { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.2rem; }
    .brand-name { font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.5rem !important; }
    .brand-tag { font-size: 0.8rem !important; color: var(--muted) !important; margin: 0 0 1.6rem; }
    .logo-glow { filter: drop-shadow(0 0 6px rgba(232,163,61,0.55)); animation: pulse 2.6s ease-in-out infinite; }
    @keyframes pulse { 0%, 100% { opacity: 0.85; } 50% { opacity: 1; } }

    .rail-label {
        font-family: 'JetBrains Mono', monospace; font-size: 0.68rem !important;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: var(--muted) !important; margin: 1.4rem 0 0.8rem;
    }

    .vstep { display: flex; gap: 0.7rem; align-items: flex-start; margin-bottom: 0.55rem; position: relative; }
    .vstep:not(:first-child)::before {
        content: ""; position: absolute; top: -18px; left: 12px; width: 2px; height: 18px;
        background: repeating-linear-gradient(180deg, var(--accent) 0 4px, transparent 4px 8px);
        background-size: 2px 16px; animation: flow 0.8s linear infinite;
    }
    @media (prefers-reduced-motion: reduce) {
        .vstep:not(:first-child)::before, .logo-glow { animation: none !important; }
    }
    @keyframes flow { from { background-position: 0 0; } to { background-position: 0 16px; } }
    .vstep .num {
        flex-shrink: 0; width: 26px; height: 26px; border-radius: 50%;
        border: 1.5px solid var(--accent); color: var(--accent) !important;
        display: flex; align-items: center; justify-content: center;
        font-family: 'JetBrains Mono', monospace; font-size: 0.7rem !important; font-weight: 600;
        background: var(--panel); position: relative; z-index: 1;
    }
    .vstep .txt .t { font-weight: 600; font-size: 0.88rem !important; }
    .vstep .txt .d { font-size: 0.76rem !important; color: var(--muted) !important; }

    .eyebrow {
        font-family: 'JetBrains Mono', monospace; font-size: 0.72rem !important;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: var(--accent) !important; margin-bottom: 0.3rem;
    }
    .subtitle { color: var(--muted) !important; font-size: 1rem !important; margin: -0.4rem 0 1.4rem; }

    .badge {
        display: inline-block; font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem !important; letter-spacing: 0.08em; text-transform: uppercase;
        color: var(--accent) !important; background: var(--accent-soft);
        border-radius: 999px; padding: 0.25rem 0.7rem; margin-bottom: 0.7rem;
    }

    /* ---- inputs, buttons, alerts, code, expanders — explicit, theme-proof ---- */
    [data-testid="stTextInput"] input {
        border-radius: 8px !important; border: 1px solid var(--border) !important;
        padding: 0.6rem 0.8rem !important; background: var(--panel-alt) !important;
    }
    [data-testid="stTextInput"] input::placeholder { color: var(--muted) !important; opacity: 1; }

    [data-testid="stColumn"]:nth-of-type(2) [data-testid="stButton"] button,
    [data-testid="stDownloadButton"] button {
        background: var(--accent) !important; color: var(--bg) !important; border: none !important;
        border-radius: 8px !important; font-weight: 600 !important; padding: 0.6rem 1.2rem !important;
    }
    [data-testid="stColumn"]:nth-of-type(2) [data-testid="stButton"] button:hover,
    [data-testid="stDownloadButton"] button:hover { background: #F0B65E !important; }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--panel-alt) !important; border-color: var(--border) !important; border-radius: 12px !important;
    }

    [data-testid="stAlert"] { background: var(--panel-alt) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }

    [data-testid="stExpander"] { background: var(--panel-alt) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }
    [data-testid="stExpander"] pre, [data-testid="stExpander"] code {
        background: var(--code-bg) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.82rem !important;
    }
    [data-testid="stCodeBlock"] pre, [data-testid="stCodeBlock"] code { background: var(--code-bg) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def extract_text(value) -> str:
    """Safely turn a chain/agent output (str, AIMessage, dict, etc.) into text."""
    if isinstance(value, str):
        return value
    if hasattr(value, "content"):
        return value.content
    return str(value)


# ----------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------
if "state" not in st.session_state:
    st.session_state.state = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "history" not in st.session_state:
    st.session_state.history = []

rail, canvas = st.columns([1, 2.3], gap="medium")

# ----------------------------------------------------------------------
# Rail — brand + pipeline steps + recent topics
# ----------------------------------------------------------------------
with rail:
    st.markdown(
        """
        <div class="brand-mark">
            <svg class="logo-glow" width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path style="fill:#E8A33D" d="M13 2C13 2 7 9.5 7 14.5C7 18.09 9.69 21 13 21C16.31 21 19 18.09 19 14.5C19 9.5 13 2 13 2Z"/>
                <path style="stroke:#E8A33D" stroke-width="1.5" stroke-linecap="round" d="M13 21V24"/>
            </svg>
            <span class="brand-name">Inkling</span>
        </div>
        <div class="brand-tag">a small idea, researched into a full one</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="rail-label">The pipeline</div>', unsafe_allow_html=True)
    steps = [
        ("01", "Search", "finds recent, reliable sources"),
        ("02", "Read", "scrapes the best one for depth"),
        ("03", "Write", "drafts the report"),
        ("04", "Critique", "reviews it and flags gaps"),
    ]
    steps_html = ""
    for n, t, d in steps:
        steps_html += (
            f'<div class="vstep"><div class="num">{n}</div>'
            f'<div class="txt"><div class="t">{t}</div><div class="d">{d}</div></div></div>'
        )
    st.markdown(steps_html, unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown('<div class="rail-label">Recent</div>', unsafe_allow_html=True)
        for i, past_topic in enumerate(reversed(st.session_state.history[-5:])):
            if st.button(f"↺  {past_topic}", key=f"recent_{i}", use_container_width=True):
                st.session_state["topic_input"] = past_topic
                st.rerun()

# ----------------------------------------------------------------------
# Canvas — input + results
# ----------------------------------------------------------------------
with canvas:
    st.markdown('<div class="eyebrow">New research</div>', unsafe_allow_html=True)
    st.markdown("## What should Inkling look into?")
    st.markdown(
        '<p class="subtitle">Give it a topic — Search, Read, Write, and Critique agents take it from there.</p>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        topic = st.text_input(
            "Research topic",
            placeholder="e.g. Impact of AI on renewable energy adoption",
            label_visibility="collapsed",
            key="topic_input",
        )
        run_clicked = st.button("Run research", type="primary", use_container_width=True)

    if run_clicked:
        if not topic.strip():
            st.warning("Enter a topic first.")
        else:
            try:
                with st.status("Working through the pipeline...", expanded=True) as status:
                    st.write("🔍 Search agent finding sources...")
                    st.write("📖 Reader agent scraping the best source...")
                    st.write("✍️ Writer drafting the report...")
                    st.write("🧐 Critic reviewing the report...")
                    result = run_resarch_pipeline(topic)
                    status.update(label="Done", state="complete", expanded=False)

                st.session_state.state = result
                st.session_state.topic = topic
                if topic not in st.session_state.history:
                    st.session_state.history.append(topic)
            except Exception as e:
                st.session_state.state = None
                st.error(f"Pipeline failed: {e}")
                with st.expander("Error details"):
                    st.code(traceback.format_exc())

    state = st.session_state.state

    if state:
        st.divider()

        with st.container(border=True):
            st.markdown('<span class="badge">Report</span>', unsafe_allow_html=True)
            report_text = extract_text(state.get("report", ""))
            st.markdown(report_text)
            st.download_button(
                "⬇ Download report (.md)",
                data=report_text,
                file_name=f"{st.session_state.topic.replace(' ', '_')}_report.md",
                mime="text/markdown",
            )

        with st.container(border=True):
            st.markdown('<span class="badge">Critic\'s review</span>', unsafe_allow_html=True)
            st.markdown(extract_text(state.get("feedback", "")))

        with st.expander("Search results (raw)"):
            st.code(extract_text(state.get("search_results", "")), language=None)

        with st.expander("Scraped content (raw)"):
            st.code(extract_text(state.get("scraped_content", "")), language=None)
    else:
        st.caption("Nothing yet — run a topic to see the report here.")
