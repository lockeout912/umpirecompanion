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
    --navy: #07111B;
    --navy-2: #0B1726;
    --navy-3: #102338;
    --panel: rgba(17, 28, 43, 0.84);
    --panel-2: rgba(22, 37, 56, 0.92);
    --panel-3: rgba(15, 25, 39, 0.96);
    --ink: #F8F4EA;
    --muted: #9FB0C3;
    --line: rgba(143, 170, 203, 0.18);
    --blue: #66B3FF;
    --blue-2: #2D7FF9;
    --green: #1E8E5A;
    --green-2: #23B26D;
    --red: #C62828;
    --red-2: #FF5A5F;
    --clay: #B85E2F;
    --gold: #E0B45C;
    --gold-2: #F7D27A;
    --ice: #DCEBFA;
    --shadow: 0 14px 38px rgba(0,0,0,.30);
    --shadow-soft: 0 10px 24px rgba(0,0,0,.20);
    --glow-blue: 0 0 0 1px rgba(102,179,255,.18), 0 0 30px rgba(45,127,249,.12);
    --glow-gold: 0 0 0 1px rgba(224,180,92,.18), 0 0 24px rgba(224,180,92,.10);
}

/* App shell */
.stApp {
    background:
        radial-gradient(circle at 8% 10%, rgba(102,179,255,.14), transparent 18%),
        radial-gradient(circle at 92% 8%, rgba(184,94,47,.12), transparent 16%),
        radial-gradient(circle at 50% 100%, rgba(35,178,109,.07), transparent 20%),
        linear-gradient(180deg, #06101A 0%, #091320 50%, #0A1522 100%);
    color: var(--ink);
}

/* subtle baseball seam accents */
.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    width: 340px;
    height: 340px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    opacity: .055;
    filter: blur(.2px);
}
.stApp::before {
    top: 110px;
    left: -170px;
    border: 2px dashed rgba(248,244,234,.28);
}
.stApp::after {
    bottom: -140px;
    right: -150px;
    border: 2px dashed rgba(248,244,234,.22);
}

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1520px;
}

/* Global typography polish */
h1, h2, h3 {
    letter-spacing: -0.02em;
}
p, div, span, label {
    letter-spacing: 0.01em;
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(135deg, rgba(255,255,255,.06), rgba(255,255,255,.015)),
        linear-gradient(115deg, #0A1726 0%, #11243A 48%, #193C63 78%, #1A3654 100%);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 26px;
    padding: 30px 30px 24px 30px;
    box-shadow: var(--shadow);
    margin-bottom: 12px;
}
.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
      repeating-linear-gradient(
        -45deg,
        transparent 0px,
        transparent 13px,
        rgba(255,255,255,.02) 13px,
        rgba(255,255,255,.02) 15px
      );
    pointer-events: none;
}
.hero::after {
    content: "";
    position: absolute;
    right: -60px;
    top: -60px;
    width: 260px;
    height: 260px;
    background: radial-gradient(circle, rgba(224,180,92,.18), transparent 60%);
    pointer-events: none;
}
.hero-kicker {
    color: #C7D6E8;
    font-size: .78rem;
    text-transform: uppercase;
    letter-spacing: .18em;
    font-weight: 800;
    margin-bottom: 8px;
}
.hero-topline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
}
.hero h1 {
    margin: 0;
    font-size: 2.4rem;
    line-height: 1.02;
    color: white;
}
.hero-live {
    background: linear-gradient(90deg, rgba(224,180,92,.18), rgba(255,255,255,.06));
    border: 1px solid rgba(255,255,255,.10);
    color: #FFF4D6;
    border-radius: 999px;
    padding: 10px 14px;
    font-weight: 800;
    font-size: .86rem;
    box-shadow: var(--glow-gold);
}
.hero p {
    margin: 12px 0 0 0;
    color: #E2ECF7;
    font-size: 1.02rem;
    max-width: 960px;
}
.hero-badges {
    margin-top: 18px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.hero-badge {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.10);
    color: #FAFCFF;
    padding: 9px 13px;
    border-radius: 999px;
    font-size: .82rem;
    font-weight: 700;
    box-shadow: var(--shadow-soft);
}

