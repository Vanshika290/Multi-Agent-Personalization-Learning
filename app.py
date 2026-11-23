"""Aspira: AI Learning Platform & Project Architect.
Features interactive dashboards, category filtering, gamified study streak tracking,
prominent project structure roadmaps, live ArXiv research papers, and AI Tutor chat.
"""

import os
import streamlit as st
from config import DEFAULT_MODEL, AVAILABLE_MODELS, get_api_key
from utils.gemini_client import GeminiClient
from agents.subject_agent import SubjectStudyAgent
from agents.project_agent import ProjectMentorAgent
from agents.arxiv_service import fetch_arxiv_papers

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(
    page_title="Aspira - AI Learning & Project Platform",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- SESSION STATE INITIALIZATION -----------------
if "study_hours" not in st.session_state:
    st.session_state["study_hours"] = 2.0
if "target_hours" not in st.session_state:
    st.session_state["target_hours"] = 3.0
if "streak_days" not in st.session_state:
    st.session_state["streak_days"] = 7
if "active_category_filter" not in st.session_state:
    st.session_state["active_category_filter"] = "All"
if "saved_bookmarks" not in st.session_state:
    st.session_state["saved_bookmarks"] = []
if "nav_index" not in st.session_state:
    st.session_state["nav_index"] = 0
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "👋 Hello! I am your Aspira AI Tutor. What subject or project can I help you architect today?"}
    ]

