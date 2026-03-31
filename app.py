import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="UmpCompanion",
    page_icon="🧢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Session State
# -----------------------------
if "checked_in" not in st.session_state:
    st.session_state.checked_in = False
if "check_in_time" not in st.session_state:
    st.session_state.check_in_time = None
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "first_pitch_time" not in st.session_state:
    st.session_state.first_pitch_time = None
if "weather_status" not in st.session_state:
    st.session_state.weather_status = "clear"

# -----------------------------
# Static demo values
# -----------------------------
current_time = datetime.now()
game_site = "Field 7 • Saratoga Springs"
assignment = "Varsity High School"
ruleset = "NFHS Varsity"
partner_eta = "6 Minutes"
weather_temp = "68°F"
weather_summary = "Clear"
lightning_risk = "No Lightning"

# Demo game time set for today at 4:00 PM
game_time = current_time.replace(hour=16, minute=0, second=0, microsecond=0)
if current_time.hour >= 18:
    game_time = game_time + timedelta(days=1)

plate_meeting_time = game_time - timedelta(minutes=15)

# -----------------------------
# Helpers
# -----------------------------
def format_dt(dt):
    if not dt:
        return "—"
    return dt.strftime("%I:%M %p").lstrip("0")

def format_td(td):
    total_seconds = max(0, int(td.total_seconds()))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"

plate_meeting_countdown = plate_meeting_time - current_time
first_pitch_countdown = game_time - current_time