/* Ops strip */
.ops-strip {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin: 4px 0 16px 0;
}
.ops-pill {
    background: linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 14px 16px;
    box-shadow: var(--shadow-soft);
}
.ops-k {
    color: #AFC0D3;
    text-transform: uppercase;
    letter-spacing: .14em;
    font-size: .68rem;
    font-weight: 800;
    margin-bottom: 6px;
}
.ops-v {
    color: #FFFFFF;
    font-size: 1rem;
    font-weight: 800;
    line-height: 1.2;
}
.ops-v.green { color: #7BE7A6; }
.ops-v.gold { color: #FFD981; }
.ops-v.blue { color: #99D0FF; }

/* Ticker */
.ticker-shell {
    margin: 12px 0 18px 0;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.09);
    background:
        linear-gradient(90deg, rgba(17,36,58,.96), rgba(21,45,74,.98) 45%, rgba(16,37,60,.96));
    box-shadow: var(--shadow);
    overflow: hidden;
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: stretch;
}
.ticker-label {
    display: flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(180deg, #B85E2F, #8F431D);
    color: white;
    font-weight: 900;
    padding: 0 18px;
    letter-spacing: .08em;
    font-size: .78rem;
    text-transform: uppercase;
    white-space: nowrap;
    border-right: 1px solid rgba(255,255,255,.08);
}
.ticker-label-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #FFD981;
    box-shadow: 0 0 12px rgba(255,217,129,.7);
}
.ticker-window {
    overflow: hidden;
    position: relative;
}
.ticker-track {
    display: flex;
    width: max-content;
    white-space: nowrap;
    animation: ticker-scroll 90s linear infinite;
    will-change: transform;
}
.ticker-content {
    display: inline-flex;
    align-items: center;
    gap: 0;
    padding: 14px 0;
}
.ticker-item {
    color: #F8FBFF;
    font-weight: 700;
    font-size: .94rem;
    letter-spacing: .01em;
}
.ticker-sep {
    color: #8EC2FF;
    opacity: .95;
    padding: 0 22px;
    font-weight: 900;
}
@keyframes ticker-scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

/* Cards */
.uc-card {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(180deg, rgba(255,255,255,.045), rgba(255,255,255,.018)),
        linear-gradient(180deg, rgba(17,28,43,.92), rgba(13,22,34,.92));
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 18px 18px 16px;
    box-shadow: var(--shadow);
    min-height: 130px;
}
.uc-card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, var(--gold), var(--blue));
    opacity: .92;
}
.uc-card:hover {
    transform: translateY(-2px);
    transition: .18s ease;
    box-shadow: 0 16px 40px rgba(0,0,0,.34);
}
.uc-label {
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .15em;
    font-size: .70rem;
    font-weight: 900;
    margin-bottom: 10px;
}
.uc-value {
    color: white;
    font-size: 1.18rem;
    font-weight: 900;
    line-height: 1.2;
}
.uc-sub {
    color: #C8D7E7;
    font-size: .92rem;
    margin-top: 7px;
}
.uc-status {
    display: inline-block;
    margin-top: 10px;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: .73rem;
    font-weight: 800;
    background: rgba(35,178,109,.12);
    color: #8EF0B6;
    border: 1px solid rgba(35,178,109,.26);
}

/* Rule result box */
.rule-box {
    background:
        linear-gradient(180deg, rgba(31,111,80,.22), rgba(31,111,80,.10)),
        linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
    color: #F3FBF7;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(31,111,80,.52);
    border-left: 6px solid #2DCC82;
    box-shadow: var(--shadow);
}

/* Panel wrappers */
.panel-wrap {
    background:
        linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.015));
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 18px;
    box-shadow: var(--shadow-soft);
    margin-top: 6px;
}

/* Streamlit tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    margin-bottom: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: linear-gradient(180deg, rgba(17,28,43,.92), rgba(14,24,37,.92));
    border: 1px solid var(--line);
    border-radius: 15px;
    padding: 11px 18px;
    color: #DCE6F2;
    font-weight: 800;
    box-shadow: var(--shadow-soft);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, #17406B, #245B94) !important;
    border-color: rgba(102,179,255,.42) !important;
    color: white !important;
    box-shadow: var(--glow-blue);
}

/* Inputs */
textarea, input {
    border-radius: 14px !important;
}
div[data-baseweb="textarea"] textarea,
div[data-baseweb="input"] input {
    background: rgba(10,19,31,.72) !important;
    color: #F5F8FC !important;
    border: 1px solid rgba(143,170,203,.18) !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 999px;
    padding: 0.92rem 1rem;
    font-weight: 900;
    letter-spacing: 0.01em;
    border: 1px solid rgba(255,255,255,.08);
    transition: all .18s ease;
    box-shadow: 0 8px 22px rgba(0,0,0,.24);
    background: linear-gradient(180deg, #215794, #173F6A);
    color: white;
}
.stButton > button:hover {
    transform: translateY(-2px);
    filter: brightness(1.06);
    box-shadow: 0 14px 28px rgba(0,0,0,.28);
}

/* Metrics */
div[data-testid="stMetric"] {
    background:
        linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.015)),
        linear-gradient(180deg, rgba(16,28,44,.96), rgba(11,20,31,.96));
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 14px 16px;
    box-shadow: var(--shadow-soft);
}
div[data-testid="stMetricLabel"] {
    color: #B4C5D7 !important;
    text-transform: uppercase;
    letter-spacing: .12em;
    font-size: .72rem !important;
    font-weight: 800 !important;
}
div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 900 !important;
}

