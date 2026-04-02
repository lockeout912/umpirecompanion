import streamlit as st
from datetime import datetime, timedelta, date
import pandas as pd

st.set_page_config(
    page_title="UmpCompanion",
    page_icon="🧢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SESSION STATE
# =========================================================
defaults = {
    "page": "Dashboard",
    "selected_game_id": None,
    "checked_in": False,
    "check_in_time": None,
    "game_started": False,
    "first_pitch_time": None,
    "weather_status": "clear",
    "rule_result_visible": False,
    "rule_result_title": "NFHS Rule 2-32 — Obstruction",
    "rule_result_text": (
        "Immediate dead ball on Type A obstruction when a play is being made on the obstructed runner. "
        "Award the obstructed runner at least one base beyond the base they would have reached without obstruction. "
        "Place all other runners accordingly."
    ),
    "active_panel": "rules",
    "game_limit": "2:00",
    "sub_scan_done": False,
    "sub_assignor_notified": False,
    "nav_opened": False,
    "nav_notes_opened": False,
    "emergency_triggered": False,
    "incident_started": False,
    "crew_chief_contacted": False,
    "last_action": "System ready",
    "schedule_window": "All",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# DATA
# =========================================================
def load_assignments():
    raw = [
        {"game_id": 852, "date": "2026-04-10", "time": "18:00", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Halfmoon Town Park, Field 3 10U", "home": "Halfmoon 10U Wrenn", "away": "Bethlehem 10U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-25"},
        {"game_id": 861, "date": "2026-04-10", "time": "20:00", "position": "Plate", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Halfmoon Town Park, Field 2 12U", "home": "Halfmoon 12U Brewer", "away": "VTB 12U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-25"},
        {"game_id": 732, "date": "2026-04-12", "time": "10:00", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Collins Park, Collins Park LL Majors Field", "home": "SG Mohawks 12U C Flickinger", "away": "Schenectady 12U Blue", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-19"},
        {"game_id": 737, "date": "2026-04-12", "time": "12:30", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Collins Park, Collins Park LL Majors Field", "home": "SG Mohawks 11U White Rakus", "away": "Twin Town White 11U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-19"},
        {"game_id": 741, "date": "2026-04-17", "time": "18:00", "position": "Plate", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Collins Park, Collins Park LL AAA", "home": "SG Mohawks 9U Kilmartin", "away": "N Colonie Blue 9U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-23"},
        {"game_id": 944, "date": "2026-04-19", "time": "10:00", "position": "Base", "sport_level": "SBUO Summer Baseball, 8U Travel 1-Man Coach Pitch POF", "site": "Clifton Commons, Field 7 Lower Quad", "home": "CP White 8U Hurley", "away": "Rotterdam 7U", "fee": 100.00, "status": "Accepted", "accepted_on": "2026-04-01"},
        {"game_id": 848, "date": "2026-04-19", "time": "12:30", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Halfmoon Town Park, Field 2 12U", "home": "Halfmoon 11U Williams", "away": "Saratoga-Milton 11U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-26"},
        {"game_id": 849, "date": "2026-04-19", "time": "15:00", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Halfmoon Town Park, Field 2 12U", "home": "Halfmoon 11U Williams", "away": "Saratoga-Milton 11U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-26"},
        {"game_id": 714, "date": "2026-04-24", "time": "18:00", "position": "Plate", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Halfmoon Town Park, Field 2 12U", "home": "Halfmoon Gray 11U", "away": "N Colonie White 11U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-23"},
        {"game_id": 728, "date": "2026-04-26", "time": "10:00", "position": "Plate", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Collins Park, Collins Park LL Majors Field", "home": "SG Mohawks 12U Pedone", "away": "Saratoga-Wilton White 12U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-23"},
        {"game_id": 729, "date": "2026-04-26", "time": "12:30", "position": "Plate", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Collins Park, Collins Park LL Majors Field", "home": "SG Mohawks 12U Pedone", "away": "Guilderland White 12U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-23"},
        {"game_id": 769, "date": "2026-04-26", "time": "15:00", "position": "Plate", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Indian Meadows, Indian Meadows Minors Field 3", "home": "BH 8U Andersen", "away": "N Colonie Blue 8U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-24"},
        {"game_id": 733, "date": "2026-05-01", "time": "18:00", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Collins Park, Collins Park LL Majors Field", "home": "SG Mohawks 12U C Flickinger", "away": "Rotterdam 12U White", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-24"},
        {"game_id": 913, "date": "2026-05-03", "time": "10:00", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Clifton Commons, Field 14 Upper Quad Rear of Concession Stand", "home": "CP Green 12 Moore", "away": "Bethlehem 12u", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-30"},
        {"game_id": 850, "date": "2026-05-08", "time": "18:00", "position": "Plate", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Halfmoon Town Park, Halfmoon Field 2 12U", "home": "Halfmoon 11U Williams", "away": "Guilderland White 11U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-27"},
        {"game_id": 920, "date": "2026-05-08", "time": "20:15", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 7 Inn POF", "site": "Halfmoon Town Park, Halfmoon Field 2 12U", "home": "Halfmoon 12U Brewer", "away": "TC Bombers 12U", "fee": 85.00, "status": "Accepted", "accepted_on": "2026-03-27"},
        {"game_id": 856, "date": "2026-05-10", "time": "10:00", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Halfmoon Town Park, Halfmoon Field 3 10U", "home": "Halfmoon 10U Wrenn", "away": "Colonie 10U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-26"},
        {"game_id": 857, "date": "2026-05-10", "time": "12:30", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Halfmoon Town Park, Halfmoon Field 3 10U", "home": "Halfmoon 10U Wrenn", "away": "Colonie 10U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-26"},
        {"game_id": 876, "date": "2026-05-10", "time": "15:00", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Clifton Commons, Field 10 Lower Quad", "home": "CP Black 10U Facteau", "away": "Colonie 10U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-28"},
        {"game_id": 690, "date": "2026-05-15", "time": "18:00", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Doubleday Fields, Doubleday 2 Lighted", "home": "Ballston Spa 10U Viscusi", "away": "Queensbury Gold 10U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-27"},
        {"game_id": 691, "date": "2026-05-15", "time": "20:00", "position": "Base", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Doubleday Fields, Doubleday 2 Lighted", "home": "Ballston Spa 12U Lemery", "away": "Niskayuna Red 12U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-27"},
        {"game_id": 579, "date": "2026-05-17", "time": "15:00", "position": "Plate", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Michigan Ave Park, Baseball Diamond", "home": "Schenectady Blue Jays White 10U", "away": "N Colonie Blue 10U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-29"},
        {"game_id": 580, "date": "2026-05-17", "time": "17:30", "position": "Plate", "sport_level": "SBUO Summer Baseball, 12U 6 Inn POF", "site": "Michigan Ave Park, Baseball Diamond", "home": "Schenectady Blue Jays Blue 10U", "away": "Saratoga-Wilton White 10U", "fee": 75.00, "status": "Accepted", "accepted_on": "2026-03-29"},
    ]

    for row in raw:
        row["game_dt"] = datetime.strptime(f"{row['date']} {row['time']}", "%Y-%m-%d %H:%M")
    return raw

assignments = load_assignments()

# =========================================================
# HELPERS
# =========================================================
def format_dt(dt):
    return dt.strftime("%I:%M %p").lstrip("0") if dt else "—"

def format_game_date(dt):
    return dt.strftime("%a, %b %d")

def format_currency(val):
    return f"${val:,.2f}"

def format_td(td):
    total_seconds = max(0, int(td.total_seconds()))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"

def get_selected_game():
    if not assignments:
        return None

    if st.session_state.selected_game_id is not None:
        for game in assignments:
            if game["game_id"] == st.session_state.selected_game_id:
                return game

    upcoming = sorted(assignments, key=lambda x: x["game_dt"])
    return upcoming[0]

def set_selected_game(game_id):
    st.session_state.selected_game_id = game_id
    st.session_state.checked_in = False
    st.session_state.check_in_time = None
    st.session_state.game_started = False
    st.session_state.first_pitch_time = None
    st.session_state.weather_status = "clear"
    st.session_state.active_panel = "rules"
    st.session_state.rule_result_visible = False
    st.session_state.last_action = f"Selected Game #{game_id}"

def get_plate_meeting_time(game_dt):
    return game_dt - timedelta(minutes=5)

def get_partner_name(position):
    return "Mike D." if position == "Plate" else "Chris M."

def get_partner_eta_minutes():
    return 6

def get_ruleset(sport_level):
    return "Modified Youth Rules" if "8U" in sport_level else "NFHS / Summer Ball"

def get_schedule_df(data):
    rows = []
    for g in data:
        rows.append({
            "Game ID": g["game_id"],
            "Date": format_game_date(g["game_dt"]),
            "Time": format_dt(g["game_dt"]),
            "Position": g["position"],
            "Level": g["sport_level"],
            "Site": g["site"],
            "Home": g["home"],
            "Away": g["away"],
            "Fee": format_currency(g["fee"]),
            "Status": g["status"],
        })
    return pd.DataFrame(rows)

def get_dashboard_metrics(data):
    today = date.today()
    today_games = [g for g in data if g["game_dt"].date() == today]
    upcoming = sorted([g for g in data if g["game_dt"] >= datetime.now()], key=lambda x: x["game_dt"])
    next_game = upcoming[0] if upcoming else sorted(data, key=lambda x: x["game_dt"])[0]
    total_fees = sum(g["fee"] for g in data)
    plate_count = sum(1 for g in data if g["position"] == "Plate")
    base_count = sum(1 for g in data if g["position"] == "Base")
    return today_games, next_game, total_fees, plate_count, base_count

def analyze_schedule_patterns(data):
    issues = []
    games_by_date = {}

    for game in sorted(data, key=lambda x: x["game_dt"]):
        games_by_date.setdefault(game["date"], []).append(game)

    for game_date, games in games_by_date.items():
        games = sorted(games, key=lambda x: x["game_dt"])

        if len(games) == 2:
            issues.append({
                "level": "good",
                "title": f"Doubleheader on {game_date}",
                "message": f"Two games scheduled. Operationally normal if travel and turnaround stay clean."
            })
        elif len(games) >= 3:
            issues.append({
                "level": "warning",
                "title": f"Heavy Workload on {game_date}",
                "message": f"{len(games)} games scheduled that day. That’s a grinder. Stay sharp on pacing and travel."
            })

        for i in range(len(games) - 1):
            current_game = games[i]
            next_game = games[i + 1]
            gap_minutes = int((next_game["game_dt"] - current_game["game_dt"]).total_seconds() / 60)

            if gap_minutes < 150:
                same_site = current_game["site"] == next_game["site"]
                if same_site:
                    issues.append({
                        "level": "good",
                        "title": f"Stacked Site Flow on {game_date}",
                        "message": f"Games #{current_game['game_id']} and #{next_game['game_id']} are same-site with a {gap_minutes}-minute gap."
                    })
                else:
                    issues.append({
                        "level": "warning",
                        "title": f"Tight Turnaround on {game_date}",
                        "message": f"Games #{current_game['game_id']} and #{next_game['game_id']} are only {gap_minutes} minutes apart at different sites."
                    })

    return issues

def get_schedule_agent_note(data):
    now = datetime.now()
    upcoming = sorted([g for g in data if g["game_dt"] >= now], key=lambda x: x["game_dt"])

    if not upcoming:
        return {
            "title": "No Upcoming Assignments",
            "message": "No future games detected in the loaded schedule.",
            "level": "warning"
        }

    next_game = upcoming[0]
    same_day = [g for g in data if g["date"] == next_game["date"]]

    if len(same_day) >= 3:
        return {
            "title": "Heavy Day Detected",
            "message": f"You have {len(same_day)} games on {next_game['date']}. Travel pacing and recovery windows matter.",
            "level": "warning"
        }

    if len(same_day) == 2:
        return {
            "title": "Doubleheader Ahead",
            "message": f"You have a two-game stack on {next_game['date']}. Good if same-site. Annoying if not. Worth planning now.",
            "level": "good"
        }

    if next_game["game_dt"] - now <= timedelta(hours=24):
        return {
            "title": "Next Assignment Approaching",
            "message": f"Your next game is #{next_game['game_id']} at {format_dt(next_game['game_dt'])} on {format_game_date(next_game['game_dt'])}.",
            "level": "good"
        }

    return {
        "title": "Schedule Looks Healthy",
        "message": f"{len(upcoming)} upcoming games loaded. No immediate overload flags from the current dataset.",
        "level": "good"
    }

def get_plate_status(td, checked_in):
    secs = td.total_seconds()
    if secs > 900 and checked_in:
        return ("On Track", "good")
    if secs > 900 and not checked_in:
        return ("Check In Pending", "warning")
    if 0 < secs <= 900 and checked_in:
        return ("Due Soon", "warning")
    if 0 < secs <= 900 and not checked_in:
        return ("Late Risk", "warning")
    if secs <= 0 and checked_in:
        return ("Conference Due / Start Now", "critical")
    return ("Past Due", "critical")

def get_checkin_text():
    if st.session_state.checked_in and st.session_state.check_in_time:
        return f"Checked in {format_dt(st.session_state.check_in_time)}"
    return "Not checked in"

def get_clock_status(selected_minutes):
    if st.session_state.game_started and st.session_state.first_pitch_time:
        elapsed = datetime.now() - st.session_state.first_pitch_time
        remaining = timedelta(minutes=selected_minutes) - elapsed
        if remaining.total_seconds() <= 0:
            return "Time limit reached"
        if remaining.total_seconds() <= 900:
            return "Final 15 minutes"
        return "Clock running"
    return "Clock not started"

def get_ops_note(game, plate_meeting_countdown, selected_minutes):
    if st.session_state.weather_status == "lightning":
        return {
            "level": "critical",
            "title": "Lightning Alert Active",
            "message": "Suspend play, clear the field, and begin delay protocol immediately.",
            "action": "Suspend play now and notify crew / assignor."
        }

    if plate_meeting_countdown.total_seconds() <= 0 and not st.session_state.checked_in:
        overdue = abs(plate_meeting_countdown)
        return {
            "level": "critical",
            "title": "Plate Conference Overdue",
            "message": f"Game #{game['game_id']} is overdue for pregame by {format_td(overdue)}.",
            "action": "Check in immediately and get to the plate."
        }

    if 0 < plate_meeting_countdown.total_seconds() <= 600 and not st.session_state.checked_in:
        return {
            "level": "warning",
            "title": "Check-In Needed",
            "message": f"Pregame is due in {format_td(plate_meeting_countdown)} and you are not checked in.",
            "action": "Check in now and move to the meeting point."
        }

    if st.session_state.game_started and st.session_state.first_pitch_time:
        elapsed = datetime.now() - st.session_state.first_pitch_time
        remaining = timedelta(minutes=selected_minutes) - elapsed
        if 0 < remaining.total_seconds() <= 900:
            return {
                "level": "warning",
                "title": "Clock Tightening",
                "message": f"Game is inside final 15 minutes. Remaining: {format_td(remaining)}.",
                "action": "Manage tempo and stay sharp on timing."
            }

    if st.session_state.checked_in:
        return {
            "level": "good",
            "title": "On Track",
            "message": f"You are checked in for Game #{game['game_id']} and on pace for first pitch.",
            "action": "Stay ready and review pregame points."
        }

    return {
        "level": "good",
        "title": "Operationally Ready",
        "message": f"Game #{game['game_id']} is loaded and awaiting field actions.",
        "action": "Monitor timing, weather, and arrival."
    }

limits = {"1:45": 105, "2:00": 120, "2:10": 130}

# =========================================================
# STYLES
# =========================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #06101A 0%, #08131F 45%, #091522 100%);
    color: #F8F4EA;
}
.block-container {
    max-width: 1450px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}
.card {
    background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
    border: 1px solid rgba(155,178,205,0.16);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
}
.topbar {
    background: linear-gradient(115deg, #0A1726 0%, #102338 50%, #16395E 78%, #19334F 100%);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 18px;
    padding: 16px 18px;
    margin-bottom: 14px;
}
.kicker {
    color: #C7D6E8;
    font-size: .72rem;
    text-transform: uppercase;
    letter-spacing: .18em;
    font-weight: 800;
}
.hero {
    font-size: 1.8rem;
    font-weight: 900;
    color: white;
    margin-top: 5px;
}
.subhero {
    color: #D9E4F0;
    font-size: .95rem;
    margin-top: 6px;
}
.agent-good { border-left: 4px solid #27C174; }
.agent-warning { border-left: 4px solid #E3B861; }
.agent-critical { border-left: 4px solid #D83535; }
div[data-testid="stMetric"] {
    background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
    border: 1px solid rgba(155,178,205,0.16);
    border-radius: 16px;
    padding: 12px 14px;
}
.stButton > button {
    width: 100%;
    border-radius: 12px;
    font-weight: 800;
}
.small-muted {
    color: #B8C7D8;
    font-size: .88rem;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# NAV
# =========================================================
def render_topbar():
    st.markdown("""
    <div class="topbar">
        <div class="kicker">Game Operations Platform</div>
        <div class="hero">🧢 UmpCompanion</div>
        <div class="subhero">Schedule intelligence • game day command • coverage workflows • incident logging</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Dashboard", key="nav_dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
    with c2:
        if st.button("My Schedule", key="nav_schedule", use_container_width=True):
            st.session_state.page = "My Schedule"
    with c3:
        if st.button("Game Day", key="nav_gameday", use_container_width=True):
            st.session_state.page = "Game Day"
    with c4:
        if st.button("Reports", key="nav_reports", use_container_width=True):
            st.session_state.page = "Reports"

# =========================================================
# DASHBOARD
# =========================================================
def render_dashboard():
    today_games, next_game, total_fees, plate_count, base_count = get_dashboard_metrics(assignments)
    schedule_note = get_schedule_agent_note(assignments)
    pattern_notes = analyze_schedule_patterns(assignments)[:4]

    st.subheader("Command Overview")

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Total Games", len(assignments))
    with m2:
        st.metric("Today's Games", len(today_games))
    with m3:
        st.metric("Total Fees", format_currency(total_fees))
    with m4:
        st.metric("Plate Assignments", plate_count)
    with m5:
        st.metric("Base Assignments", base_count)

    st.markdown(
        f"""
        <div class="card agent-{schedule_note['level']}">
            <h4>Schedule Agent</h4>
            <p><strong>{schedule_note['title']}</strong></p>
            <p>{schedule_note['message']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown(
            f"""
            <div class="card">
                <h4>Next Assignment</h4>
                <p><strong>Game #{next_game['game_id']}</strong> • {next_game['position']} • {format_game_date(next_game['game_dt'])} at {format_dt(next_game['game_dt'])}</p>
                <p>{next_game['home']} vs {next_game['away']}</p>
                <p>{next_game['site']}</p>
                <p>Fee: {format_currency(next_game['fee'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(f"Launch Game Day for #{next_game['game_id']}", key="launch_next_game", use_container_width=True):
            set_selected_game(next_game["game_id"])
            st.session_state.page = "Game Day"

    with right:
        st.markdown('<div class="card"><h4>Schedule Signals</h4>', unsafe_allow_html=True)
        if pattern_notes:
            for note in pattern_notes:
                st.write(f"**{note['title']}** — {note['message']}")
        else:
            st.write("No pattern issues detected.")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# SCHEDULE
# =========================================================
def filter_assignments(data, window_filter, position_filter, site_search):
    now = datetime.now()
    filtered = data[:]

    if window_filter == "Today":
        filtered = [g for g in filtered if g["game_dt"].date() == now.date()]
    elif window_filter == "Next 7 Days":
        end_window = now + timedelta(days=7)
        filtered = [g for g in filtered if now.date() <= g["game_dt"].date() <= end_window.date()]
    elif window_filter == "Upcoming":
        filtered = [g for g in filtered if g["game_dt"] >= now]

    if position_filter != "All":
        filtered = [g for g in filtered if g["position"] == position_filter]

    if site_search.strip():
        filtered = [g for g in filtered if site_search.lower() in g["site"].lower()]

    return sorted(filtered, key=lambda x: x["game_dt"])

def render_schedule_summary(filtered):
    total_fees = sum(g["fee"] for g in filtered)
    plate_count = sum(1 for g in filtered if g["position"] == "Plate")
    base_count = sum(1 for g in filtered if g["position"] == "Base")

    a, b, c, d = st.columns(4)
    with a:
        st.metric("Filtered Games", len(filtered))
    with b:
        st.metric("Filtered Fees", format_currency(total_fees))
    with c:
        st.metric("Plate", plate_count)
    with d:
        st.metric("Base", base_count)

def render_schedule_cards(filtered):
    st.markdown("### Assignment Cards")
    if not filtered:
        st.info("No games match the current filters.")
        return

    for g in filtered:
        with st.container():
            st.markdown(
                f"""
                <div class="card">
                    <h4>Game #{g['game_id']} • {format_game_date(g['game_dt'])} • {format_dt(g['game_dt'])}</h4>
                    <p><strong>{g['home']}</strong> vs <strong>{g['away']}</strong></p>
                    <p>{g['site']}</p>
                    <p>{g['position']} • {g['sport_level']} • Fee {format_currency(g['fee'])} • {g['status']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"Activate #{g['game_id']}", key=f"activate_{g['game_id']}", use_container_width=True):
                    set_selected_game(g["game_id"])
                    st.success(f"Game #{g['game_id']} is now active.")
            with c2:
                if st.button(f"Open Game Day #{g['game_id']}", key=f"open_gameday_{g['game_id']}", use_container_width=True):
                    set_selected_game(g["game_id"])
                    st.session_state.page = "Game Day"

def render_schedule():
    st.subheader("My Schedule")

    f1, f2, f3 = st.columns(3)
    with f1:
        window_filter = st.selectbox("Window", ["All", "Upcoming", "Today", "Next 7 Days"], key="window_filter")
    with f2:
        position_filter = st.selectbox("Position", ["All", "Plate", "Base"], key="position_filter")
    with f3:
        site_search = st.text_input("Site Search", placeholder="Halfmoon, Collins, Clifton...", key="site_search")

    filtered = filter_assignments(assignments, window_filter, position_filter, site_search)

    render_schedule_summary(filtered)
    st.dataframe(get_schedule_df(filtered), use_container_width=True, hide_index=True)

    schedule_note = get_schedule_agent_note(filtered) if filtered else {
        "title": "No Matching Games",
        "message": "Current filters removed everything from view.",
        "level": "warning"
    }

    st.markdown(
        f"""
        <div class="card agent-{schedule_note['level']}">
            <h4>Filtered Schedule Agent</h4>
            <p><strong>{schedule_note['title']}</strong></p>
            <p>{schedule_note['message']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    render_schedule_cards(filtered[:10])

# =========================================================
# GAME DAY
# =========================================================
def render_game_day():
    game = get_selected_game()
    if not game:
        st.warning("No game selected.")
        return

    partner_name = get_partner_name(game["position"])
    partner_eta_minutes = get_partner_eta_minutes()
    partner_eta = f"{partner_eta_minutes} Minutes"
    ruleset = get_ruleset(game["sport_level"])
    weather_temp = "68°F"
    weather_summary = "Clear"

    current_time = datetime.now()
    game_time = game["game_dt"]
    plate_meeting_time = get_plate_meeting_time(game_time)
    plate_meeting_countdown = plate_meeting_time - current_time

    selected_limit = st.session_state["game_limit"]
    selected_minutes = limits[selected_limit]
    plate_status_text, plate_status_level = get_plate_status(
        plate_meeting_countdown,
        st.session_state.checked_in
    )
    ops_note = get_ops_note(game, plate_meeting_countdown, selected_minutes)

    st.subheader("Game Day Mode")

    st.markdown(
        f"""
        <div class="card">
            <h3>Active Assignment • Game #{game['game_id']}</h3>
            <p><strong>{game['home']}</strong> vs <strong>{game['away']}</strong></p>
            <p>{game['site']}</p>
            <p>{format_game_date(game['game_dt'])} • {format_dt(game['game_dt'])} • {game['position']} • {ruleset}</p>
            <p>Fee: {format_currency(game['fee'])} • Status: {game['status']} • Accepted On: {game['accepted_on']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    s1, s2, s3, s4, s5, s6 = st.columns(6)
    with s1:
        st.metric("Partner", partner_name)
    with s2:
        st.metric("Partner ETA", partner_eta)
    with s3:
        st.metric("Check-In", get_checkin_text())
    with s4:
        st.metric("Pregame", format_td(plate_meeting_countdown))
    with s5:
        st.metric("Weather", f"{weather_temp} / {weather_summary}")
    with s6:
        st.metric("Clock", get_clock_status(selected_minutes))

    st.markdown(
        f"""
        <div class="card agent-{ops_note['level']}">
            <h4>Game Day Ops Agent</h4>
            <p><strong>{ops_note['title']}</strong></p>
            <p>{ops_note['message']}</p>
            <p><strong>Recommended action:</strong> {ops_note['action']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    readiness_col1, readiness_col2 = st.columns(2)
    with readiness_col1:
        st.markdown(
            f"""
            <div class="card">
                <h4>Readiness Strip</h4>
                <p>Plate Conference: <strong>{format_dt(plate_meeting_time)}</strong></p>
                <p>Status: <strong>{plate_status_text}</strong></p>
                <p class="small-muted">That’s the clock that matters before the clock that matters.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with readiness_col2:
        st.markdown(
            f"""
            <div class="card">
                <h4>Game Context</h4>
                <p>Ruleset: <strong>{ruleset}</strong></p>
                <p>Position: <strong>{game['position']}</strong></p>
                <p>Site: <strong>{game['site']}</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Control Center")
    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    with r1c1:
        if st.button("✅ Check In", key="gd_checkin", use_container_width=True):
            st.session_state.checked_in = True
            st.session_state.check_in_time = datetime.now()
            st.session_state.last_action = f"Checked in for Game #{game['game_id']} at {format_dt(st.session_state.check_in_time)}"
    with r1c2:
        if st.button("📖 Rules", key="gd_rules", use_container_width=True):
            st.session_state.active_panel = "rules"
    with r1c3:
        if st.button("⏱ Clock", key="gd_clock", use_container_width=True):
            st.session_state.active_panel = "clock"
    with r1c4:
        if st.button("🌩 Weather", key="gd_weather", use_container_width=True):
            st.session_state.active_panel = "weather"

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        if st.button("🚨 Emergency", key="gd_emergency", use_container_width=True):
            st.session_state.active_panel = "emergency"
    with r2c2:
        if st.button("🔄 Find Sub", key="gd_sub", use_container_width=True):
            st.session_state.active_panel = "sub"
    with r2c3:
        if st.button("📍 Navigate", key="gd_nav", use_container_width=True):
            st.session_state.active_panel = "nav"

    panel = st.session_state.active_panel

    if panel == "rules":
        st.markdown("### Rule Lookup")
        st.text_area(
            "Describe the play",
            "Runner on first, ground ball to shortstop. Fielder obstructs the runner.",
            height=120,
            key="rules_textarea"
        )
        if st.button("Get Exact Ruling", key="get_ruling", use_container_width=True):
            st.session_state.rule_result_visible = True
            st.session_state.last_action = "Rule result generated"

        if st.session_state.rule_result_visible:
            st.markdown(
                f"""
                <div class="card">
                    <h4>{st.session_state.rule_result_title}</h4>
                    <p>{st.session_state.rule_result_text}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    elif panel == "clock":
        st.selectbox("Game Time Limit", ["1:45", "2:00", "2:10"], key="game_limit")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("⏱ Start Game", key="start_clock", use_container_width=True):
                st.session_state.game_started = True
                st.session_state.first_pitch_time = datetime.now()
                st.session_state.last_action = f"Game #{game['game_id']} clock started"
        with c2:
            if st.button("↺ Reset Clock", key="reset_clock", use_container_width=True):
                st.session_state.game_started = False
                st.session_state.first_pitch_time = None
                st.session_state.last_action = f"Game #{game['game_id']} clock reset"

        if st.session_state.game_started and st.session_state.first_pitch_time:
            elapsed = datetime.now() - st.session_state.first_pitch_time
            remaining = timedelta(minutes=limits[st.session_state["game_limit"]]) - elapsed

            mc1, mc2 = st.columns(2)
            with mc1:
                st.metric("Elapsed", format_td(elapsed))
            with mc2:
                st.metric("Remaining", format_td(remaining))

    elif panel == "weather":
        st.markdown("### Weather Control")
        wc1, wc2, wc3 = st.columns(3)
        with wc1:
            if st.button("Clear", key="weather_clear_btn", use_container_width=True):
                st.session_state.weather_status = "clear"
        with wc2:
            if st.button("Caution", key="weather_caution_btn", use_container_width=True):
                st.session_state.weather_status = "caution"
        with wc3:
            if st.button("Lightning", key="weather_lightning_btn", use_container_width=True):
                st.session_state.weather_status = "lightning"

        st.info(f"Manual weather mode set to: {st.session_state.weather_status.title()}")

    elif panel == "emergency":
        st.markdown("### Emergency Workflow")
        if st.button("🚨 Alert Assignor", key="alert_assignor_btn", use_container_width=True):
            st.session_state.emergency_triggered = True
            st.error("Assignor emergency alert triggered.")
        if st.button("📝 Open Incident Report", key="open_incident_btn", use_container_width=True):
            st.session_state.incident_started = True
            st.success("Incident workflow opened.")

    elif panel == "sub":
        st.markdown("### Substitute Coverage")
        if st.button("🔄 Scan Nearest Available", key="scan_sub_btn", use_container_width=True):
            st.session_state.sub_scan_done = True
            st.info("Nearest qualified official 4.2 miles away notified. Assignor copied.")
        if st.button("📤 Notify Assignor of Coverage Risk", key="notify_assignor_sub_btn", use_container_width=True):
            st.session_state.sub_assignor_notified = True
            st.warning("Coverage risk notification sent.")

    elif panel == "nav":
        st.markdown("### Navigation + Arrival")
        st.write(f"Navigate to: **{game['site']}**")
        if st.button("📍 Open Field Navigation", key="open_nav_btn", use_container_width=True):
            st.success("Preferred parking and route workflow opened.")
        if st.button("🧭 View Arrival Notes", key="arrival_notes_btn", use_container_width=True):
            st.info("Arrival note: park behind first-base side concessions and walk to plate area.")

# =========================================================
# REPORTS
# =========================================================
def render_reports():
    st.subheader("Reports + Logs")

    st.markdown(
        """
        <div class="card">
            <h4>Incident Agent</h4>
            <p>Future lane: convert rough notes into polished, assignor-ready incident reports.</p>
            <p>Next implementation target: abuse / ejection / field issue templates with timestamps and export.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    incident_type = st.selectbox(
        "Report Type",
        ["Coach Conduct", "Fan Conduct", "Ejection", "Field Safety", "Payment Issue", "Other"],
        key="report_type"
    )
    notes = st.text_area("Notes", height=180, placeholder="Describe exactly what happened...", key="report_notes")

    if st.button("Generate Draft Report", key="generate_report", use_container_width=True):
        st.success(f"{incident_type} draft report generated.")
        st.write("**Draft Summary**")
        st.write(
            f"During the assignment, an incident categorized as '{incident_type}' was observed. "
            f"Initial notes: {notes if notes else '[no notes entered]'}"
        )

# =========================================================
# APP RENDER
# =========================================================
render_topbar()

if st.session_state.page == "Dashboard":
    render_dashboard()
elif st.session_state.page == "My Schedule":
    render_schedule()
elif st.session_state.page == "Game Day":
    render_game_day()
elif st.session_state.page == "Reports":
    render_reports()