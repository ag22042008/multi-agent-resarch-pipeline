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
# Style — a two-tone "ink meets paper" concept: a dark rail carries the
# brand and the pipeline steps, a warm paper canvas is where the topic
# goes in and the report comes out. Wax-seal red is the one accent color;
# everything else stays quiet.
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');

    :root {
        --ink-900: #12181F;
        --ink-700: #232C36;
        --ink-100: #E7ECEF;
        --paper: #FBF9F4;
        --paper-line: #E4DFD3;
        --text: #201C18;
        --muted: #7A756B;
        --accent: #8C2F3B;
        --accent-soft: #F3E3E4;
    }

    .stApp { background: var(--paper); }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--text); }
    h1, h2, h3 { font-family: 'Fraunces', serif !important; color: var(--text) !important; letter-spacing: -0.01em; }

    /* --- rail (first column) --- */
    [data-testid="stColumn"]:nth-of-type(1) {
        background: var(--ink-900);
        border-radius: 18px;
        padding: 1.8rem 1.4rem;
        min-height: 560px;
    }
    [data-testid="stColumn"]:nth-of-type(1) * { color: var(--ink-100) !important; }
    [data-testid="stColumn"]:nth-of-type(1) h1,
    [data-testid="stColumn"]:nth-of-type(1) h2,
    [data-testid="stColumn"]:nth-of-type(1) h3 { color: var(--ink-100) !important; }
    [data-testid="stColumn"]:nth-of-type(1) [data-testid="stButton"] button {
        background: transparent !important;
        border: 1px solid rgba(231,236,239,0.25) !important;
        color: var(--ink-100) !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        padding: 0.35rem 0.7rem !important;
        text-align: left !important;
    }
    [data-testid="stColumn"]:nth-of-type(1) [data-testid="stButton"] button:hover {
        border-color: var(--accent) !important;
        color: white !important;
    }

    /* --- canvas (second column) --- */
    [data-testid="stColumn"]:nth-of-type(2) {
        background: var(--paper);
        border: 1px solid var(--paper-line);
        border-radius: 18px;
        padding: 2rem 2.2rem;
    }

    .brand-mark { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.2rem; }
    .brand-name { font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.5rem; color: var(--ink-100); }
    .brand-tag { font-size: 0.8rem; color: #A9B0B6; margin-top: -0.3rem; margin-bottom: 1.6rem; }

    .rail-label {
        font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: #A9B0B6; margin: 1.4rem 0 0.6rem;
    }

    .vstep { display: flex; gap: 0.7rem; align-items: flex-start; margin-bottom: 0.9rem; }
    .vstep .num {
        flex-shrink: 0; width: 26px; height: 26px; border-radius: 50%;
        border: 1.5px solid var(--accent); color: var(--accent) !important;
        display: flex; align-items: center; justify-content: center;
        font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 600;
        background: transparent;
    }
    .vstep .txt .t { font-weight: 600; font-size: 0.88rem; }
    .vstep .txt .d { font-size: 0.76rem; color: #A9B0B6 !important; }

    .eyebrow {
        font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: var(--accent); margin-bottom: 0.3rem;
    }
    .subtitle { color: var(--muted); font-size: 1rem; margin-top: -0.5rem; margin-bottom: 1.4rem; }

    .badge {
        display: inline-block; font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase;
        color: var(--accent); background: var(--accent-soft);
        border-radius: 999px; padding: 0.25rem 0.7rem; margin-bottom: 0.7rem;
    }

    [data-testid="stColumn"]:nth-of-type(2) [data-testid="stTextInput"] input {
        border-radius: 8px; border: 1px solid var(--paper-line);
        padding: 0.6rem 0.8rem; font-family: 'Inter', sans-serif; background: white;
    }
    [data-testid="stColumn"]:nth-of-type(2) [data-testid="stButton"] button {
        background: var(--accent) !important; color: white !important; border: none !important;
        border-radius: 8px !important; font-weight: 600 !important; padding: 0.6rem 1.2rem !important;
    }
    [data-testid="stColumn"]:nth-of-type(2) [data-testid="stButton"] button:hover {
        background: #6E2530 !important;
    }

    [data-testid="stExpander"] pre { font-family: 'JetBrains Mono', monospace !important; font-size: 0.82rem !important; }
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
            <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M13 2C13 2 7 9.5 7 14.5C7 18.09 9.69 21 13 21C16.31 21 19 18.09 19 14.5C19 9.5 13 2 13 2Z" fill="#8C2F3B"/>
                <path d="M13 21V24" stroke="#8C2F3B" stroke-width="1.5" stroke-linecap="round"/>
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