/* Alerts / info polish */
div[data-testid="stAlert"] {
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,.08);
    box-shadow: var(--shadow-soft);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    border-right: 1px solid var(--line);
    background:
        linear-gradient(180deg, rgba(10,18,29,.98), rgba(8,15,24,.98)) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1rem;
}
.sidebar-box {
    background: linear-gradient(180deg, rgba(20,33,51,.92), rgba(14,23,36,.94));
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 16px;
    box-shadow: var(--shadow-soft);
    margin-bottom: 12px;
}
.sidebar-title {
    text-transform: uppercase;
    letter-spacing: .14em;
    font-size: .72rem;
    font-weight: 900;
    color: #B7C8DA;
    margin-bottom: 10px;
}
.small-note {
    color: #A2B3C5;
    font-size: .86rem;
    line-height: 1.45;
}

/* Footer caption */
.app-footer {
    margin-top: 18px;
    color: #A9B9CA;
    font-size: .88rem;
    text-align: center;
    padding-bottom: 10px;
    letter-spacing: .01em;
}

/* Responsive */
@media (max-width: 1100px) {
    .ops-strip {
        grid-template-columns: repeat(2, 1fr);
    }
}
@media (max-width: 700px) {
    .ops-strip {
        grid-template-columns: 1fr;
    }
    .hero h1 {
        font-size: 1.9rem;
    }
    .ticker-label {
        padding: 0 12px;
    }
}
</style>
""")

# HERO
st.html("""
<div class="hero">
    <div class="hero-kicker">Elite Officiating Operations Platform</div>
    <div class="hero-topline">
        <h1>🧢 UmpCompanion</h1>
        <div class="hero-live">● LIVE GAME DAY MODE</div>
    </div>
    <p>
        Professional game-day support for serious baseball umpires — rules, crew tools,
        assignment visibility, safety workflows, crew communication, and certification tracking
        in one polished command center.
    </p>
    <div class="hero-badges">
        <div class="hero-badge">NFHS / NCAA / OBR Ready</div>
        <div class="hero-badge">Live Crew Coordination</div>
        <div class="hero-badge">Incident & Safety Workflows</div>
        <div class="hero-badge">Association-Scale Ready</div>
    </div>
</div>
""")

# OPS STRIP
st.html("""
<div class="ops-strip">
    <div class="ops-pill">
        <div class="ops-k">Assignment</div>
        <div class="ops-v gold">Varsity HS • 4:00 PM</div>
    </div>
    <div class="ops-pill">
        <div class="ops-k">Site</div>
        <div class="ops-v">Field 7 • Saratoga Springs</div>
    </div>
    <div class="ops-pill">
        <div class="ops-k">Partner Status</div>
        <div class="ops-v green">ETA 6 Minutes</div>
    </div>
    <div class="ops-pill">
        <div class="ops-k">Weather</div>
        <div class="ops-v blue">68°F • Clear • No Lightning</div>
    </div>
    <div class="ops-pill">
        <div class="ops-k">Ruleset</div>
        <div class="ops-v">NFHS Loaded</div>
    </div>
</div>
""")

# CONTINUOUS TICKER
ticker_content = """
<span class="ticker-item">🚨 2026 NFHS Rule Update: New obstruction clarification in effect</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">📅 Annual mechanics clinic this Saturday at 9:00 AM</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">🌤️ Tonight’s slate: clear skies, low lightning risk across local fields</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">✅ 14 umpires completed annual certification this week</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">💡 Pregame point of emphasis: trapped-ball communication and rotations</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">🧭 Crew arrival window active: parking side confirmed for Field 7</span>
<span class="ticker-sep">•</span>
"""

st.html(f"""
<div class="ticker-shell">
    <div class="ticker-label"><span class="ticker-label-dot"></span> Live Feed</div>
    <div class="ticker-window">
        <div class="ticker-track">
            <div class="ticker-content">
                {ticker_content}
            </div>
            <div class="ticker-content">
                {ticker_content}
            </div>
        </div>
    </div>