# ----------------- ASPIRA THEME CUSTOM CSS -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    
    .stApp {
        background-color: #120e24 !important;
        color: #e2e8f0;
    }
    
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1440px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1a1435 !important;
        border-right: 1px solid #2a2250 !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    /* Brand Logo Header */
    .brand-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0.5rem 1.4rem 0.5rem;
    }
    .brand-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.45rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .brand-icon {
        width: 38px;
        height: 38px;
        background: linear-gradient(135deg, #8b5cf6, #6366f1);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        box-shadow: 0 4px 14px rgba(139, 92, 246, 0.45);
    }
    
    .page-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .top-actions-row {
        display: flex;
        align-items: center;
        gap: 12px;
        justify-content: flex-end;
    }
    .icon-btn {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: #231c47;
        border: 1px solid #342865;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #a5a1c9;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .icon-btn:hover {
        background: #342865;
        color: #ffffff;
    }
    .user-avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: #3b82f6;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
    }

    /* Gamification Sidebar Cards */
    .streak-card {
        background: linear-gradient(135deg, #2c1f57 0%, #1c153b 100%);
        border: 1px solid #3c2d6f;
        border-radius: 16px;
        padding: 16px;
        margin-top: 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }
    .streak-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }
    .streak-badge-icon {
        width: 32px;
        height: 32px;
        background: rgba(168, 85, 247, 0.25);
        color: #c084fc;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    .streak-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #ffffff;
    }
    .streak-sub {
        font-size: 0.75rem;
        color: #a5a1c9;
        margin-left: 42px;
        margin-top: -6px;
        margin-bottom: 12px;
    }
    .streak-days {
        display: flex;
        justify-content: space-between;
        gap: 4px;
    }
    .day-pill {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        background: #34275f;
        color: #d8b4fe;
    }
    .day-pill.active {
        background: linear-gradient(135deg, #8b5cf6, #a855f7);
        color: #ffffff;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.6);
    }

    .goal-card {
        background: #211945;
        border: 1px solid #36296b;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 14px;
    }
    .goal-top {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
    }
    .goal-progress-bg {
        width: 100%;
        height: 7px;
        background: #36296b;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 8px;
    }
    .goal-progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #8b5cf6, #c084fc);
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    .goal-sub {
        font-size: 0.75rem;
        color: #a5a1c9;
    }

    /* Course Cards */
    .aspira-card {
        background: #211a43;
        border: 1px solid #342865;
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 8px;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        display: flex;
        flex-direction: column;
    }
    .aspira-card:hover {
        transform: translateY(-4px);
        border-color: #6366f1;
        box-shadow: 0 12px 28px rgba(0,0,0,0.45);
    }
    .card-banner {
        width: 100%;
        height: 160px;
        position: relative;
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        padding: 12px;
    }
    .card-banner::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 65%;
        background: linear-gradient(to top, #211a43, transparent);
    }
    .banner-tag {
        position: relative;
        z-index: 2;
        background: rgba(18, 14, 36, 0.75);
        backdrop-filter: blur(8px);
        color: #e2e8f0;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.12);
    }
    .rating-badge {
        position: relative;
        z-index: 2;
        background: rgba(18, 14, 36, 0.75);
        backdrop-filter: blur(8px);
        color: #fbbf24;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.12);
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .card-body {
        padding: 18px 18px 14px 18px;
        display: flex;
        flex-direction: column;
    }
    .meta-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .level-badge {
        font-size: 0.75rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
    }
    .level-beginner { background: rgba(34, 197, 94, 0.2); color: #4ade80; }
    .level-intermediate { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
    .level-advanced { background: rgba(239, 68, 68, 0.2); color: #f87171; }
    .duration-text {
        font-size: 0.78rem;
        color: #a5a1c9;
        font-weight: 600;
    }
    .card-title {
        font-size: 1.08rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
        line-height: 1.35;
    }
    .card-desc {
        font-size: 0.82rem;
        color: #a5a1c9;
        line-height: 1.45;
        margin-bottom: 14px;
        min-height: 38px;
    }
    .progress-section {
        margin-bottom: 12px;
    }
    .progress-label-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        color: #a5a1c9;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .progress-bar-container {
        width: 100%;
        height: 6px;
        background: #2e245b;
        border-radius: 10px;
        overflow: hidden;
    }
    .progress-fill-purple {
        height: 100%;
        background: linear-gradient(90deg, #8b5cf6, #c084fc);
        border-radius: 10px;
    }
    .tags-row {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
        margin-bottom: 8px;
    }
    .tech-pill {
        background: #2a2154;
        color: #c4b5fd;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
    }

    /* Interactive Roadmap Cards & Flow */
    .roadmap-phase-card {
        background: #1f183d;
        border: 1px solid #3c2e72;
        border-left: 4px solid #8b5cf6;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
    }
    .roadmap-phase-title {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }
    .roadmap-phase-badge {
        font-size: 0.72rem;
        font-weight: 700;
        background: rgba(139, 92, 246, 0.25);
        color: #c084fc;
        padding: 2px 8px;
        border-radius: 6px;
    }
    .structure-box {
        background: #17112e;
        border: 1px solid #2f2359;
        border-radius: 12px;
        padding: 16px;
        font-family: 'Courier New', Courier, monospace;
        color: #7dd3fc;
        font-size: 0.88rem;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    /* Buttons */
    div.continue-btn button {
        background: #2e245a !important;
        border: 1px solid #483984 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        padding: 0.55rem !important;
        box-shadow: none !important;
        width: 100% !important;
    }
    div.continue-btn button:hover {
        background: #7c3aed !important;
        border-color: #7c3aed !important;
        color: #ffffff !important;
    }

    div.enroll-btn button {
        background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
        border: none !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        padding: 0.55rem !important;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.4) !important;
        width: 100% !important;
    }
    div.enroll-btn button:hover {
        background: linear-gradient(135deg, #6d28d9, #4f46e5) !important;
        box-shadow: 0 6px 18px rgba(124, 58, 237, 0.6) !important;
        color: #ffffff !important;
    }

    /* Research Paper Cards */
    .research-card {
        background: #211a43;
        border: 1px solid #36296b;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 16px;
        transition: border-color 0.2s ease;
    }
    .research-card:hover {
        border-color: #8b5cf6;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #211a43 !important;
        border: 1px solid #342865 !important;
        border-radius: 10px !important;
        color: #a5a1c9 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
    }
    .stTabs [aria-selected="true"] {
        background: #7c3aed !important;
        color: #ffffff !important;
        border-color: #7c3aed !important;
        box-shadow: 0 2px 10px rgba(124, 58, 237, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR: BRAND, NAVIGATION & GAMIFICATION -----------------
with st.sidebar:
    st.markdown("""
    <div class="brand-container">
        <div class="brand-logo">
            <div class="brand-icon">📖</div>
            <span>Aspira</span>
        </div>
        <div style="color: #a5a1c9; font-size: 1.1rem; cursor: pointer;">⇄</div>
    </div>
    """, unsafe_allow_html=True)

    nav_options = [
        "⊞  Dashboard",
        "📖  Courses",
        "🧭  Learning Paths",
        "🎯  Goals & Streaks",
        "🤖  AI Tutor",
        "⭐  Saved Library"
    ]

    current_nav_idx = min(len(nav_options) - 1, max(0, st.session_state.get("nav_index", 0)))
    nav_choice = st.radio(
        "Navigation",
        options=nav_options,
        index=current_nav_idx,
        key="sidebar_navigation_radio",
        label_visibility="collapsed"
    )
    # Sync back state
    st.session_state["nav_index"] = nav_options.index(nav_choice)

    # 7-Day Streak Card
    st.markdown(f"""
    <div class="streak-card">
        <div class="streak-header">
            <div class="streak-badge-icon">🔥</div>
            <div class="streak-title">{st.session_state['streak_days']}-Day Streak!</div>
        </div>
        <div class="streak-sub">Keep it going!</div>
        <div class="streak-days">
            <div class="day-pill active">1</div>
            <div class="day-pill active">2</div>
            <div class="day-pill active">3</div>
            <div class="day-pill active">4</div>
            <div class="day-pill active">5</div>
            <div class="day-pill active">6</div>
            <div class="day-pill active">7</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Today's Goal Card
    curr_hours = st.session_state["study_hours"]
    tgt_hours = st.session_state["target_hours"]
    pct = min(100, int((curr_hours / tgt_hours) * 100))
    hours_left = max(0.0, tgt_hours - curr_hours)

    st.markdown(f"""
    <div class="goal-card">
        <div class="goal-top">
            <span>Today's Goal</span>
            <span>{pct}%</span>
        </div>
        <div style="font-size: 0.85rem; font-weight: 700; color: #ffffff; margin-bottom: 6px;">{curr_hours:.1f}/{tgt_hours:.0f} hours</div>
        <div class="goal-progress-bg">
            <div class="goal-progress-fill" style="width: {pct}%;"></div>
        </div>
        <div class="goal-sub">{'Daily goal achieved! 🎉' if hours_left == 0 else f'{hours_left:.1f} more hour to reach your daily goal!'}</div>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Log Study Time Button
    if st.button("⏱️ Log +30 Min Study", use_container_width=True):
        st.session_state["study_hours"] = round(st.session_state["study_hours"] + 0.5, 1)
        if st.session_state["study_hours"] >= st.session_state["target_hours"]:
            st.balloons()
        st.rerun()

    st.markdown("---")
    
    # API Engine Configuration
    st.markdown("<div style='font-size: 0.82rem; font-weight: 700; color: #a5a1c9; margin-bottom: 6px;'>⚙️ AI ENGINE CONFIG</div>", unsafe_allow_html=True)
    env_key = get_api_key()
    user_api_key = st.text_input(
        "Gemini API Key",
        value=st.session_state.get("gemini_api_key", env_key),
        type="password",
        placeholder="Enter API key...",
        help="Optional: Free key from https://aistudio.google.com/"
    )
    if user_api_key:
        st.session_state["gemini_api_key"] = user_api_key
        st.caption("🟢 Gemini API Connected")
    else:
        st.caption("🟡 Preview Mode Active (Curated Knowledge Base)")

    selected_model = st.selectbox("Model", options=AVAILABLE_MODELS, index=0)

# Initialize AI Client and Agents
client = GeminiClient(api_key=user_api_key or env_key, model_name=selected_model)
subject_agent = SubjectStudyAgent(client=client)
project_agent = ProjectMentorAgent(client=client)

# Define Course Catalog Data
ALL_COURSES = [
    {
        "id": "ml",
        "title": "Introduction to Machine Learning",
        "category": "Data Science",
        "level": "Beginner",
        "duration": "20 hours",
        "rating": "4.8",
        "desc": "Learn the fundamentals of machine learning algorithms, model training, and applications.",
        "progress": 65,
        "tags": ["Python", "ML", "Data Science"],
        "banner": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=500&auto=format&fit=crop",
        "subject_query": "Machine Learning"
    },
    {
        "id": "js",
        "title": "Advanced JavaScript Concepts",
        "category": "Web Development",
        "level": "Advanced",
        "duration": "15 hours",
        "rating": "4.9",
        "desc": "Deep dive into advanced JavaScript concepts like closures, prototypes, event loops, and async patterns.",
        "progress": 30,
        "tags": ["JavaScript", "Web", "Programming"],
        "banner": "https://images.unsplash.com/photo-1579468118864-1b9ea3c0db4a?w=500&auto=format&fit=crop",
        "subject_query": "Advanced JavaScript"
    },
    {
        "id": "ux",
        "title": "UX Design Principles",
        "category": "Design",
        "level": "Intermediate",
        "duration": "12 hours",
        "rating": "4.7",
        "desc": "Master the principles of user experience design, wireframing, heuristic evaluation, and intuitive interfaces.",
        "progress": 0,
        "tags": ["UX", "Design", "UI"],
        "banner": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=500&auto=format&fit=crop",
        "subject_query": "UX Design Principles"
    },
    {
        "id": "dsa",
        "title": "Data Structures & Algorithms",
        "category": "Computer Science",
        "level": "Intermediate",
        "duration": "25 hours",
        "rating": "4.6",
        "desc": "Master Trees, Graphs, Dynamic Programming, and complexity analysis for technical interviews.",
        "progress": 45,
        "tags": ["DSA", "C++", "Algorithms"],
        "banner": "https://images.unsplash.com/photo-1516116211227-bbc154563c63?w=500&auto=format&fit=crop",
        "subject_query": "Data Structures and Algorithms"
    },
    {
        "id": "cloud",
        "title": "Cloud Architecture & DevOps",
        "category": "Cloud Computing",
        "level": "Advanced",
        "duration": "18 hours",
        "rating": "4.5",
        "desc": "Deploy resilient microservices using Docker, Kubernetes, CI/CD pipelines, and serverless backends.",
        "progress": 20,
        "tags": ["AWS", "Kubernetes", "DevOps"],
        "banner": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=500&auto=format&fit=crop",
        "subject_query": "Cloud Computing and DevOps"
    }
]

# ----------------- VIEW 1: DASHBOARD -----------------
if "Dashboard" in nav_choice:
    # Header Row
    header_col1, header_col2, header_col3, header_col4 = st.columns([2.2, 3.2, 2.2, 1.4])
    with header_col1:
        st.markdown('<div class="page-title">My Courses</div>', unsafe_allow_html=True)
    with header_col2:
        search_query = st.text_input(
            "Search courses...",
            placeholder="🔍 Search courses or type any subject...",
            label_visibility="collapsed"
        )
    with header_col3:
        st.markdown('<div class="enroll-btn">', unsafe_allow_html=True)
        explore_btn = st.button("+ Explore New Courses", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with header_col4:
        st.markdown("""
        <div class="top-actions-row">
            <div class="icon-btn" title="Toggle Theme">☼</div>
            <div class="icon-btn" title="Settings">⚙</div>
            <div class="user-avatar" title="Learner Profile">👤</div>
        </div>
        """, unsafe_allow_html=True)

    # Category Filter Pills
    cat_cols = st.columns([0.8, 1.3, 1.6, 1.0, 1.6, 1.5, 3.0])
    categories = ["All", "Data Science", "Web Development", "Design", "Computer Science", "Cloud Computing"]
    
    for i, cat in enumerate(categories):
        with cat_cols[i]:
            is_active = (st.session_state["active_category_filter"] == cat)
            button_label = f"• {cat}" if is_active else cat
            if st.button(button_label, key=f"cat_{cat}"):
                st.session_state["active_category_filter"] = cat
                st.rerun()

    current_filter = st.session_state["active_category_filter"]
    display_courses = ALL_COURSES if current_filter == "All" else [c for c in ALL_COURSES if c["category"] == current_filter]

    if search_query.strip():
        st.markdown(f"### 🔍 AI Curated Results for: **{search_query}**")
        with st.spinner(f"Curating verified YouTube channels and top blogs for '{search_query}'..."):
            curated_res = subject_agent.curate_subject(search_query.strip())
            st.markdown(curated_res, unsafe_allow_html=True)
        st.markdown("---")

    if explore_btn:
        st.session_state["show_explore_modal"] = not st.session_state.get("show_explore_modal", False)

    if st.session_state.get("show_explore_modal"):
        with st.expander("✨ Explore Any New Subject or Course", expanded=True):
            exp_col1, exp_col2 = st.columns([3, 1])
            with exp_col1:
                custom_subj = st.text_input("Enter any subject to curate:", placeholder="e.g. Operating Systems, Quantum Computing, Deep Learning...")
            with exp_col2:
                st.write("")
                st.write("")
                go_curate = st.button("🚀 Curate Subject")
            if go_curate and custom_subj.strip():
                with st.spinner(f"Curating top YouTube channels and reading materials for {custom_subj}..."):
                    res = subject_agent.curate_subject(custom_subj.strip())
                    st.markdown(res, unsafe_allow_html=True)

    # Render Courses Grid (3 items per row)
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
    num_courses = len(display_courses)
    
    for row_start in range(0, num_courses, 3):
        row_slice = display_courses[row_start:row_start + 3]
        cols = st.columns(3)
        for idx, course in enumerate(row_slice):
            with cols[idx]:
                level_class = f"level-{course['level'].lower()}"
                st.markdown(f"""
                <div class="aspira-card">
                    <div class="card-banner" style="background-image: linear-gradient(180deg, rgba(18,14,36,0.3) 0%, rgba(33,26,67,0.95) 100%), url('{course['banner']}');">
                        <span class="banner-tag">{course['category']}</span>
                        <span class="rating-badge">★ {course['rating']}</span>
                    </div>
                    <div class="card-body">
                        <div class="meta-row">
                            <span class="level-badge {level_class}">{course['level']}</span>
                            <span class="duration-text">{course['duration']}</span>
                        </div>
                        <div class="card-title">{course['title']}</div>
                        <div class="card-desc">{course['desc']}</div>
                        <div class="progress-section">
                            <div class="progress-label-row">
                                <span>Progress</span>
                                <span>{course['progress']}%</span>
                            </div>
                            <div class="progress-bar-container">
                                <div class="progress-fill-purple" style="width: {course['progress']}%;"></div>
                            </div>
                        </div>
                        <div class="tags-row">
                            {' '.join([f'<span class="tech-pill">{t}</span>' for t in course['tags']])}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                btn_wrapper = "continue-btn" if course['progress'] > 0 else "enroll-btn"
                btn_text = "Continue Learning" if course['progress'] > 0 else "Enroll Now"
                st.markdown(f'<div class="{btn_wrapper}">', unsafe_allow_html=True)
                if st.button(btn_text, key=f"btn_course_{course['id']}", use_container_width=True):
                    st.session_state["active_subject_view"] = course["subject_query"]
                st.markdown('</div>', unsafe_allow_html=True)

    # Prompt Card to Switch to Projects View
    st.markdown('<div style="height: 14px;"></div>', unsafe_allow_html=True)
    c_p1, c_p2, c_p3 = st.columns(3)
    with c_p1:
        st.markdown("""
        <div class="aspira-card" style="border: 2px dashed #4f3b89; background: rgba(33,26,67,0.45); justify-content: center; align-items: center; text-align: center; padding: 26px 18px;">
            <div style="font-size: 2.2rem; margin-bottom: 8px;">🚀</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 6px;">Build a Project</div>
            <div style="font-size: 0.82rem; color: #a5a1c9; margin-bottom: 14px;">Turn your idea into a step-by-step engineering roadmap with live ArXiv papers.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="enroll-btn">', unsafe_allow_html=True)
        if st.button("Launch Project Mentor ➔", key="btn_proj_prompt_db", use_container_width=True):
            st.session_state["nav_index"] = 2
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # If an active course card was clicked, show its full study companion guide right below!
    if "active_subject_view" in st.session_state:
        target_subject = st.session_state["active_subject_view"]
        st.markdown("---")
        header_l, header_r = st.columns([3, 1])
        with header_l:
            st.markdown(f"## 📚 Curriculum & Curation: **{target_subject}**")
        with header_r:
            if st.button("⭐ Bookmark Course", key="btn_bkmk_top"):
                if target_subject not in st.session_state["saved_bookmarks"]:
                    st.session_state["saved_bookmarks"].append(target_subject)
                    st.toast(f"Saved {target_subject} to your Library!", icon="⭐")

        with st.spinner(f"Curating verified YouTube channels, top blogs, and roadmap for {target_subject}..."):
            guide = subject_agent.curate_subject(target_subject)
            st.markdown(guide, unsafe_allow_html=True)
            
            st.download_button(
                "📥 Download Course Guide (.md)",
                data=guide,
                file_name=f"{target_subject.replace(' ', '_')}_Guide.md",
                mime="text/markdown"
            )

# ----------------- VIEW 2: COURSES (SUBJECT COMPANION) -----------------
elif "Courses" in nav_choice:
    st.markdown('<div class="page-title">📖 Courses & Subject Study Companion</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #a5a1c9; font-size: 0.95rem; margin-bottom: 16px;">Type any academic subject or technical course. Aspira curates top YouTube channels, verified blogs, milestone checklists, and self-check flashcards.</div>', unsafe_allow_html=True)

    # Quick Topic Chips
    st.markdown("<div style='font-size: 0.82rem; font-weight: 700; color: #a5a1c9;'>⚡ QUICK POPULAR SUBJECTS:</div>", unsafe_allow_html=True)
    chip_cols = st.columns(6)
    quick_subjects = ["Operating Systems", "Computer Networks", "Compiler Design", "Quantum Computing", "Deep Learning", "Organic Chemistry"]
    for i, subj in enumerate(quick_subjects):
        with chip_cols[i]:
            if st.button(subj, key=f"quick_subj_{i}", use_container_width=True):
                st.session_state["subject_input_field"] = subj
                st.rerun()

    c1, c2, c3 = st.columns([3, 1.5, 1.5])
    with c1:
        subject_query = st.text_input(
            "Subject Name",
            value=st.session_state.get("subject_input_field", ""),
            placeholder="e.g. Operating Systems, Computer Networks, Machine Learning, Organic Chemistry..."
        )
    with c2:
        level_sel = st.selectbox(
            "Knowledge Level",
            ["Beginner (First-time learner)", "Intermediate (Foundations clear)", "Advanced (Deep dive & Mastery)"]
        )
    with c3:
        goal_sel = st.selectbox(
            "Learning Goal",
            ["Comprehensive Understanding", "Exam & Semester Prep", "Job Interview Preparation", "Practical Project Building"]
        )

    st.markdown('<div class="enroll-btn">', unsafe_allow_html=True)
    curate_btn = st.button("🚀 Curate Subject Guide & Recommendations", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if curate_btn:
        if not subject_query.strip():
            st.warning("Please type a subject name.")
        else:
            with st.spinner(f"Curating YouTube channels and blogs for '{subject_query}'..."):
                guide = subject_agent.curate_subject(subject_query.strip(), level=level_sel, goal=goal_sel)
                st.session_state["curated_guide"] = guide
                st.session_state["curated_guide_subject"] = subject_query.strip()

    if "curated_guide" in st.session_state:
        st.markdown("---")
        h_col1, h_col2 = st.columns([3, 1])
        with h_col1:
            st.markdown(f"### 🎯 Results for: {st.session_state.get('curated_guide_subject', 'Subject')}")
        with h_col2:
            if st.button("⭐ Save to My Library", key="save_subj_btn"):
                subj_name = st.session_state.get('curated_guide_subject', 'Subject')
                if subj_name not in st.session_state["saved_bookmarks"]:
                    st.session_state["saved_bookmarks"].append(subj_name)
                    st.toast(f"Saved {subj_name} to your library!", icon="⭐")

        st.markdown(st.session_state["curated_guide"], unsafe_allow_html=True)
        st.download_button(
            "📥 Download Subject Guide (.md)",
            data=st.session_state["curated_guide"],
            file_name=f"{st.session_state.get('curated_guide_subject', 'Subject')}_Guide.md",
            mime="text/markdown"
        )

# ----------------- VIEW 3: LEARNING PATHS (PROJECT ROADMAP & ARCHITECTURE) -----------------
elif "Learning Paths" in nav_choice:
    st.markdown('<div class="page-title">🧭 Learning Paths: Project Roadmap & Architecture Mentor</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #a5a1c9; font-size: 0.95rem; margin-bottom: 16px;">Describe any project idea you want to build. Aspira generates a <b>step-by-step implementation roadmap</b>, <b>production directory structure</b>, <b>system architecture</b>, and <b>live ArXiv research papers</b>.</div>', unsafe_allow_html=True)

    # Clickable Project Idea Chips
    st.markdown("<div style='font-size: 0.82rem; font-weight: 700; color: #a5a1c9;'>⚡ CLICK A SAMPLE PROJECT IDEA TO TRY:</div>", unsafe_allow_html=True)
    p_chips = st.columns(4)
    ideas = [
        ("Autonomous Drone Navigation (Computer Vision)", "Robotics, IoT & Embedded Systems"),
        ("AI Interview Voice Agent with Emotion Analysis", "Artificial Intelligence & Machine Learning"),
        ("Medical Image Segmentation for Cancer Detection", "Artificial Intelligence & Machine Learning"),
        ("Blockchain Decentralized Voting Protocol", "Blockchain & Web3")
    ]
    for idx, (idea_text, d_text) in enumerate(ideas):
        with p_chips[idx]:
            if st.button(idea_text[:35] + "...", key=f"chip_idea_{idx}", use_container_width=True):
                st.session_state["prefill_project_idea"] = idea_text
                st.session_state["prefill_domain"] = d_text
                st.rerun()

    col_idea, col_meta = st.columns([2.5, 1.5])
    with col_idea:
        project_idea = st.text_area(
            "Describe your project idea:",
            value=st.session_state.get("prefill_project_idea", "AI-powered recruitment agent that conducts automated voice interviews, evaluates speech and technical skills, and summarizes applicant metrics"),
            placeholder="e.g. AI-powered recruitment agent that conducts automated voice interviews, evaluates speech and technical skills, and summarizes applicant metrics...",
            height=110
        )
    with col_meta:
        domain_options = [
            "Artificial Intelligence & Machine Learning",
            "Full-Stack Web Development",
            "Cybersecurity & Cryptography",
            "Cloud, DevOps & Distributed Systems",
            "Robotics, IoT & Embedded Systems",
            "Mobile & Cross-Platform Apps",
            "Blockchain & Web3"
        ]
        default_domain = st.session_state.get("prefill_domain", domain_options[0])
        domain_idx = domain_options.index(default_domain) if default_domain in domain_options else 0
        
        domain_choice = st.selectbox("Engineering Domain", domain_options, index=domain_idx)
        time_choice = st.selectbox(
            "Target Timeframe",
            [
                "4-6 Weeks (Semester Project)",
                "2-3 Weeks (Fast Sprint MVP)",
                "2-3 Months (Capstone / Thesis Project)",
                "6+ Months (Production SaaS)"
            ]
        )
        papers_count = st.slider("ArXiv Papers to Fetch", 1, 5, 3)

    st.markdown('<div class="enroll-btn">', unsafe_allow_html=True)
    generate_proj = st.button("🚀 Architect Project & Generate Complete Roadmap", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Automatically initialize default blueprint if none exists so the user sees the structure right away!
    if "active_project_blueprint" not in st.session_state:
        with st.spinner("Initializing sample project structure roadmap..."):
            initial_res = project_agent.create_project_roadmap(
                project_idea=project_idea.strip() or "AI-powered technical interview agent",
                domain=domain_choice,
                timeframe=time_choice,
                max_papers=papers_count
            )
            st.session_state["active_project_blueprint"] = initial_res
            st.session_state["active_project_title"] = project_idea.strip()

    if generate_proj:
        if not project_idea.strip():
            st.warning("Please enter your project idea.")
        else:
            with st.spinner("Searching ArXiv repository & synthesizing full project structure & roadmap with Gemini..."):
                result = project_agent.create_project_roadmap(
                    project_idea=project_idea.strip(),
                    domain=domain_choice,
                    timeframe=time_choice,
                    max_papers=papers_count
                )
                st.session_state["active_project_blueprint"] = result
                st.session_state["active_project_title"] = project_idea.strip()

    if "active_project_blueprint" in st.session_state:
        b_res = st.session_state["active_project_blueprint"]
        papers = b_res.get("papers", [])
        roadmap_md = b_res.get("roadmap_markdown", "")
        p_name = st.session_state.get('active_project_title', 'Project')

        st.markdown("---")
        h_proj1, h_proj2 = st.columns([3, 1])
        with h_proj1:
            st.markdown(f"## 🚀 Project Architecture & Roadmap: **{p_name}**")
        with h_proj2:
            if st.button("⭐ Save to My Library", key="save_proj_btn"):
                if p_name not in st.session_state["saved_bookmarks"]:
                    st.session_state["saved_bookmarks"].append(f"Project: {p_name}")
                    st.toast(f"Saved '{p_name}' to your library!", icon="⭐")

        # Visual Highlights Banner
        st.markdown(f"""
        <div style="background: #211a43; border: 1px solid #36296b; border-radius: 14px; padding: 14px 20px; margin-bottom: 20px; display: flex; flex-wrap: wrap; gap: 14px; justify-content: space-between;">
            <div><span style="color: #a5a1c9; font-size: 0.8rem;">DOMAIN</span><br><b style="color: #ffffff;">{domain_choice}</b></div>
            <div><span style="color: #a5a1c9; font-size: 0.8rem;">TIMEFRAME</span><br><b style="color: #c084fc;">{time_choice}</b></div>
            <div><span style="color: #a5a1c9; font-size: 0.8rem;">ARCHITECTURE</span><br><b style="color: #4ade80;">Async Pipeline & Modularity</b></div>
            <div><span style="color: #a5a1c9; font-size: 0.8rem;">RESEARCH LITERATURE</span><br><b style="color: #38bdf8;">{len(papers)} ArXiv Papers Attached</b></div>
        </div>
        """, unsafe_allow_html=True)

        # Prominent Interactive Sub-Tabs: ROADMAP & STRUCTURE ARE FIRST!
        tab_roadmap, tab_structure, tab_papers, tab_code, tab_full_raw = st.tabs([
            "🗺️ Phased Implementation Roadmap",
            "📁 Project Directory Structure & Architecture",
            "📄 Research Papers (ArXiv)",
            "💻 Starter Code (`main.py`)",
            "📄 Full Blueprint Document"
        ])

        # TAB 1: ROADMAP & MILESTONES (PRIMARY VIEW)
        with tab_roadmap:
            st.markdown("### 🗺️ Step-by-Step Implementation Roadmap")
            st.markdown(f"Follow these 4 sequential engineering phases to build your project within **{time_choice}**:")

            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.markdown("""
                <div class="roadmap-phase-card">
                    <div class="roadmap-phase-title">
                        <span>Phase 1: Environment Setup & Architecture</span>
                        <span class="roadmap-phase-badge">Week 1</span>
                    </div>
                    <ul style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.6; padding-left: 18px;">
                        <li>Define API contracts, schema models, and data flow pipelines.</li>
                        <li>Initialize Git repository with <code>src/</code>, <code>tests/</code>, and virtual environment.</li>
                        <li>Review literature from ArXiv to lock down algorithms and baseline models.</li>
                    </ul>
                    <div style="font-size: 0.8rem; color: #4ade80; font-weight: 700; margin-top: 8px;">🎯 Milestone: Working local environment & architectural specification.</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="roadmap-phase-card" style="border-left-color: #38bdf8;">
                    <div class="roadmap-phase-title">
                        <span>Phase 2: Core MVP Implementation</span>
                        <span class="roadmap-phase-badge" style="background: rgba(56,189,248,0.25); color: #7dd3fc;">Week 2-3</span>
                    </div>
                    <ul style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.6; padding-left: 18px;">
                        <li>Implement ingestion endpoints and input sanitization pipeline.</li>
                        <li>Connect primary inference model or business processing engine.</li>
                        <li>Build initial unit tests covering the end-to-end data processing loop.</li>
                    </ul>
                    <div style="font-size: 0.8rem; color: #38bdf8; font-weight: 700; margin-top: 8px;">🎯 Milestone: Functional MVP passing test cases locally.</div>
                </div>
                """, unsafe_allow_html=True)

            with col_r2:
                st.markdown("""
                <div class="roadmap-phase-card" style="border-left-color: #fbbf24;">
                    <div class="roadmap-phase-title">
                        <span>Phase 3: Optimization & Edge Cases</span>
                        <span class="roadmap-phase-badge" style="background: rgba(245,158,11,0.25); color: #fde68a;">Week 4</span>
                    </div>
                    <ul style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.6; padding-left: 18px;">
                        <li>Incorporate Redis caching and asynchronous timeouts for API calls.</li>
                        <li>Handle edge cases: missing inputs, malformed requests, and rate limits.</li>
                        <li>Optimize latency and memory footprint using benchmarking profiling tools.</li>
                    </ul>
                    <div style="font-size: 0.8rem; color: #fbbf24; font-weight: 700; margin-top: 8px;">🎯 Milestone: Robust, optimized engine resilient to failures.</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="roadmap-phase-card" style="border-left-color: #4ade80;">
                    <div class="roadmap-phase-title">
                        <span>Phase 4: Testing, CI/CD & Deployment</span>
                        <span class="roadmap-phase-badge" style="background: rgba(34,197,94,0.25); color: #86efac;">Final Week</span>
                    </div>
                    <ul style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.6; padding-left: 18px;">
                        <li>Containerize entire application with multi-stage <code>Dockerfile</code>.</li>
                        <li>Deploy frontend and backend to cloud hosting (Render / AWS / Vercel).</li>
                        <li>Document project with architecture diagrams, demo video, and quantified resume bullets.</li>
                    </ul>
                    <div style="font-size: 0.8rem; color: #4ade80; font-weight: 700; margin-top: 8px;">🎯 Milestone: Public live URL & portfolio-ready GitHub repository.</div>
                </div>
                """, unsafe_allow_html=True)

        # TAB 2: PROJECT DIRECTORY STRUCTURE & ARCHITECTURE
        with tab_structure:
            st.markdown("### 📁 Recommended Production Repository Structure")
            st.markdown("Here is the clean, industry-standard directory tree for this project:")

            clean_proj_folder = p_name.lower().replace(" ", "_")[:24]
            dir_tree = f"""📦 {clean_proj_folder}/
├── 📁 src/
│   ├── 📁 api/
│   │   ├── __init__.py
│   │   └── routes.py         # REST & WebSocket endpoint handlers
│   ├── 📁 core/
│   │   ├── config.py         # Environment variables & constants
│   │   └── pipeline.py       # Core orchestration logic
│   ├── 📁 models/
│   │   └── processor.py      # AI/ML algorithms & inference engine
│   └── 📁 utils/
│       └── helpers.py        # Formatting, validations & transformations
├── 📁 tests/
│   ├── test_api.py           # Endpoint integration tests
│   └── test_pipeline.py      # Unit tests for core processing logic
├── .env.example              # Sample environment variables
├── Dockerfile                # Containerization specification
├── requirements.txt          # Python package dependencies
└── README.md                 # Documentation, architecture & setup guide"""

            st.markdown(f'<div class="structure-box"><pre>{dir_tree}</pre></div>', unsafe_allow_html=True)

            st.markdown("### 🏗️ High-Level System Architecture & Data Flow")
            st.markdown("""
```mermaid
graph TD
    Client([Client / User Interface]) --> API[API Gateway / Router]
    API --> Pipeline[Core Processing Pipeline]
    Pipeline --> Cache[(Redis Cache)]
    Pipeline --> Storage[(Database / Storage)]
    Pipeline --> Engine[AI Engine / Models]
    Engine --> Output([Processed Output / Telemetry])
```
            """)

        # TAB 3: ACADEMIC RESEARCH PAPERS (ARXIV)
        with tab_papers:
            st.markdown("### 📄 Real-Time Peer-Reviewed Research Papers (ArXiv)")
            st.markdown("Study these papers to understand foundational algorithms, loss functions, and benchmark datasets:")
            if papers:
                for i, p in enumerate(papers, 1):
                    st.markdown(f"""
                    <div class="research-card">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #a78bfa; margin-bottom: 6px;">
                            {i}. {p['title']}
                        </div>
                        <div style="margin-bottom: 8px;">
                            <span style="background: rgba(139,92,246,0.25); color: #c4b5fd; font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">📅 {p['published']}</span>
                            <span style="background: rgba(56,189,248,0.2); color: #7dd3fc; font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">📂 {p['primary_category']}</span>
                            <span style="color: #94a3b8; font-size: 0.85rem;">👥 {', '.join(p['authors'])}</span>
                        </div>
                        <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 12px;">
                            {p['summary']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c_pdf, c_arxiv, _ = st.columns([1.5, 1.5, 4])
                    with c_pdf:
                        if p.get("pdf_url"):
                            st.link_button("📥 Read PDF", p["pdf_url"], use_container_width=True)
                    with c_arxiv:
                        if p.get("arxiv_url"):
                            st.link_button("🔗 View on ArXiv", p["arxiv_url"], use_container_width=True)
                    st.write("")
            else:
                st.info("No direct papers retrieved. Foundational references are included in the blueprint.")

        # TAB 4: STARTER BOILERPLATE CODE
        with tab_code:
            st.markdown("### 💻 Starter Boilerplate Template (`main.py`)")
            st.markdown("Use this template as the baseline entry point for your project repository:")
            starter_code = f"""# {p_name} - Starter Pipeline
import os
import sys
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class ProjectPipeline:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {{}}
        logger.info("Initializing pipeline for: {p_name}")

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"End-to-end execution loop.\"\"\"
        logger.info("Step 1: Ingesting and validating input payload...")
        validated = self._validate(payload)
        
        logger.info("Step 2: Executing core processing & model inference...")
        processed = self._process(validated)
        
        logger.info("Step 3: Generating benchmarks and response...")
        return {{"status": "success", "data": processed}}

    def _validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return data

    def _process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {{"message": "Core model output generated successfully"}}

if __name__ == "__main__":
    pipeline = ProjectPipeline()
    sample_input = {{"test_key": "sample_data"}}
    output = pipeline.run(sample_input)
    print("Execution Result:", output)
"""
            st.code(starter_code, language="python")
            st.download_button(
                "📥 Download Starter Code (`main.py`)",
                data=starter_code,
                file_name="main.py",
                mime="text/x-python"
            )

        # TAB 5: FULL UNCUT BLUEPRINT DOCUMENT
        with tab_full_raw:
            st.markdown(roadmap_md, unsafe_allow_html=True)
            st.download_button(
                "📥 Download Complete Blueprint (.md)",
                data=roadmap_md,
                file_name=f"{clean_proj_folder}_Blueprint.md",
                mime="text/markdown"
            )

# ----------------- VIEW 4: GOALS & STREAKS -----------------
elif "Goals" in nav_choice:
    st.markdown('<div class="page-title">🎯 Goals, Streaks & Study Consistency</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #a5a1c9; font-size: 0.95rem; margin-bottom: 20px;">Track your daily study consistency, course completion milestones, and roadmap achievements.</div>', unsafe_allow_html=True)

    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown(f"""
        <div class="aspira-card" style="padding: 20px;">
            <div style="font-size: 0.9rem; font-weight: 700; color: #a5a1c9; margin-bottom: 6px;">CURRENT STREAK</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; margin-bottom: 8px;">🔥 {st.session_state['streak_days']} Days</div>
            <div style="color: #4ade80; font-size: 0.82rem; font-weight: 600;">Top 5% of consistent learners this week!</div>
        </div>
        """, unsafe_allow_html=True)
    with g2:
        st.markdown(f"""
        <div class="aspira-card" style="padding: 20px;">
            <div style="font-size: 0.9rem; font-weight: 700; color: #a5a1c9; margin-bottom: 6px;">TODAY'S STUDY HOURS</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; margin-bottom: 8px;">⏱️ {st.session_state['study_hours']:.1f} hrs</div>
            <div style="color: #a78bfa; font-size: 0.82rem; font-weight: 600;">Goal: {st.session_state['target_hours']:.0f} hours daily</div>
        </div>
        """, unsafe_allow_html=True)
    with g3:
        st.markdown(f"""
        <div class="aspira-card" style="padding: 20px;">
            <div style="font-size: 0.9rem; font-weight: 700; color: #a5a1c9; margin-bottom: 6px;">SAVED LIBRARY</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; margin-bottom: 8px;">⭐ {len(st.session_state['saved_bookmarks'])} Items</div>
            <div style="color: #38bdf8; font-size: 0.82rem; font-weight: 600;">Bookmarked courses & roadmaps</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🏆 Consistency Milestones")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.checkbox("✅ Complete 7-Day Study Streak (Achieved!)", value=True, disabled=True)
        st.checkbox("✅ Review first ArXiv Research Paper (Achieved!)", value=True, disabled=True)
    with col_m2:
        st.checkbox("⏳ Complete 30-Day Learning Challenge", value=False)
        st.checkbox("⏳ Deploy first Capstone Project to Cloud", value=False)

# ----------------- VIEW 5: AI TUTOR -----------------
elif "AI Tutor" in nav_choice:
    st.markdown('<div class="page-title">🤖 Aspira AI Tutor & Research Mentor</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #a5a1c9; font-size: 0.95rem; margin-bottom: 16px;">Ask any academic question, debug your project architecture, or ask for explanations of mathematical formulas in research papers.</div>', unsafe_allow_html=True)

    # Quick Tutor Prompt Pills
    st.markdown("<div style='font-size: 0.82rem; font-weight: 700; color: #a5a1c9;'>💡 QUICK PROMPT SUGGESTIONS:</div>", unsafe_allow_html=True)
    t_cols = st.columns(4)
    sample_queries = [
        "Explain backpropagation intuitively with formulas",
        "How do I choose between PostgreSQL and MongoDB?",
        "What questions will professors ask in my project viva?",
        "How do I read an ArXiv paper efficiently?"
    ]
    for idx, q in enumerate(sample_queries):
        with t_cols[idx]:
            if st.button(q[:30] + "...", key=f"tutor_prompt_{idx}", use_container_width=True):
                st.session_state["chat_history"].append({"role": "user", "content": q})
                with st.spinner("Aspira AI Tutor is thinking..."):
                    resp = client.generate(
                        prompt=q,
                        system_instruction="You are Aspira AI Tutor, an encouraging, deeply knowledgeable professor and engineering mentor."
                    )
                    st.session_state["chat_history"].append({"role": "assistant", "content": resp})
                st.rerun()

    # Chat Messages
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask a question about any subject, algorithm, or project...")
    if user_query:
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.generate(
                    prompt=user_query,
                    system_instruction="You are Aspira AI Tutor, an encouraging, highly knowledgeable professor and engineering mentor."
                )
                st.markdown(response)
                st.session_state["chat_history"].append({"role": "assistant", "content": response})

# ----------------- VIEW 6: SAVED LIBRARY (BOOKMARKS) -----------------
elif "Saved Library" in nav_choice:
    st.markdown('<div class="page-title">⭐ My Saved Library</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #a5a1c9; font-size: 0.95rem; margin-bottom: 20px;">Access your bookmarked subjects, courses, and generated project blueprints anytime.</div>', unsafe_allow_html=True)

    saved = st.session_state.get("saved_bookmarks", [])
    if not saved:
        st.info("No bookmarks saved yet! Click '⭐ Bookmark Course' or '⭐ Save to My Library' on any page to pin it here.")
    else:
        for idx, item in enumerate(saved, 1):
            with st.container():
                st.markdown(f"""
                <div class="research-card">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #ffffff;">{idx}. {item}</div>
                    <div style="font-size: 0.8rem; color: #a5a1c9; margin-top: 4px;">Pinned to your personal Aspira collection.</div>
                </div>
                """, unsafe_allow_html=True)
                
                c_open, c_remove, _ = st.columns([1.5, 1.5, 4])
                with c_open:
                    if st.button("Open Guide ➔", key=f"open_saved_{idx}"):
                        clean_name = item.replace("Project: ", "")
                        if "Project:" in item:
                            st.session_state["prefill_project_idea"] = clean_name
                            st.session_state["nav_index"] = 2
                        else:
                            st.session_state["active_subject_view"] = clean_name
                            st.session_state["nav_index"] = 0
                        st.rerun()
                with c_remove:
                    if st.button("Remove", key=f"remove_saved_{idx}"):
                        st.session_state["saved_bookmarks"].remove(item)
                        st.rerun()
                st.write("")