# -----------------------------
# CSS
# -----------------------------
st.html("""
<style>
:root {
    --navy: #06101A;
    --navy-2: #0B1726;
    --navy-3: #102338;
    --panel: rgba(15, 24, 37, 0.88);
    --panel-2: rgba(18, 31, 48, 0.94);
    --panel-3: rgba(12, 22, 34, 0.98);
    --ink: #F8F4EA;
    --muted: #A9BACC;
    --line: rgba(155, 178, 205, 0.16);
    --blue: #67B5FF;
    --blue-2: #2B80F7;
    --green: #1E8E5A;
    --green-2: #27C174;
    --green-3: #A7FFD0;
    --red: #D83535;
    --red-2: #FF6A6F;
    --clay: #B85E2F;
    --gold: #E3B861;
    --gold-2: #FFD981;
    --ice: #DFECF9;
    --shadow: 0 14px 38px rgba(0,0,0,.32);
    --shadow-soft: 0 10px 26px rgba(0,0,0,.22);
    --glow-blue: 0 0 0 1px rgba(103,181,255,.20), 0 0 32px rgba(43,128,247,.14);
    --glow-gold: 0 0 0 1px rgba(227,184,97,.18), 0 0 24px rgba(227,184,97,.12);
    --glow-green: 0 0 0 1px rgba(39,193,116,.20), 0 0 22px rgba(39,193,116,.12);
}

.stApp {
    background:
        radial-gradient(circle at 7% 10%, rgba(103,181,255,.12), transparent 18%),
        radial-gradient(circle at 92% 8%, rgba(184,94,47,.10), transparent 16%),
        radial-gradient(circle at 50% 100%, rgba(39,193,116,.06), transparent 20%),
        linear-gradient(180deg, #06101A 0%, #08131F 45%, #091522 100%);
    color: var(--ink);
}

.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    width: 320px;
    height: 320px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    opacity: .05;
}
.stApp::before {
    top: 120px;
    left: -160px;
    border: 2px dashed rgba(248,244,234,.24);
}
.stApp::after {
    bottom: -120px;
    right: -150px;
    border: 2px dashed rgba(248,244,234,.18);
}

.block-container {
    position: relative;
    z-index: 1;
    max-width: 1500px;
    padding-top: 0.8rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    letter-spacing: -0.02em;
    color: white;
}
p, div, span, label {
    letter-spacing: 0.01em;
}

.hero {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(135deg, rgba(255,255,255,.055), rgba(255,255,255,.012)),
        linear-gradient(115deg, #0A1726 0%, #102338 48%, #16395E 78%, #19334F 100%);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 24px;
    padding: 22px 24px 20px 24px;
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
        rgba(255,255,255,.018) 13px,
        rgba(255,255,255,.018) 15px
      );
    pointer-events: none;
}
.hero::after {
    content: "";
    position: absolute;
    right: -65px;
    top: -65px;
    width: 220px;
    height: 220px;
    background: radial-gradient(circle, rgba(227,184,97,.16), transparent 60%);
    pointer-events: none;
}
.hero-kicker {
    color: #C7D6E8;
    font-size: .72rem;
    text-transform: uppercase;
    letter-spacing: .18em;
    font-weight: 900;
    margin-bottom: 8px;
}
.hero-topline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    flex-wrap: wrap;
}
.hero h1 {
    margin: 0;
    font-size: 2.15rem;
    line-height: 1.02;
}
.hero-live {
    background: linear-gradient(90deg, rgba(227,184,97,.18), rgba(255,255,255,.06));
    border: 1px solid rgba(255,255,255,.12);
    color: #FFF4D6;
    border-radius: 999px;
    padding: 9px 14px;
    font-weight: 900;
    font-size: .84rem;
    box-shadow: var(--glow-gold);
}
.hero p {
    margin: 10px 0 0 0;
    color: #E2ECF7;
    font-size: 1rem;
    max-width: 980px;
}
.hero-badges {
    margin-top: 14px;
    display: flex;
    gap: 9px;
    flex-wrap: wrap;
}
.hero-badge {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.10);
    color: #FAFCFF;
    padding: 8px 12px;
    border-radius: 999px;
    font-size: .80rem;
    font-weight: 800;
    box-shadow: var(--shadow-soft);
}

.command-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin: 6px 0 14px 0;
}
.command-pill {
    background: linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 13px 14px;
    box-shadow: var(--shadow-soft);
}
.command-k {
    color: #AFC0D3;
    text-transform: uppercase;
    letter-spacing: .14em;
    font-size: .66rem;
    font-weight: 900;
    margin-bottom: 5px;
}
.command-v {
    color: #FFF;
    font-size: 1rem;
    font-weight: 900;
    line-height: 1.2;
}
.command-v.green { color: #94F0BD; }
.command-v.blue { color: #A5D2FF; }
.command-v.gold { color: #FFD981; }

.panel {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(180deg, rgba(255,255,255,.045), rgba(255,255,255,.018)),
        linear-gradient(180deg, rgba(17,28,43,.92), rgba(13,22,34,.92));
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 18px;
    box-shadow: var(--shadow);
}
.panel::before {
    content: "";
    position: absolute;
    inset: 0 0 auto 0;
    height: 3px;
    background: linear-gradient(90deg, var(--gold), var(--blue));
    opacity: .95;
}
.panel-title {
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .16em;
    font-size: .70rem;
    font-weight: 900;
    margin-bottom: 10px;
}
.panel-big {
    color: white;
    font-size: 1.3rem;
    font-weight: 900;
    line-height: 1.15;
}
.panel-sub {
    color: #C9D8E8;
    font-size: .95rem;
    margin-top: 7px;
}
.status-pill {
    display: inline-block;
    margin-top: 10px;
    padding: 7px 12px;
    border-radius: 999px;
    font-size: .76rem;
    font-weight: 900;
    background: rgba(39,193,116,.13);
    color: var(--green-3);
    border: 1px solid rgba(39,193,116,.34);
    box-shadow: var(--glow-green);
}
.status-pill.warn {
    background: rgba(227,184,97,.12);
    color: #FFE39C;
    border: 1px solid rgba(227,184,97,.34);
    box-shadow: var(--glow-gold);
}
.status-pill.alert {
    background: rgba(216,53,53,.14);
    color: #FFC1C1;
    border: 1px solid rgba(216,53,53,.34);
    box-shadow: 0 0 0 1px rgba(216,53,53,.18), 0 0 22px rgba(216,53,53,.12);
}

.ticker-shell {
    margin: 14px 0 16px 0;
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
    animation: ticker-scroll 120s linear infinite;
    will-change: transform;
}
.ticker-content {
    display: inline-flex;
    align-items: center;
    gap: 0;
    padding: 13px 0;
}
.ticker-item {
    color: #F8FBFF;
    font-weight: 800;
    font-size: .92rem;
    letter-spacing: .01em;
}
.ticker-sep {
    color: #8EC2FF;
    opacity: .95;
    padding: 0 20px;
    font-weight: 900;
}
@keyframes ticker-scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

.quick-actions-wrap {
    margin: 8px 0 14px 0;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    margin-bottom: 6px;
}
.stTabs [data-baseweb="tab"] {
    background: linear-gradient(180deg, rgba(17,28,43,.92), rgba(14,24,37,.92));
    border: 1px solid var(--line);
    border-radius: 15px;
    padding: 11px 18px;
    color: #DCE6F2;
    font-weight: 900;
    box-shadow: var(--shadow-soft);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, #17406B, #245B94) !important;
    border-color: rgba(103,181,255,.42) !important;
    color: white !important;
    box-shadow: var(--glow-blue);
}

textarea, input, select {
    border-radius: 14px !important;
}
div[data-baseweb="textarea"] textarea,
div[data-baseweb="input"] input,
div[data-baseweb="select"] > div {
    background: rgba(10,19,31,.74) !important;
    color: #F5F8FC !important;
    border: 1px solid rgba(143,170,203,.18) !important;
}

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

div[data-testid="stAlert"] {
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,.08);
    box-shadow: var(--shadow-soft);
}

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

.app-footer {
    margin-top: 18px;
    color: #A9B9CA;
    font-size: .88rem;
    text-align: center;
    padding-bottom: 10px;
    letter-spacing: .01em;
}

@media (max-width: 1100px) {
    .command-strip {
        grid-template-columns: repeat(2, 1fr);
    }
}
@media (max-width: 700px) {
    .command-strip {
        grid-template-columns: repeat(2, 1fr);
    }
    .hero h1 {
        font-size: 1.82rem;
    }
    .ticker-label {
        padding: 0 12px;
    }
    .hero {
        padding: 18px 18px 16px 18px;
    }
}
</style>
""")

