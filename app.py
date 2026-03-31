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

limits = {
    "1:45": 105,
    "2:00": 120,
    "2:10": 130
}
selected_limit = st.session_state.get("game_limit", "2:00")
selected_minutes = limits[selected_limit]

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
st.html("""
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
    padding-top: 0.65rem;
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
    border-radius: 22px;
    padding: 16px 18px 15px 18px;
    box-shadow: var(--shadow);
    margin-bottom: 12px;
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
    gap: 14px;
    flex-wrap: wrap;
}
.header-kicker {
    color: #C7D6E8;
    font-size: .68rem;
    text-transform: uppercase;
    letter-spacing: .18em;
    font-weight: 900;
    margin-bottom: 6px;
}
.header-title {
    margin: 0;
    font-size: 1.9rem;
    font-weight: 900;
    line-height: 1.02;
}
.header-live {
    background: linear-gradient(90deg, rgba(227,184,97,.18), rgba(255,255,255,.06));
    border: 1px solid rgba(255,255,255,.12);
    color: #FFF4D6;
    border-radius: 999px;
    padding: 8px 13px;
    font-weight: 900;
    font-size: .80rem;
    box-shadow: var(--glow-gold);
}
.header-sub {
    margin-top: 8px;
    color: #D9E4F0;
    font-size: .96rem;
}

/* Action deck */
.deck-shell {
    margin: 8px 0 14px 0;
}
.deck-title {
    color: #AFC0D3;
    text-transform: uppercase;
    letter-spacing: .16em;
    font-size: .68rem;
    font-weight: 900;
    margin-bottom: 8px;
}
.deck-actions .stButton > button {
    min-height: 62px;
    font-size: 1.02rem;
}
.primary-row .stButton > button {
    background: linear-gradient(180deg, #2A6AB0, #194B7E);
    box-shadow: var(--glow-blue);
}
.alert-row .stButton > button {
    background: linear-gradient(180deg, #2A6AB0, #194B7E);
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
    font-size: .68rem;
    font-weight: 900;
    margin-bottom: 9px;
}
.panel-big {
    color: white;
    font-size: 1.18rem;
    font-weight: 900;
    line-height: 1.15;
}
.panel-sub {
    color: #C9D8E8;
    font-size: .92rem;
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
}

.snapshot-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 10px;
    margin-bottom: 14px;
}
.snap {
    background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 12px 13px;
    box-shadow: var(--shadow-soft);
}
.snap-k {
    color: #AFC0D3;
    text-transform: uppercase;
    letter-spacing: .13em;
    font-size: .64rem;
    font-weight: 900;
    margin-bottom: 5px;
}
.snap-v {
    color: #FFF;
    font-size: .98rem;
    font-weight: 900;
    line-height: 1.15;
}
.snap-v.green { color: #94F0BD; }
.snap-v.blue { color: #A5D2FF; }
.snap-v.gold { color: #FFD981; }

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
    border-radius: 999px;
    padding: 0.90rem 1rem;
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
    font-size: .68rem !important;
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
    margin-top: 20px;
    color: #A9B9CA;
    font-size: .86rem;
    text-align: center;
}

@media (max-width: 1100px) {
    .snapshot-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}
@media (max-width: 700px) {
    .header-title {
        font-size: 1.6rem;
    }
    .snapshot-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .deck-actions .stButton > button {
        min-height: 58px;
        font-size: .96rem;
    }
}
</style>
""")

# -----------------------------
# Header
# -----------------------------
st.html(f"""
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
""")

# -----------------------------
# Rapid Action Deck
# -----------------------------
st.markdown('<div class="deck-shell"><div class="deck-title">Rapid Action Deck</div></div>', unsafe_allow_html=True)

st.markdown('<div class="deck-actions primary-row">', unsafe_allow_html=True)
r1c1, r1c2, r1c3, r1c4 = st.columns(4)
with r1c1:
    if st.button("✅ Check In", use_container_width=True, key="top_checkin"):
        st.session_state.checked_in = True
        st.session_state.check_in_time = datetime.now()
with r1c2:
    if st.button("📍 Navigate", use_container_width=True, key="top_nav"):
        st.info("Opening exact field pin with preferred parking approach.")
with r1c3:
    if st.button("⏱ Start Game", use_container_width=True, key="top_start"):
        st.session_state.game_started = True
        st.session_state.first_pitch_time = datetime.now()
with r1c4:
    if st.button("⚡ Weather Alert", use_container_width=True, key="top_weather"):
        st.warning("Weather controls are active below. Use Clear / Caution / Lightning.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="deck-actions alert-row">', unsafe_allow_html=True)
r2c1, r2c2, r2c3, r2c4 = st.columns(4)
with r2c1:
    if st.button("📖 Rule Lookup", use_container_width=True, key="top_rule"):
        st.toast("Rule lookup is ready below.")
with r2c2:
    if st.button("🚨 Emergency", use_container_width=True, key="top_emergency"):
        st.error("Emergency alert workflow triggered for assignor and safety contact.")
with r2c3:
    if st.button("📝 Incident", use_container_width=True, key="top_incident"):
        st.success("Incident report workflow opened.")
with r2c4:
    if st.button("📞 Crew Chief", use_container_width=True, key="top_crewchief"):
        st.success("Crew communication lane opened.")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Snapshot Grid
# -----------------------------
check_in_text = (
    f"Checked in {format_dt(st.session_state.check_in_time)}"
    if st.session_state.checked_in and st.session_state.check_in_time
    else "Not checked in"
)

st.html(f"""
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
""")

# -----------------------------
# Main operational row
# -----------------------------
left, right = st.columns([1.25, 1])

with left:
    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">Plate Meeting + Arrival</div>
        <div class="panel-big">{assignment} • {format_dt(game_time)}</div>
        <div class="panel-sub">{game_site}</div>
        <div class="panel-sub">Plate Meeting: {format_dt(plate_meeting_time)} • First Pitch: {format_dt(game_time)}</div>
        <div class="status-pill">Meeting in {format_td(plate_meeting_countdown)}</div>
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
        height=140,
        placeholder="Example: R1 stealing, throw from catcher pulls F6 into the baseline..."
    )

    if st.button("Get Exact Ruling", key="ruling_btn", use_container_width=True):
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
    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">Live Weather Alert</div>
        <div class="panel-big">{weather_temp} • {weather_summary}</div>
        <div class="panel-sub">Radar-ready tile for lightning and weather delay workflows.</div>
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

    st.selectbox(
        "Game Time Limit",
        ["1:45", "2:00", "2:10"],
        index=["1:45", "2:00", "2:10"].index(selected_limit),
        key="game_limit"
    )
    selected_limit = st.session_state["game_limit"]
    selected_minutes = limits[selected_limit]

    st.markdown("""
    <div class="panel" style="margin-top:10px;">
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
    '<div class="footer-note">UmpCompanion live prototype • fast field workflow • built for serious baseball operations</div>',
    unsafe_allow_html=True
)