</div>
""")

# TOP STATUS ROW
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.html("""
    <div class="uc-card">
        <div class="uc-label">Today's Assignment</div>
        <div class="uc-value">Varsity High School • 4:00 PM</div>
        <div class="uc-sub">Field 7 • Plate meeting in 42 minutes</div>
        <div class="uc-status">Ready for first pitch</div>
    </div>
    """)

with col2:
    st.html("""
    <div class="uc-card">
        <div class="uc-label">Crew Partner</div>
        <div class="uc-value">ETA 6 Minutes 🟢</div>
        <div class="uc-sub">Route active • parking side confirmed</div>
        <div class="uc-status">Crew arrival on pace</div>
    </div>
    """)

with col3:
    st.html("""
    <div class="uc-card">
        <div class="uc-label">Weather Window</div>
        <div class="uc-value">68°F • Clear</div>
        <div class="uc-sub">No lightning concern at first pitch</div>
        <div class="uc-status">Playable conditions</div>
    </div>
    """)

with col4:
    st.html("""
    <div class="uc-card">
        <div class="uc-label">Ruleset Loaded</div>
        <div class="uc-value">NFHS Varsity Profile</div>
        <div class="uc-sub">Context-aware rule support active</div>
        <div class="uc-status">Rule engine armed</div>
    </div>
    """)

st.markdown("")
tab1, tab2, tab3 = st.tabs(["📖 Rule Advisor", "⚾ Game Day Toolkit", "💬 Crew Chat & Tracker"])

with tab1:
    st.subheader("Instant Rule Advisor")
    st.caption("Current profile auto-loaded: Varsity High School Baseball • NFHS")

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown('<div class="panel-wrap">', unsafe_allow_html=True)

        situation = st.text_area(
            "Describe the play:",
            "Runner on first, ground ball to shortstop. Fielder obstructs the runner.",
            height=145,
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
            st.success("Ruling returned fast — clean, clear, and field-usable.")

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.metric("Most Common Call Tonight", "Obstruction / Interference")
        st.metric("Rulebook Loaded", "NFHS")
        st.metric("Confidence Mode", "High")
        st.info("Game note: kill the play decisively, then verbalize obstruction separately from interference so coaches hear command, not confusion.")

with tab2:
    st.subheader("Game Day Toolkit")

    top_a, top_b, top_c = st.columns(3)
    with top_a:
        if st.button("📍 Navigate to Field", use_container_width=True):
            st.info("Opening exact field pin with preferred parking approach.")
    with top_b:
        if st.button("📝 Generate Incident Report", use_container_width=True):
            st.success("Professional incident report created and ready for review.")
    with top_c:
        if st.button("🔄 Find Replacement Umpire", use_container_width=True):
            st.info("Nearest qualified official pinged. Assignor copied.")

    danger_a, danger_b = st.columns(2)
    with danger_a:
        if st.button("🚨 Emergency Alert", use_container_width=True):
            st.error("Immediate alert sent to Assignor, Safety Contact, and emergency workflow.")
    with danger_b:
        if st.button("📞 Contact Crew Chief", use_container_width=True):
            st.success("Crew communication lane opened.")

    st.markdown("")
    st.subheader("Live Game Counter")
    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Balls", "2")
    g2.metric("Strikes", "1")
    g3.metric("Outs", "0")
    g4.metric("Pitch Count", "47")

    st.caption("Designed to evolve into a larger tap-friendly field view for fast game use on mobile.")

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
    st.caption("Game-day operations for working umpires and associations")

    st.html("""
    <div class="sidebar-box">
        <div class="sidebar-title">Crew Control Panel</div>
        <div class="small-note">Fast access to rules support, safety workflows, communication, assignment operations, and live game status.</div>
    </div>
    """)

    st.success("Live • Fast • Professional")
    st.info(
        "• Context-aware rule lookup\n"
        "• One-tap safety & incident tools\n"
        "• Replacement helper for assignors\n"
        "• Private crew communication\n"
        "• Certification tracking"
    )

    st.html("""
    <div class="sidebar-box">
        <div class="sidebar-title">Operational Add-Ons</div>
        <div class="small-note">
            GPS arrival check-in • crew availability board • live radar tile • lightning delay timer • digital lineup card • ejection log • association analytics
        </div>
    </div>
    """)

st.html("""
<div class="app-footer">
    UmpCompanion live prototype • game-day command center • built for serious baseball operations
</div>
""")