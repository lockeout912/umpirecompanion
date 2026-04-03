import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# =========================
# SAMPLE DATA (REPLACE LATER)
# =========================
assignments = [
    {
        "game_id": 852,
        "game_dt": datetime.now() + timedelta(hours=3),
        "position": "Plate",
        "home": "Halfmoon",
        "away": "Bethlehem",
        "site": "Halfmoon Field 2",
        "fee": 75,
        "status": "Accepted"
    },
    {
        "game_id": 853,
        "game_dt": datetime.now() + timedelta(days=1),
        "position": "Base",
        "home": "Saratoga",
        "away": "Shen",
        "site": "East Side Rec",
        "fee": 65,
        "status": "Accepted"
    }
]

# =========================
# SESSION STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "selected_game_id" not in st.session_state:
    st.session_state.selected_game_id = None

if "last_action" not in st.session_state:
    st.session_state.last_action = "App Initialized"

if "weather_status" not in st.session_state:
    st.session_state.weather_status = "clear"

if "checked_in" not in st.session_state:
    st.session_state.checked_in = False

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "emergency_triggered" not in st.session_state:
    st.session_state.emergency_triggered = False


# =========================
# HELPERS
# =========================
def get_selected_game():
    for g in assignments:
        if g["game_id"] == st.session_state.selected_game_id:
            return g
    return assignments[0]


def set_selected_game(game_id):
    st.session_state.selected_game_id = game_id


def format_dt(dt):
    return dt.strftime("%I:%M %p")


def format_date(dt):
    return dt.strftime("%b %d")


def format_currency(x):
    return f"${x:.2f}"


def get_dashboard_metrics():
    next_game = sorted(assignments, key=lambda x: x["game_dt"])[0]
    total = sum(a["fee"] for a in assignments)
    plate = sum(1 for a in assignments if a["position"] == "Plate")
    base = sum(1 for a in assignments if a["position"] == "Base")
    return next_game, total, plate, base


def get_weather_summary():
    if st.session_state.weather_status == "lightning":
        return ("Lightning Alert", "Suspend play immediately")
    if st.session_state.weather_status == "caution":
        return ("Weather Watch", "Monitor radar closely")
    return ("Clear", "No issues detected")


def get_next_game_countdown_text():
    g = get_selected_game()
    diff = g["game_dt"] - datetime.now()
    mins = int(diff.total_seconds() / 60)
    return f"{mins} mins"


# =========================
# FIXED LIVE FEED FUNCTION
# =========================
def build_live_feed_items():
    next_game, total, plate, base = get_dashboard_metrics()
    weather_title, weather_detail = get_weather_summary()
    selected_game = get_selected_game()

    return [
        f"🌤 Weather: {weather_title} • {weather_detail}",
        f"🧢 Next: Game #{next_game['game_id']} • {format_dt(next_game['game_dt'])}",
        f"💰 Fees: {format_currency(total)}",
        f"⚾ Roles: Plate {plate} • Base {base}",
        f"⏳ Countdown: {get_next_game_countdown_text()}",
        f"📍 Active Game: #{selected_game['game_id']}",
        f"✅ Last Action: {st.session_state.last_action}",
    ]


# =========================
# RULES ENGINE
# =========================
rules_data = {
    "obstruction": "Obstruction: A fielder without the ball impedes a runner.",
    "interference": "Interference: Offensive player disrupts defense.",
    "infield fly": "Infield Fly: Less than 2 outs, force play, ball can be caught."
}


def search_rules(query):
    results = []
    for k, v in rules_data.items():
        if query.lower() in k or query.lower() in v:
            results.append(v)
    return results


# =========================
# DASHBOARD
# =========================
def render_dashboard():
    next_game, total, plate, base = get_dashboard_metrics()
    feed = build_live_feed_items()

    st.title("🧢 UmpCompanion Command Center")

    # ticker
    st.markdown("### 🔴 Live Feed")
    st.write(" • ".join(feed))

    # tiles
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Next Game", f"#{next_game['game_id']}")
    c2.metric("Total Fees", format_currency(total))
    c3.metric("Plate", plate)
    c4.metric("Base", base)

    st.divider()

    st.subheader("Quick Actions")

    col1, col2 = st.columns(2)

    if col1.button(f"Launch Game #{next_game['game_id']} • {next_game['position']}"):
        set_selected_game(next_game["game_id"])
        st.session_state.page = "Game Day"

    if col2.button("Open Rules"):
        st.session_state.page = "Rules"


# =========================
# GAME DAY
# =========================
def render_game_day():
    g = get_selected_game()

    st.title(f"Game #{g['game_id']} • {g['position']}")

    st.write(f"{g['home']} vs {g['away']}")
    st.write(f"{g['site']}")
    st.write(f"{format_dt(g['game_dt'])}")

    st.divider()

    c1, c2, c3 = st.columns(3)

    if c1.button("Check In"):
        st.session_state.checked_in = True

    if c2.button("Start Game"):
        st.session_state.game_started = True

    if c3.button("Emergency"):
        st.session_state.emergency_triggered = True

    st.divider()

    st.subheader("Weather Radar")
    st.markdown(
        "[Open Live Radar](https://wnyt.com/weather/radar/)",
        unsafe_allow_html=True
    )

    if st.button("Back to Dashboard"):
        st.session_state.page = "Dashboard"


# =========================
# RULES PAGE
# =========================
def render_rules():
    st.title("📖 Rules Engine")

    query = st.text_input("Search rules")

    if query:
        results = search_rules(query)
        for r in results:
            st.success(r)

    if st.button("Back"):
        st.session_state.page = "Dashboard"


# =========================
# ROUTER
# =========================
if st.session_state.page == "Dashboard":
    render_dashboard()

elif st.session_state.page == "Game Day":
    render_game_day()

elif st.session_state.page == "Rules":
    render_rules()