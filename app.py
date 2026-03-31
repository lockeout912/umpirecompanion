import streamlit as st

st.set_page_config(
    page_title="UmpCompanion",
    page_icon="🧢",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.html("""
<style>
:root {
    --navy: #08131F;
    --navy-2: #0E1724;
    --panel: #111C2B;
    --panel-2: #162538;
    --ink: #F5F0E6;
    --muted: #9FB0C3;
    --line: #243244;
    --blue: #7FB3FF;
    --green: #1F6F50;
    --red: #C62828;
    --clay: #A8572A;
    --gold: #D6B25E;
    --shadow: 0 10px 30px rgba(0,0,0,.28);
}

/* App shell */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(127,179,255,.08), transparent 25%),
        radial-gradient(circle at top right, rgba(168,87,42,.08), transparent 22%),
        linear-gradient(180deg, #08131F 0%, #0B1624 100%);
    color: var(--ink);
}

/* Main width */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(135deg, rgba(255,255,255,.03), rgba(255,255,255,.01)),
        linear-gradient(90deg, #0C1A2A 0%, #13233A 55%, #1B314F 100%);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 22px;
    padding: 26px 28px;
    box-shadow: var(--shadow);
    margin-bottom: 14px;
}
.hero:before {
    content: "";
    position: absolute;
    inset: 0;
    background:
      repeating-linear-gradient(
        -45deg,
        transparent 0px,
        transparent 14px,
        rgba(255,255,255,.015) 14px,
        rgba(255,255,255,.015) 16px
      );
    pointer-events: none;
}
.hero-kicker {
    color: #B8C7D9;
    font-size: .78rem;
    text-transform: uppercase;
    letter-spacing: .16em;
    font-weight: 700;
    margin-bottom: 8px;
}
.hero h1 {
    margin: 0;
    font-size: 2.1rem;
    line-height: 1.05;
    color: white;
}
.hero p {
    margin: 10px 0 0 0;
    color: #DDE7F2;
    font-size: 1rem;
    max-width: 900px;
}
.hero-badges {
    margin-top: 16px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.hero-badge {
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.09);
    color: #F8FAFC;
    padding: 8px 12px;
    border-radius: 999px;
    font-size: .82rem;
    font-weight: 600;
}

/* Ticker */
.ticker-wrap {
    margin: 10px 0 18px 0;
    border-radius: 16px;
    background: linear-gradient(90deg, #12243A, #173255);
    border: 1px solid rgba(255,255,255,.08);
    box-shadow: var(--shadow);
    overflow: hidden;
}
.ticker-label {
    display: inline-block;
    background: #A8572A;
    color: white;
    font-weight: 800;
    padding: 12px 14px;
    letter-spacing: .06em;
    font-size: .78rem;
    text-transform: uppercase;
}
.ticker {
    display: inline-block;
    white-space: nowrap;
    min-width: calc(100% - 120px);
    color: #F8FAFC;
    padding: 12px 0;
    font-weight: 600;
}
.ticker-track {
    display: inline-block;
    padding-left: 100%;
    animation: scroll-left 28s linear infinite;
}
@keyframes scroll-left {
    0% { transform: translateX(0); }
    100% { transform: translateX(-100%); }
}

/* Cards */
.uc-card {
    background: linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,.01));
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 18px 18px 16px;
    box-shadow: var(--shadow);
    min-height: 122px;
}
.uc-label {
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .14em;
    font-size: .72rem;
    font-weight: 800;
    margin-bottom: 10px;
}
.uc-value {
    color: white;
    font-size: 1.18rem;
    font-weight: 800;
    line-height: 1.2;
}
.uc-sub {
    color: #C5D2E0;
    font-size: .92rem;
    margin-top: 6px;
}

/* Rule result box */
.rule-box {
    background: linear-gradient(180deg, rgba(31,111,80,.18), rgba(31,111,80,.08));
    color: #F3FBF7;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(31,111,80,.55);
    border-left: 6px solid #2DAA73;
    box-shadow: var(--shadow);
}

/* Streamlit tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background: #101C2B;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 10px 16px;
    color: #DCE6F2;
    font-weight: 700;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, #163150, #1E4570);
    border-color: #34699E !important;
    color: white !important;
}

/* Inputs */
textarea, input {
    border-radius: 14px !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 999px;
    padding: 0.85rem 1rem;
    font-weight: 800;
    border: 1px solid transparent;
    transition: all .18s ease;
    box-shadow: 0 6px 18px rgba(0,0,0,.22);
}
.stButton > button:hover {
    transform: translateY(-2px);
    filter: brightness(1.05);
}

/* Optional role classes for HTML-based action blocks */
.action-row {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-top: 8px;
}

/* Sidebar polish */
section[data-testid="stSidebar"] {
    border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1rem;
}
.sidebar-box {
    background: linear-gradient(180deg, #132033, #101A29);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 16px;
    box-shadow: var(--shadow);
    margin-bottom: 12px;
}
.sidebar-title {
    text-transform: uppercase;
    letter-spacing: .14em;
    font-size: .72rem;
    font-weight: 800;
    color: #AFC0D3;
    margin-bottom: 10px;
}
.small-note {
    color: #9FB0C3;
    font-size: .84rem;
}

/* Section spacing */
.section-gap {
    margin-top: 10px;
    margin-bottom: 12px;
}
</style>
""")

# HERO
st.html("""
<div class="hero">
    <div class="hero-kicker">Elite Officiating Operations Platform</div>
    <h1>🧢 UmpCompanion</h1>
    <p>
        Professional game-day support for serious baseball umpires — rules, crew tools,
        assignment visibility, safety workflows, and certification tracking in one clean command center.
    </p>
    <div class="hero-badges">
        <div class="hero-badge">NFHS / NCAA / OBR Ready</div>
        <div class="hero-badge">Fast Crew Communication</div>
        <div class="hero-badge">Incident & Safety Tools</div>
        <div class="hero-badge">Built to Scale for Associations</div>
    </div>
</div>
""")

# LIVE TICKER
st.html("""
<div class="ticker-wrap">
    <span class="ticker-label">Live Feed</span>
    <span class="ticker">
        <span class="ticker-track">
            🚨 2026 NFHS Rule Update: New Obstruction Clarification &nbsp;&nbsp;•&nbsp;&nbsp;
            📅 Annual Clinic This Saturday at 9:00 AM &nbsp;&nbsp;•&nbsp;&nbsp;
            🌤️ Today's Slate: Clear skies, low lightning risk &nbsp;&nbsp;•&nbsp;&nbsp;
            ✅ 14 umpires completed annual testing this week &nbsp;&nbsp;•&nbsp;&nbsp;
            💡 Pregame Focus: Partner positioning on rotations and trapped-ball communication
        </span>
    </span>
</div>
""")

# TOP STATUS ROW
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.html("""
    <div class="uc-card">
        <div class="uc-label">Today's Assignment</div>
        <div class="uc-value">Varsity HS • 4:00 PM</div>
        <div class="uc-sub">Field 7 • Saratoga Springs</div>
    </div>
    """)

with col2:
    st.html("""
    <div class="uc-card">
        <div class="uc-label">Crew Partner</div>
        <div class="uc-value">ETA 6 Minutes 🟢</div>
        <div class="uc-sub">Route active • parking side confirmed</div>
    </div>
    """)

with col3:
    st.html("""
    <div class="uc-card">
        <div class="uc-label">Weather Window</div>
        <div class="uc-value">68°F • Clear</div>
        <div class="uc-sub">No lightning concern at first pitch</div>
    </div>
    """)

with col4:
    st.html("""
    <div class="uc-card">
        <div class="uc-label">Ruleset Loaded</div>
        <div class="uc-value">NFHS</div>
        <div class="uc-sub">Varsity baseball profile active</div>
    </div>
    """)

st.markdown("")
tab1, tab2, tab3 = st.tabs(["📖 Rule Advisor", "⚾ Game Day Toolkit", "💬 Crew Chat & Tracker"])

with tab1:
    st.subheader("Instant Rule Advisor")
    st.caption("Current profile auto-loaded: Varsity High School Baseball • NFHS")

    left, right = st.columns([1.3, 1])

    with left:
        situation = st.text_area(
            "Describe the play:",
            "Runner on first, ground ball to shortstop. Fielder obstructs the runner.",
            height=140,
            placeholder="Example: R1 stealing, throw from catcher pulls F6 into the baseline..."
        )

        if st.button("Get Exact Ruling", key="ruling_btn", use_container_width=True):
            st.html("""
            <div class="rule-box">
                <strong>NFHS Rule 2-32 — Obstruction</strong><br><br>
                Immediate dead ball on Type A obstruction when a play is being made on the obstructed runner.<br><br>
                Award the obstructed runner at least one base beyond the base they would have reached without obstruction.<br>
                Place all other runners accordingly.
            </div>
            """)
            st.success("Ruling returned fast — clear, confident, and field-usable.")

    with right:
        st.metric("Most Common Call Tonight", "Obstruction / Interference")
        st.metric("Rulebook Loaded", "NFHS")
        st.metric("Confidence Mode", "High")
        st.info("Tip: show the dead-ball signal decisively, then separate obstruction from interference in your verbal explanation.")

with tab2:
    st.subheader("Game Day Toolkit")

    top_a, top_b, top_c = st.columns(3)
    with top_a:
        if st.button("📍 Navigate to Field", use_container_width=True):
            st.info("Opening exact field pin with preferred parking approach.")
    with top_b:
        if st.button("📝 Generate Incident Report", use_container_width=True):
            st.success("Professional PDF created and queued for send.")
    with top_c:
        if st.button("🔄 Find Replacement Umpire", use_container_width=True):
            st.info("Nearest qualified official pinged. Assignor copied.")

    danger_a, danger_b = st.columns([1, 1])
    with danger_a:
        if st.button("🚨 Emergency Alert", use_container_width=True):
            st.error("Immediate alert sent to Assignor, Safety Contact, and emergency workflow.")
    with danger_b:
        if st.button("📞 Contact Crew Chief", use_container_width=True):
            st.success("Crew channel opened.")

    st.markdown("")
    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Balls", "2")
    g2.metric("Strikes", "1")
    g3.metric("Outs", "0")
    g4.metric("Pitch Count", "47")

    st.caption("Live counter should eventually become a giant tap-friendly plate view for mobile use. Big, bold, no squinting nonsense.")

with tab3:
    st.subheader("Private Crew Chat")
    st.write("No scattered texts. No missed threads. One locked-in communication lane for the crew.")

    message = st.text_input("Type message to crew:")
    if st.button("Send Message", use_container_width=True):
        st.success("Message posted to crew channel.")

    st.markdown("")
    st.subheader("Certification Locker")
    c1, c2 = st.columns(2)
    with c1:
        st.success("2025 NFHS Annual Test: **92%** — Passed")
        st.write("Last clinic attendance: **March 28**")
    with c2:
        st.info("Plate mechanics review: current")
        st.write("Association profile: **active and eligible**")

    if st.button("Add Score / Mark Attendance", use_container_width=True):
        st.toast("Certification record updated.")

with st.sidebar:
    st.markdown("## UmpCompanion")
    st.caption("Built for associations, assignors, and working umpires")

    st.html("""
    <div class="sidebar-box">
        <div class="sidebar-title">Crew Control Panel</div>
        <div class="small-note">Fast access to rule help, safety workflows, crew communication, and assignment operations.</div>
    </div>
    """)

    st.success("Professional • Fast • Reliable")
    st.info(
        "• Context-aware rule lookup\n"
        "• One-tap safety & incident tools\n"
        "• Sub helper for assignors\n"
        "• Private crew chat\n"
        "• Certification tracking"
    )

    st.html("""
    <div class="sidebar-box">
        <div class="sidebar-title">Next-Level Additions</div>
        <div class="small-note">
            GPS arrival check-in • crew availability board • weather radar tile • lightning timer • digital lineup card • ejection log • association analytics
        </div>
    </div>
    """)

st.caption("Live demo build • premium baseball operations aesthetic • ready to impress your assignor without looking like a science fair project")