# -----------------------------
# Weather alert presentation
# -----------------------------
weather_map = {
    "clear": {
        "title": "Clear / Playable",
        "pill_class": "status-pill",
        "pill_text": "Playable conditions",
        "alert_func": "success",
        "alert_text": "Radar clear in this prototype view. No lightning concern at first pitch."
    },
    "caution": {
        "title": "Weather Caution",
        "pill_class": "status-pill warn",
        "pill_text": "Monitor conditions",
        "alert_func": "warning",
        "alert_text": "Weather caution mode active. Radar monitoring recommended and crew should stay alert."
    },
    "lightning": {
        "title": "Lightning Alert",
        "pill_class": "status-pill alert",
        "pill_text": "Suspend play / clear field",
        "alert_func": "error",
        "alert_text": "Lightning alert mode active. Suspend play, clear the field, and begin your delay protocol."
    }
}
weather_state = weather_map[st.session_state.weather_status]

# -----------------------------
# Hero
# -----------------------------
st.html("""
<div class="hero">
    <div class="hero-kicker">Elite Officiating Operations Platform</div>
    <div class="hero-topline">
        <h1>🧢 UmpCompanion</h1>
        <div class="hero-live">● LIVE GAME DAY MODE</div>
    </div>
    <p>
        Professional game-day support for serious baseball umpires — plate meeting readiness,
        live crew coordination, weather awareness, rules support, safety workflows, and clean
        game management in one polished command center.
    </p>
    <div class="hero-badges">
        <div class="hero-badge">NFHS / NCAA / OBR Ready</div>
        <div class="hero-badge">Game Check-In</div>
        <div class="hero-badge">Weather + Lightning Workflow</div>
        <div class="hero-badge">Live Game Clock</div>
    </div>
</div>
""")

# -----------------------------
# Compact command strip
# -----------------------------
st.html(f"""
<div class="command-strip">
    <div class="command-pill">
        <div class="command-k">Assignment</div>
        <div class="command-v gold">{assignment} • 4:00 PM</div>
    </div>
    <div class="command-pill">
        <div class="command-k">Site</div>
        <div class="command-v">{game_site}</div>
    </div>
    <div class="command-pill">
        <div class="command-k">Partner</div>
        <div class="command-v green">ETA {partner_eta}</div>
    </div>
    <div class="command-pill">
        <div class="command-k">Weather / Ruleset</div>
        <div class="command-v blue">{weather_temp} • {weather_summary} • NFHS</div>
    </div>
</div>
""")

# -----------------------------
# Ticker
# -----------------------------
ticker_content = f"""
<span class="ticker-item">📍 Assignment loaded: {assignment} at 4:00 PM</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">🧢 Plate meeting target: {format_dt(plate_meeting_time)}</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">🌤️ Weather: {weather_temp} • {weather_summary} • {lightning_risk}</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">✅ Crew status: partner ETA {partner_eta}</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">📖 Ruleset loaded: {ruleset}</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">🚨 Safety workflows armed and ready</span>
<span class="ticker-sep">•</span>
"""

