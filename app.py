import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="UmpCompanion",
    page_icon="🧢",
    layout="wide",
    initial_sidebar_state="collapsed"
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
if "rule_result_visible" not in st.session_state:
    st.session_state.rule_result_visible = False
if "rule_result_title" not in st.session_state:
    st.session_state.rule_result_title = "NFHS Rule 2-32 — Obstruction"
if "rule_result_text" not in st.session_state:
    st.session_state.rule_result_text = (
        "Immediate dead ball on Type A obstruction when a play is being made on the obstructed runner. "
        "Award the obstructed runner at least one base beyond the base they would have reached without obstruction. "
        "Place all other runners accordingly."
    )
if "active_panel" not in st.session_state:
    st.session_state.active_panel = "rules"

# -----------------------------
# Static demo values
# -----------------------------
current_time = datetime.now()
assignment = "Varsity High School"
game_site = "Field 7 • Saratoga Springs"
ruleset = "NFHS Varsity"
partner_name = "Mike D."
partner_eta = "6 Minutes"
weather_temp = "68°F"
weather_summary = "Clear"
lightning_risk = "No Lightning"
crew_status = "Partner on pace"

org_message = "SBUO Reminder: polish shoes, clean hat, sharp plate conference presence."
nfhs_update = "NFHS Point of Emphasis: obstruction and slide rule communication."

# Demo game time set for today at 4:00 PM
game_time = current_time.replace(hour=16, minute=0, second=0, microsecond=0)
if current_time.hour >= 18:
    game_time = game_time + timedelta(days=1)

# Plate conference should be 5 minutes before game
plate_meeting_time = game_time - timedelta(minutes=5)

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

limits = {
    "1:45": 105,
    "2:00": 120,
    "2:10": 130
}
selected_limit = st.session_state.get("game_limit", "2:00")
selected_minutes = limits[selected_limit]

def get_plate_status(td):
    secs = td.total_seconds()
    if secs > 900:
        return ("On Track", "status-pill")
    elif secs > 0:
        return ("Late Risk", "status-pill warn")
    else:
        return ("Past Due", "status-pill alert")

plate_status_text, plate_status_class = get_plate_status(plate_meeting_countdown)