st.html(f"""
<div class="ticker-shell">
    <div class="ticker-label"><span class="ticker-label-dot"></span> Live Feed</div>
    <div class="ticker-window">
        <div class="ticker-track">
            <div class="ticker-content">{ticker_content}</div>
            <div class="ticker-content">{ticker_content}</div>
        </div>
    </div>
</div>
""")

# -----------------------------
# Top row: Plate Meeting / Weather / Game Clock
# -----------------------------
top1, top2, top3 = st.columns(3)

with top1:
    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">Plate Meeting + Check-In</div>
        <div class="panel-big">{assignment} • 4:00 PM</div>
        <div class="panel-sub">{game_site}</div>
        <div class="panel-sub">Plate Meeting: {format_dt(plate_meeting_time)} • First Pitch: {format_dt(game_time)}</div>
        <div class="status-pill">Meeting in {format_td(plate_meeting_countdown)}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Check In", use_container_width=True):
            st.session_state.checked_in = True
            st.session_state.check_in_time = datetime.now()
    with c2:
        if st.button("📍 Navigate", use_container_width=True):
            st.info("Opening exact field pin with preferred parking approach.")

    if st.session_state.checked_in:
        st.success(f"Checked in at {format_dt(st.session_state.check_in_time)}. Admin can now see arrival status.")
    else:
        st.info("Not checked in yet. Tap check-in on arrival so admin sees live status.")

with top2:
    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">Live Weather Alert</div>
        <div class="panel-big">{weather_temp} • {weather_summary}</div>
        <div class="panel-sub">Radar-ready status tile for lightning and delay workflows.</div>
        <div class="{weather_state['pill_class']}">{weather_state['pill_text']}</div>
    </div>
    """, unsafe_allow_html=True)

    w1, w2, w3 = st.columns(3)
    with w1:
        if st.button("Clear", key="weather_clear", use_container_width=True):
            st.session_state.weather_status = "clear"
    with w2:
        if st.button("Caution", key="weather_caution", use_container_width=True):
            st.session_state.weather_status = "caution"
    with w3:
        if st.button("Lightning", key="weather_lightning", use_container_width=True):
            st.session_state.weather_status = "lightning"

    getattr(st, weather_map[st.session_state.weather_status]["alert_func"])(
        weather_map[st.session_state.weather_status]["alert_text"]
    )
    st.caption("Tonight’s prototype uses manual weather modes. Next step: hook to a live radar/weather API and trigger automated alerts.")

with top3:
    selected_limit = st.selectbox(
        "Game Time Limit",
        ["1:45", "2:00", "2:10"],
        index=1,
        key="game_limit"
    )

    limits = {
        "1:45": 105,
        "2:00": 120,
        "2:10": 130
    }
    selected_minutes = limits[selected_limit]

    st.markdown("""
    <div class="panel">
        <div class="panel-title">Game Clock</div>
        <div class="panel-big">Start on First Pitch</div>
        <div class="panel-sub">Track elapsed game time and know when you’re nearing the cap.</div>
    </div>
    """, unsafe_allow_html=True)

    gc1, gc2 = st.columns(2)
    with gc1:
        if st.button("⏱️ Start Game", use_container_width=True):
            st.session_state.game_started = True
            st.session_state.first_pitch_time = datetime.now()
    with gc2:
        if st.button("↺ Reset Clock", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.first_pitch_time = None

    if st.session_state.game_started and st.session_state.first_pitch_time:
        elapsed = datetime.now() - st.session_state.first_pitch_time
        remaining = timedelta(minutes=selected_minutes) - elapsed
        st.metric("Elapsed", format_td(elapsed))
        st.metric("Remaining", format_td(remaining))
        if remaining.total_seconds() <= 0:
            st.error("Time limit reached.")
        elif remaining.total_seconds() <= 900:
            st.warning("Final 15 minutes of game limit.")
        else:
            st.success("Clock running inside time window.")
        st.caption(f"First pitch logged at {format_dt(st.session_state.first_pitch_time)}")
    else:
        st.metric("Elapsed", "00:00")
        st.metric("Remaining", f"{selected_minutes}:00")
        st.info("Clock not started yet. Tap Start Game on first pitch.")

# -----------------------------
# Quick action row
# -----------------------------
st.markdown('<div class="quick-actions-wrap">', unsafe_allow_html=True)
qa1, qa2, qa3 = st.columns(3)
with qa1:
    if st.button("📖 Instant Ruling", use_container_width=True):
        st.toast("Rule Advisor is ready below.")
with qa2:
    if st.button("⚠️ Emergency Alert", use_container_width=True):
        st.error("Emergency alert workflow triggered for assignor and safety contact.")
with qa3:
    if st.button("📝 Incident Report", use_container_width=True):
        st.success("Incident report workflow opened.")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs(["📖 Rule Advisor", "⚾ Game Day Toolkit", "💬 Crew Chat & Tracker"])

with tab1:
    st.subheader("Instant Rule Advisor")
    st.caption("Current profile auto-loaded: Varsity High School Baseball • NFHS")

    left, right = st.columns([1.35, 1])

    with left:
        situation = st.text_area(
            "Describe the play:",
            "Runner on first, ground ball to shortstop. Fielder obstructs the runner.",
            height=150,
            placeholder="Example: R1 stealing, throw from catcher pulls F6 into the baseline..."
        )

        if st.button("Get Exact Ruling", key="ruling_btn", use_container_width=True):
            st.markdown("""
            <div class="panel" style="margin-top:10px;">
                <div class="panel-title">Rule Result</div>
                <div class="panel-big">NFHS Rule 2-32 — Obstruction</div>
                <div class="panel-sub">
                    Immediate dead ball on Type A obstruction when a play is being made on the obstructed runner.
                    Award the obstructed runner at least one base beyond the base they would have reached without obstruction.
                    Place all other runners accordingly.
                </div>
                <div class="status-pill">High-confidence ruling delivered</div>
            </div>
            """, unsafe_allow_html=True)
            st.success("Ruling returned fast — clean, clear, and field-usable.")

    with right:
        st.metric("Most Common Call Tonight", "Obstruction / Interference")
        st.metric("Rulebook Loaded", "NFHS")
        st.metric("Confidence Mode", "High")
        st.info("Game note: kill the play decisively, then verbalize obstruction separately from interference so coaches hear command, not confusion.")

with tab2:
    st.subheader("Game Day Toolkit")

    top_a, top_b, top_c = st.columns(3)
    with top_a:
        if st.button("📍 Open Field Navigation", use_container_width=True):
            st.info("Opening exact field pin with preferred parking approach.")
    with top_b:
        if st.button("🔄 Find Replacement Umpire", use_container_width=True):
            st.info("Nearest qualified official pinged. Assignor copied.")
    with top_c:
        if st.button("📞 Contact Crew Chief", use_container_width=True):
            st.success("Crew communication lane opened.")

    d1, d2 = st.columns(2)
    with d1:
        if st.button("🚨 Trigger Emergency Workflow", use_container_width=True):
            st.error("Immediate alert sent to assignor, safety contact, and emergency workflow.")
    with d2:
        if st.button("🧾 Generate Incident Report", use_container_width=True):
            st.success("Professional incident report created and ready for review.")

    st.markdown("")
    st.subheader("Live Game Counter")
    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Balls", "2")
    g2.metric("Strikes", "1")
    g3.metric("Outs", "0")
    g4.metric("Pitch Count", "47")

    st.caption("This section can later become a larger one-tap mobile field view for quick use between pitches.")

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

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## UmpCompanion")
    st.caption("Game-day operations for working umpires and associations")

    st.markdown("""
    <div class="sidebar-box">
        <div class="sidebar-title">Live Status</div>
        <div class="small-note">
            Assignment: Varsity HS • 4:00 PM<br>
            Site: Field 7 • Saratoga Springs<br>
            Ruleset: NFHS Varsity<br>
            Check-In: READY
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-box">
        <div class="sidebar-title">Tonight's Demo Strengths</div>
        <div class="small-note">
            Plate meeting readiness • live check-in • weather alert workflow • game clock • context-aware rules • incident + emergency actions
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "• Context-aware rule lookup\n"
        "• One-tap safety workflows\n"
        "• Crew coordination tools\n"
        "• Check-in visibility\n"
        "• Game time tracking"
    )

# -----------------------------
# Footer
# -----------------------------
st.html("""
<div class="app-footer">
    UmpCompanion live prototype • game-day command center • built for serious baseball operations
</div>
""")