# -----------------------------
# Weather state
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
# CSS
# -----------------------------
st.markdown("""
<style>
:root {
    --navy: #06101A;
    --navy-2: #0B1726;
    --navy-3: #102338;
    --panel: rgba(15, 24, 37, 0.92);
    --panel-2: rgba(18, 31, 48, 0.96);
    --ink: #F8F4EA;
    --muted: #A9BACC;
    --line: rgba(155, 178, 205, 0.16);
    --blue: #67B5FF;
    --blue-2: #2B80F7;
    --green: #1E8E5A;
    --green-2: #27C174;
    --green-3: #A7FFD0;
    --red: #D83535;
    --gold: #E3B861;
    --gold-2: #FFD981;
    --shadow: 0 14px 38px rgba(0,0,0,.32);
    --shadow-soft: 0 10px 26px rgba(0,0,0,.22);
    --glow-blue: 0 0 0 1px rgba(103,181,255,.20), 0 0 28px rgba(43,128,247,.12);
    --glow-gold: 0 0 0 1px rgba(227,184,97,.18), 0 0 22px rgba(227,184,97,.10);
    --glow-green: 0 0 0 1px rgba(39,193,116,.20), 0 0 20px rgba(39,193,116,.12);
}

.stApp {
    background:
        radial-gradient(circle at 7% 10%, rgba(103,181,255,.10), transparent 18%),
        radial-gradient(circle at 92% 8%, rgba(184,94,47,.09), transparent 16%),
        radial-gradient(circle at 50% 100%, rgba(39,193,116,.05), transparent 20%),
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
    opacity: .04;
}
.stApp::before {
    top: 120px;
    left: -160px;
    border: 2px dashed rgba(248,244,234,.22);
}
.stApp::after {
    bottom: -120px;
    right: -150px;
    border: 2px dashed rgba(248,244,234,.16);
}

.block-container {
    position: relative;
    z-index: 1;
    max-width: 1460px;
    padding-top: 0.55rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    letter-spacing: -0.02em;
    color: white;
}
p, div, span, label {
    letter-spacing: 0.01em;
}

/* Header */
.header-shell {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(135deg, rgba(255,255,255,.05), rgba(255,255,255,.01)),
        linear-gradient(115deg, #0A1726 0%, #102338 50%, #16395E 78%, #19334F 100%);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 20px;
    padding: 14px 18px 13px 18px;
    box-shadow: var(--shadow);
    margin-bottom: 10px;
}
.header-shell::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
      repeating-linear-gradient(
        -45deg,
        transparent 0px,
        transparent 13px,
        rgba(255,255,255,.016) 13px,
        rgba(255,255,255,.016) 15px
      );
    pointer-events: none;
}
.header-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
}
.header-kicker {
    color: #C7D6E8;
    font-size: .66rem;
    text-transform: uppercase;
    letter-spacing: .18em;
    font-weight: 900;
    margin-bottom: 5px;
}
.header-title {
    margin: 0;
    font-size: 1.72rem;
    font-weight: 900;
    line-height: 1.02;
}
.header-live {
    background: linear-gradient(90deg, rgba(227,184,97,.18), rgba(255,255,255,.06));
    border: 1px solid rgba(255,255,255,.12);
    color: #FFF4D6;
    border-radius: 999px;
    padding: 7px 12px;
    font-weight: 900;
    font-size: .76rem;
    box-shadow: var(--glow-gold);
}
.header-sub {
    margin-top: 7px;
    color: #D9E4F0;
    font-size: .92rem;
}

/* Top snapshot */
.snapshot-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 9px;
    margin-bottom: 10px;
}
.snap {
    background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
    border: 1px solid var(--line);
    border-radius: 15px;
    padding: 11px 12px;
    box-shadow: var(--shadow-soft);
}
.snap-k {
    color: #AFC0D3;
    text-transform: uppercase;
    letter-spacing: .13em;
    font-size: .62rem;
    font-weight: 900;
    margin-bottom: 5px;
}
.snap-v {
    color: #FFF;
    font-size: .95rem;
    font-weight: 900;
    line-height: 1.15;
}
.snap-v.green { color: #94F0BD; }
.snap-v.blue { color: #A5D2FF; }
.snap-v.gold { color: #FFD981; }

/* Control center */
.control-center-title {
    color: #AFC0D3;
    text-transform: uppercase;
    letter-spacing: .16em;
    font-size: .66rem;
    font-weight: 900;
    margin: 2px 0 8px 0;
}
.control-row .stButton > button {
    min-height: 48px !important;
    padding: .55rem .75rem !important;
    font-size: .93rem !important;
    border-radius: 14px !important;
    background: linear-gradient(180deg, #235C97, #173F6A) !important;
    box-shadow: 0 6px 18px rgba(0,0,0,.22) !important;
}
.control-row .stButton > button:hover {
    transform: translateY(-1px);
    filter: brightness(1.05);
}

/* Banner */
.ticker-shell {
    margin: 10px 0 12px 0;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.09);
    background:
        linear-gradient(90deg, rgba(17,36,58,.96), rgba(21,45,74,.98) 45%, rgba(16,37,60,.96));
    box-shadow: var(--shadow-soft);
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
    padding: 0 16px;
    letter-spacing: .08em;
    font-size: .76rem;
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
    animation: ticker-scroll 88s linear infinite;
    will-change: transform;
}
.ticker-content {
    display: inline-flex;
    align-items: center;
    gap: 0;
    padding: 12px 0;
}
.ticker-item {
    color: #F8FBFF;
    font-weight: 800;
    font-size: .90rem;
    letter-spacing: .01em;
}
.ticker-sep {
    color: #8EC2FF;
    opacity: .95;
    padding: 0 18px;
    font-weight: 900;
}
@keyframes ticker-scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

/* Cards / panels */
.panel {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.018)),
        linear-gradient(180deg, rgba(17,28,43,.94), rgba(13,22,34,.94));
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 16px;
    box-shadow: var(--shadow-soft);
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
    font-size: .66rem;
    font-weight: 900;
    margin-bottom: 8px;
}
.panel-big {
    color: white;
    font-size: 1.15rem;
    font-weight: 900;
    line-height: 1.15;
}
.panel-sub {
    color: #C9D8E8;
    font-size: .91rem;
    margin-top: 6px;
}
.status-pill {
    display: inline-block;
    margin-top: 10px;
    padding: 7px 12px;
    border-radius: 999px;
    font-size: .75rem;
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
}

/* Inputs and buttons */
textarea, input, select {
    border-radius: 14px !important;
}
div[data-baseweb="textarea"] textarea,
div[data-baseweb="input"] input,
div[data-baseweb="select"] > div {
    background: rgba(10,19,31,.76) !important;
    color: #F5F8FC !important;
    border: 1px solid rgba(143,170,203,.18) !important;
}

.stButton > button {
    width: 100%;
    border-radius: 14px;
    padding: .72rem .9rem;
    font-weight: 900;
    letter-spacing: 0.01em;
    border: 1px solid rgba(255,255,255,.08);
    transition: all .18s ease;
    box-shadow: 0 8px 22px rgba(0,0,0,.22);
    background: linear-gradient(180deg, #215794, #173F6A);
    color: white;
}
.stButton > button:hover {
    transform: translateY(-1px);
    filter: brightness(1.05);
}

div[data-testid="stMetric"] {
    background:
        linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.015)),
        linear-gradient(180deg, rgba(16,28,44,.96), rgba(11,20,31,.96));
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 12px 14px;
    box-shadow: var(--shadow-soft);
}
div[data-testid="stMetricLabel"] {
    color: #B4C5D7 !important;
    text-transform: uppercase;
    letter-spacing: .12em;
    font-size: .66rem !important;
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
    display: none;
}

.footer-note {
    margin-top: 18px;
    color: #A9B9CA;
    font-size: .84rem;
    text-align: center;
}

@media (max-width: 1100px) {
    .snapshot-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}
@media (max-width: 700px) {
    .header-title {
        font-size: 1.45rem;
    }
    .snapshot-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .control-row .stButton > button {
        min-height: 44px !important;
        font-size: .88rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(f"""
<div class="header-shell">
    <div class="header-kicker">Game Day Command Center</div>
    <div class="header-top">
        <div>
            <div class="header-title">🧢 UmpCompanion</div>
        </div>
        <div class="header-live">● LIVE GAME DAY MODE</div>
    </div>
    <div class="header-sub">
        {assignment} • {game_site} • Partner ETA {partner_eta} • First Pitch {format_dt(game_time)}
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Top snapshot
# -----------------------------
check_in_text = (
    f"Checked in {format_dt(st.session_state.check_in_time)}"
    if st.session_state.checked_in and st.session_state.check_in_time
    else "Not checked in"
)

st.markdown(f"""
<div class="snapshot-grid">
    <div class="snap">
        <div class="snap-k">Assignment</div>
        <div class="snap-v gold">{assignment}</div>
    </div>
    <div class="snap">
        <div class="snap-k">Site</div>
        <div class="snap-v">{game_site}</div>
    </div>
    <div class="snap">
        <div class="snap-k">Partner</div>
        <div class="snap-v green">{partner_name} • ETA {partner_eta}</div>
    </div>
    <div class="snap">
        <div class="snap-k">Weather</div>
        <div class="snap-v blue">{weather_temp} • {weather_summary}</div>
    </div>
    <div class="snap">
        <div class="snap-k">Ruleset</div>
        <div class="snap-v">NFHS Varsity</div>
    </div>
    <div class="snap">
        <div class="snap-k">Check-In</div>
        <div class="snap-v">{check_in_text}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Compact control center
# -----------------------------
st.markdown('<div class="control-center-title">Control Center</div>', unsafe_allow_html=True)

st.markdown('<div class="control-row">', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    if st.button("📖 Rules", key="panel_rules", use_container_width=True):
        st.session_state.active_panel = "rules"
with c2:
    if st.button("✅ Check In", key="panel_checkin", use_container_width=True):
        st.session_state.checked_in = True
        st.session_state.check_in_time = datetime.now()
with c3:
    if st.button("📍 Navigate", key="panel_nav", use_container_width=True):
        st.info("Opening exact field pin with preferred parking approach.")
with c4:
    if st.button("⏱ Clock", key="panel_clock", use_container_width=True):
        st.session_state.active_panel = "clock"
with c5:
    if st.button("🌩 Weather", key="panel_weather", use_container_width=True):
        st.session_state.active_panel = "weather"
with c6:
    if st.button("🚨 Emergency", key="panel_emergency", use_container_width=True):
        st.session_state.active_panel = "emergency"
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Live organization banner
# -----------------------------
ticker_content = f"""
<span class="ticker-item">🌤 Current Weather: {weather_temp} • {weather_summary} • {lightning_risk}</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">📣 {org_message}</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">📖 NFHS Update: {nfhs_update}</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">🧢 Plate Conference Target: {format_dt(plate_meeting_time)}</span>
<span class="ticker-sep">•</span>
<span class="ticker-item">✅ Crew Status: {crew_status}</span>
<span class="ticker-sep">•</span>
"""

st.markdown(f"""
<div class="ticker-shell">
    <div class="ticker-label"><span class="ticker-label-dot"></span> Live Feed</div>
    <div class="ticker-window">
        <div class="ticker-track">
            <div class="ticker-content">{ticker_content}</div>
            <div class="ticker-content">{ticker_content}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Accountability + active panel row
# -----------------------------
left, right = st.columns([1.12, 1])

with left:
    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">Assignment Accountability</div>
        <div class="panel-big">{assignment} • {format_dt(game_time)}</div>
        <div class="panel-sub">{game_site}</div>
        <div class="panel-sub">Plate Conference: {format_dt(plate_meeting_time)} • First Pitch: {format_dt(game_time)}</div>
        <div class="{plate_status_class}">{plate_status_text} • Conference in {format_td(plate_meeting_countdown)}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.checked_in:
        st.success(f"Checked in at {format_dt(st.session_state.check_in_time)}. Admin can now see live arrival status.")
    else:
        st.info("Not checked in yet. Tap Check In on arrival so admin sees live status.")

    st.markdown("### 📖 Rule Lookup")
    situation = st.text_area(
        "Describe the play:",
        "Runner on first, ground ball to shortstop. Fielder obstructs the runner.",
        height=130,
        placeholder="Example: R1 stealing, throw from catcher pulls F6 into the baseline..."
    )

    if st.button("Get Exact Ruling", key="ruling_btn", use_container_width=True):
        st.session_state.active_panel = "rules"
        st.session_state.rule_result_visible = True
        st.session_state.rule_result_title = "NFHS Rule 2-32 — Obstruction"
        st.session_state.rule_result_text = (
            "Immediate dead ball on Type A obstruction when a play is being made on the obstructed runner. "
            "Award the obstructed runner at least one base beyond the base they would have reached without obstruction. "
            "Place all other runners accordingly."
        )

    if st.session_state.rule_result_visible:
        st.markdown(f"""
        <div class="panel" style="margin-top:10px;">
            <div class="panel-title">Rule Result</div>
            <div class="panel-big">{st.session_state.rule_result_title}</div>
            <div class="panel-sub">{st.session_state.rule_result_text}</div>
            <div class="status-pill">High-confidence ruling delivered</div>
        </div>
        """, unsafe_allow_html=True)

with right:
    active_panel = st.session_state.active_panel

    if active_panel == "weather":
        st.markdown(f"""
        <div class="panel">
            <div class="panel-title">Live Weather Alert</div>
            <div class="panel-big">{weather_temp} • {weather_summary}</div>
            <div class="panel-sub">Radar-ready tile for lightning and delay workflows.</div>
            <div class="{weather_state['pill_class']}">{weather_state['pill_text']}</div>
        </div>
        """, unsafe_allow_html=True)

        wc1, wc2, wc3 = st.columns(3)
        with wc1:
            if st.button("Clear", key="weather_clear", use_container_width=True):
                st.session_state.weather_status = "clear"
        with wc2:
            if st.button("Caution", key="weather_caution", use_container_width=True):
                st.session_state.weather_status = "caution"
        with wc3:
            if st.button("Lightning", key="weather_lightning", use_container_width=True):
                st.session_state.weather_status = "lightning"

        weather_state = weather_map[st.session_state.weather_status]
        getattr(st, weather_state["alert_func"])(weather_state["alert_text"])

        st.caption("Prototype mode uses manual weather states. Next step is a live radar/weather API with automated alerting.")

    elif active_panel == "clock":
        st.selectbox(
            "Game Time Limit",
            ["1:45", "2:00", "2:10"],
            index=["1:45", "2:00", "2:10"].index(selected_limit),
            key="game_limit"
        )
        selected_limit = st.session_state["game_limit"]
        selected_minutes = limits[selected_limit]

        st.markdown("""
        <div class="panel">
            <div class="panel-title">Game Clock</div>
            <div class="panel-big">Start on First Pitch</div>
            <div class="panel-sub">Track elapsed time and know when you’re nearing the cap.</div>
        </div>
        """, unsafe_allow_html=True)

        gc1, gc2 = st.columns(2)
        with gc1:
            if st.button("⏱ Start Game", key="clock_start", use_container_width=True):
                st.session_state.game_started = True
                st.session_state.first_pitch_time = datetime.now()
        with gc2:
            if st.button("↺ Reset Clock", key="clock_reset", use_container_width=True):
                st.session_state.game_started = False
                st.session_state.first_pitch_time = None

        if st.session_state.game_started and st.session_state.first_pitch_time:
            elapsed = datetime.now() - st.session_state.first_pitch_time
            remaining = timedelta(minutes=selected_minutes) - elapsed

            m1, m2 = st.columns(2)
            with m1:
                st.metric("Elapsed", format_td(elapsed))
            with m2:
                st.metric("Remaining", format_td(remaining))

            if remaining.total_seconds() <= 0:
                st.error("Time limit reached.")
            elif remaining.total_seconds() <= 900:
                st.warning("Final 15 minutes of game limit.")
            else:
                st.success("Clock running inside time window.")

            st.caption(f"First pitch logged at {format_dt(st.session_state.first_pitch_time)}")
        else:
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Elapsed", "00:00")
            with m2:
                st.metric("Remaining", f"{selected_minutes}:00")
            st.info("Clock not started yet. Tap Start Game on first pitch.")

        st.markdown("### ⚾ Live Game Count")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Balls", "2")
        with c2:
            st.metric("Strikes", "1")
        with c3:
            st.metric("Outs", "0")
        with c4:
            st.metric("Pitch", "47")

    elif active_panel == "emergency":
        st.markdown("""
        <div class="panel">
            <div class="panel-title">Emergency Workflow</div>
            <div class="panel-big">Critical Actions</div>
            <div class="panel-sub">Fast emergency response tools for assignor notification and incident handling.</div>
            <div class="status-pill alert">Emergency tools armed</div>
        </div>
        """, unsafe_allow_html=True)

        e1, e2 = st.columns(2)
        with e1:
            if st.button("🚨 Alert Assignor", key="alert_assignor", use_container_width=True):
                st.error("Emergency alert workflow triggered for assignor and safety contact.")
        with e2:
            if st.button("📝 Incident Report", key="incident_report", use_container_width=True):
                st.success("Incident report workflow opened.")

        if st.button("📞 Contact Crew Chief", key="emergency_crew", use_container_width=True):
            st.success("Crew communication lane opened.")

    else:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">Rules + Crew Support</div>
            <div class="panel-big">Fast Field Decision Support</div>
            <div class="panel-sub">Rule context, crew operations, and organizational readiness in one place.</div>
            <div class="status-pill">Operationally ready</div>
        </div>
        """, unsafe_allow_html=True)

        st.metric("Most Common Call Tonight", "Obstruction / Interference")
        r1, r2 = st.columns(2)
        with r1:
            st.metric("Rulebook Loaded", "NFHS")
        with r2:
            st.metric("Confidence Mode", "High")
        st.info("Game note: kill the play decisively, then verbalize obstruction separately from interference so coaches hear command, not confusion.")

# -----------------------------
# Secondary tools
# -----------------------------
with st.expander("⚾ Secondary Game Day Tools"):
    s1, s2, s3 = st.columns(3)
    with s1:
        if st.button("🔄 Find Replacement Umpire", use_container_width=True, key="replace"):
            st.info("Nearest qualified official pinged. Assignor copied.")
    with s2:
        if st.button("📍 Open Field Navigation", use_container_width=True, key="nav_lower"):
            st.info("Opening exact field pin with preferred parking approach.")
    with s3:
        if st.button("🧾 Generate Incident Report", use_container_width=True, key="incident_lower"):
            st.success("Professional incident report created and ready for review.")

with st.expander("💬 Crew Chat + Certification"):
    st.subheader("Private Crew Chat")
    message = st.text_input("Type message to crew:")
    if st.button("Send Message", use_container_width=True, key="send_msg"):
        st.success("Message posted to crew channel.")

    cc1, cc2 = st.columns(2)
    with cc1:
        st.success("2025 NFHS Annual Test: **92%** — Passed")
        st.write("Last clinic attendance: **March 28**")
    with cc2:
        st.info("Plate mechanics review: current")
        st.write("Association profile: **active and eligible**")

    if st.button("Add Score / Mark Attendance", use_container_width=True, key="attendance"):
        st.toast("Certification record updated.")

st.markdown(
    '<div class="footer-note">UmpCompanion live prototype • accountability + fast field workflow • built for serious baseball operations</div>',
    unsafe_allow_html=True
)