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
    "coverage_selected_official": None,
    "incident_generated_text": "",
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


def load_official_pool():
    return [
        {"name": "Cody L.", "home_base": "Ballston Spa", "distance_miles": 7.2, "plate_skill": 84, "base_skill": 88, "availability": "Available", "reliability": 92, "cert": "NFHS", "notes": "Strong hustle, newer but coachable."},
        {"name": "Mike D.", "home_base": "Saratoga Springs", "distance_miles": 12.5, "plate_skill": 93, "base_skill": 89, "availability": "Maybe", "reliability": 97, "cert": "NFHS + Varsity", "notes": "Veteran presence. Better for plate-heavy spots."},
        {"name": "Chris M.", "home_base": "Clifton Park", "distance_miles": 9.8, "plate_skill": 79, "base_skill": 91, "availability": "Available", "reliability": 90, "cert": "NFHS", "notes": "Efficient on bases, dependable fill."},
        {"name": "Dan R.", "home_base": "Niskayuna", "distance_miles": 15.4, "plate_skill": 88, "base_skill": 85, "availability": "Available", "reliability": 86, "cert": "NFHS", "notes": "Solid all-around option."},
        {"name": "Joe S.", "home_base": "Halfmoon", "distance_miles": 4.1, "plate_skill": 74, "base_skill": 83, "availability": "Available", "reliability": 80, "cert": "Rec + Travel", "notes": "Fastest arrival window. Better for base coverage."},
        {"name": "Matt P.", "home_base": "Guilderland", "distance_miles": 21.3, "plate_skill": 90, "base_skill": 87, "availability": "Maybe", "reliability": 89, "cert": "NFHS + College", "notes": "Excellent upside, farther travel."},
        {"name": "Rob T.", "home_base": "Queensbury", "distance_miles": 28.6, "plate_skill": 82, "base_skill": 84, "availability": "Unavailable", "reliability": 91, "cert": "NFHS", "notes": "Good official but currently blocked."},
    ]


assignments = load_assignments()
official_pool = load_official_pool()

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
    return sorted(assignments, key=lambda x: x["game_dt"])[0]


def set_selected_game(game_id):
    st.session_state.selected_game_id = game_id
    st.session_state.checked_in = False
    st.session_state.check_in_time = None
    st.session_state.game_started = False
    st.session_state.first_pitch_time = None
    st.session_state.weather_status = "clear"
    st.session_state.active_panel = "rules"
    st.session_state.rule_result_visible = False
    st.session_state.coverage_selected_official = None
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
                "message": "Two games scheduled. Operationally normal if travel and turnaround stay clean."
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


def get_weather_summary():
    if st.session_state.weather_status == "lightning":
        return ("Lightning Alert", "Suspend play / clear field")
    if st.session_state.weather_status == "caution":
        return ("Weather Caution", "Monitor radar")
    return ("Clear / Playable", "No lightning risk")


def get_coverage_status():
    if st.session_state.coverage_selected_official:
        return f"Recommended: {st.session_state.coverage_selected_official}"
    if st.session_state.sub_assignor_notified:
        return "Assignor notified of coverage risk"
    if st.session_state.sub_scan_done:
        return "Replacement scan completed"
    return "No active coverage issue"


def get_next_game_countdown_text():
    _, next_game, _, _, _ = get_dashboard_metrics(assignments)
    delta = next_game["game_dt"] - datetime.now()
    if delta.total_seconds() <= 0:
        return f"Game #{next_game['game_id']} is in the past / underway window"
    hours = int(delta.total_seconds() // 3600)
    minutes = int((delta.total_seconds() % 3600) // 60)
    if hours > 0:
        return f"Next game in {hours}h {minutes}m"
    return f"Next game in {minutes}m"


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


def score_official(game, official):
    if official["availability"] == "Unavailable":
        return None

    role_skill = official["plate_skill"] if game["position"] == "Plate" else official["base_skill"]
    availability_score = 100 if official["availability"] == "Available" else 70
    distance_score = max(0, 100 - int(official["distance_miles"] * 3))
    reliability_score = official["reliability"]

    weighted_score = (
        role_skill * 0.35
        + availability_score * 0.25
        + distance_score * 0.20
        + reliability_score * 0.20
    )

    urgency = "High" if official["distance_miles"] > 20 or official["availability"] == "Maybe" else "Normal"

    return {
        **official,
        "fit_score": round(weighted_score, 1),
        "role_skill_used": role_skill,
        "distance_score": distance_score,
        "availability_score": availability_score,
        "urgency": urgency,
    }


def get_coverage_candidates(game):
    ranked = []
    for official in official_pool:
        scored = score_official(game, official)
        if scored is not None:
            ranked.append(scored)
    return sorted(ranked, key=lambda x: x["fit_score"], reverse=True)


def build_assignor_message(game, candidate):
    return (
        f"Coverage recommendation for Game #{game['game_id']}: "
        f"{game['home']} vs {game['away']} on {format_game_date(game['game_dt'])} at {format_dt(game['game_dt'])}, "
        f"site {game['site']}. Best current replacement option is {candidate['name']} "
        f"({candidate['availability']}, {candidate['distance_miles']} miles away, fit score {candidate['fit_score']}). "
        f"Recommended action: contact immediately for {game['position']} coverage."
    )


def build_incident_report(game, incident_type, severity, inning, notes):
    return (
        f"Incident Report Draft\n\n"
        f"Game #{game['game_id']} — {game['home']} vs {game['away']}\n"
        f"Date: {format_game_date(game['game_dt'])}\n"
        f"Time: {format_dt(game['game_dt'])}\n"
        f"Site: {game['site']}\n"
        f"Position Worked: {game['position']}\n"
        f"Incident Type: {incident_type}\n"
        f"Severity: {severity}\n"
        f"Inning / Timeframe: {inning}\n\n"
        f"Summary:\n{notes if notes else '[No notes entered]'}\n\n"
        f"Recommended follow-up: review with assignor / board leadership and retain for organizational record."
    )


def build_live_feed_items():
    _, next_game, total_fees, plate_count, base_count = get_dashboard_metrics(assignments)
    weather_title, weather_detail = get_weather_summary()
    schedule_note = get_schedule_agent_note(assignments)
    pattern_notes = analyze_schedule_patterns(assignments)
    selected_game = get_selected_game()

    items = [
        f"🌤 Weather: {weather_title} • {weather_detail}",
        "📣 Org Note: SBUO reminder — clean hat, polished shoes, strong plate presence",
        "📖 NFHS Update: obstruction / interference communication remains a point of emphasis",
        f"🧢 Next Assignment: Game #{next_game['game_id']} • {format_game_date(next_game['game_dt'])} • {format_dt(next_game['game_dt'])}",
        f"⏳ Countdown: {get_next_game_countdown_text()}",
        f"💰 Fee Board: {len(assignments)} games loaded • total fees {format_currency(total_fees)}",
        f"📍 Coverage Status: {get_coverage_status()}",
        f"🎯 Schedule Agent: {schedule_note['title']}",
        f"⚾ Role Split: Plate {plate_count} • Base {base_count}",
        f"✅ Last Action: {st.session_state.last_action}",
    ]

    if pattern_notes:
        items.append(f"🚦 Ops Signal: {pattern_notes[0]['title']}")

    if selected_game:
        items.append(f"🗂 Active Game: #{selected_game['game_id']} • {selected_game['home']} vs {selected_game['away']}")

    if st.session_state.checked_in:
        items.append(f"✅ Check-In Live: {get_checkin_text()}")

    if st.session_state.game_started:
        items.append("⏱ Game Clock Active")

    if st.session_state.emergency_triggered:
        items.append("🚨 Emergency workflow has been triggered")

    return items


limits = {"1:45": 105, "2:00": 120, "2:10": 130}

# =========================================================
# STYLES
# =========================================================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 7% 10%, rgba(103,181,255,.08), transparent 18%),
        radial-gradient(circle at 92% 8%, rgba(184,94,47,.07), transparent 16%),
        radial-gradient(circle at 50% 100%, rgba(39,193,116,.04), transparent 20%),
        linear-gradient(180deg, #06101A 0%, #08131F 45%, #091522 100%);
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
    box-shadow: 0 10px 26px rgba(0,0,0,.18);
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
.stButton > button {
    width: 100%;
    border-radius: 12px;
    font-weight: 800;
}
.small-muted {
    color: #B8C7D8;
    font-size: .88rem;
}

/* Command Center Header */
.cc-shell {
    position: relative;
    overflow: hidden;
    background: linear-gradient(115deg, #0A1726 0%, #102338 50%, #16395E 78%, #19334F 100%);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 20px;
    padding: 16px 18px;
    margin-bottom: 10px;
}
.cc-kicker {
    color: #C7D6E8;
    font-size: .68rem;
    text-transform: uppercase;
    letter-spacing: .18em;
    font-weight: 900;
    margin-bottom: 6px;
}
.cc-title {
    color: white;
    font-size: 1.85rem;
    font-weight: 900;
    line-height: 1.05;
}
.cc-sub {
    color: #D9E4F0;
    font-size: .94rem;
    margin-top: 8px;
}
.cc-live-pill {
    display: inline-block;
    margin-top: 10px;
    background: rgba(227,184,97,.15);
    border: 1px solid rgba(255,255,255,.12);
    color: #FFF4D6;
    border-radius: 999px;
    padding: 7px 12px;
    font-weight: 900;
    font-size: .76rem;
}

/* Scrolling ticker */
.ticker-shell {
    margin: 10px 0 14px 0;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.09);
    background: linear-gradient(90deg, rgba(17,36,58,.96), rgba(21,45,74,.98) 45%, rgba(16,37,60,.96));
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
    animation: ticker-scroll 80s linear infinite;
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

/* Snapshot grid */
.command-grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 10px;
    margin-bottom: 14px;
}
.command-tile {
    background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
    border: 1px solid rgba(155,178,205,0.16);
    border-radius: 15px;
    padding: 12px;
    box-shadow: 0 10px 26px rgba(0,0,0,.12);
}
.command-k {
    color: #AFC0D3;
    text-transform: uppercase;
    letter-spacing: .13em;
    font-size: .62rem;
    font-weight: 900;
    margin-bottom: 6px;
}
.command-v {
    color: #FFF;
    font-size: .96rem;
    font-weight: 900;
    line-height: 1.15;
}
.command-v.gold { color: #FFD981; }
.command-v.green { color: #94F0BD; }
.command-v.blue { color: #A5D2FF; }

@media (max-width: 1350px) {
    .command-grid { grid-template-columns: repeat(4, 1fr); }
}
@media (max-width: 700px) {
    .command-grid { grid-template-columns: repeat(2, 1fr); }
    .cc-title { font-size: 1.5rem; }
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
    pattern_notes = analyze_schedule_patterns(assignments)[:5]
    weather_title, weather_detail = get_weather_summary()

    live_items = build_live_feed_items()
    ticker_content = "".join(
        [f'<span class="ticker-item">{item}</span><span class="ticker-sep">•</span>' for item in live_items]
    )

    st.markdown(
        f"""
        <div class="cc-shell">
            <div class="cc-kicker">Umpire Operations Command Center</div>
            <div class="cc-title">🧢 UmpCompanion</div>
            <div class="cc-sub">
                Next up: Game #{next_game['game_id']} • {next_game['home']} vs {next_game['away']} •
                {format_game_date(next_game['game_dt'])} at {format_dt(next_game['game_dt'])}
            </div>
            <div class="cc-live-pill">● LIVE OPS MODE</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="ticker-shell">
            <div class="ticker-label"><span class="ticker-label-dot"></span> Live Feed</div>
            <div class="ticker-window">
                <div class="ticker-track">
                    <div class="ticker-content">{ticker_content}</div>
                    <div class="ticker-content">{ticker_content}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="command-grid">
            <div class="command-tile">
                <div class="command-k">Next Assignment</div>
                <div class="command-v gold">#{next_game['game_id']} • {next_game['position']}</div>
            </div>
            <div class="command-tile">
                <div class="command-k">Today’s Games</div>
                <div class="command-v">{len(today_games)}</div>
            </div>
            <div class="command-tile">
                <div class="command-k">Total Games</div>
                <div class="command-v">{len(assignments)}</div>
            </div>
            <div class="command-tile">
                <div class="command-k">Fee Board</div>
                <div class="command-v green">{format_currency(total_fees)}</div>
            </div>
            <div class="command-tile">
                <div class="command-k">Plate Assignments</div>
                <div class="command-v">{plate_count}</div>
            </div>
            <div class="command-tile">
                <div class="command-k">Base Assignments</div>
                <div class="command-v">{base_count}</div>
            </div>
            <div class="command-tile">
                <div class="command-k">Weather</div>
                <div class="command-v blue">{weather_title}</div>
            </div>
            <div class="command-tile">
                <div class="command-k">Coverage</div>
                <div class="command-v">{get_coverage_status()}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns([1.25, 1])

    with left:
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

        st.markdown(
            f"""
            <div class="card">
                <h4>Primary Assignment Focus</h4>
                <p><strong>Game #{next_game['game_id']}</strong> • {next_game['position']}</p>
                <p>{next_game['home']} vs {next_game['away']}</p>
                <p>{next_game['site']}</p>
                <p>{format_game_date(next_game['game_dt'])} • {format_dt(next_game['game_dt'])} • Fee {format_currency(next_game['fee'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### Quick Actions")
        q1, q2, q3, q4 = st.columns(4)
        with q1:
            if st.button(f"Launch Game #{next_game['game_id']}", key="dash_launch_game", use_container_width=True):
                set_selected_game(next_game["game_id"])
                st.session_state.page = "Game Day"
        with q2:
            if st.button("Open Full Schedule", key="dash_open_schedule", use_container_width=True):
                st.session_state.page = "My Schedule"
        with q3:
            if st.button("Open Reports", key="dash_open_reports", use_container_width=True):
                st.session_state.page = "Reports"
        with q4:
            if st.button("Activate Next Game", key="dash_activate_next", use_container_width=True):
                set_selected_game(next_game["game_id"])
                st.success(f"Game #{next_game['game_id']} is now active.")

        st.markdown("### Upcoming Assignments")
        for g in sorted(assignments, key=lambda x: x["game_dt"])[:6]:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(
                    f"""
                    <div class="card">
                        <p><strong>Game #{g['game_id']}</strong> • {format_game_date(g['game_dt'])} • {format_dt(g['game_dt'])} • {g['position']}</p>
                        <p>{g['home']} vs {g['away']}</p>
                        <p>{g['site']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with c2:
                if st.button("Use", key=f"use_game_{g['game_id']}", use_container_width=True):
                    set_selected_game(g["game_id"])
                    st.session_state.page = "Game Day"

    with right:
        st.markdown(
            f"""
            <div class="card">
                <h4>Weather + Alert Status</h4>
                <p><strong>{weather_title}</strong></p>
                <p>{weather_detail}</p>
                <p>Last action: {st.session_state.last_action}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="card"><h4>Schedule Signals</h4>', unsafe_allow_html=True)
        if pattern_notes:
            for note in pattern_notes:
                st.write(f"**{note['title']}** — {note['message']}")
        else:
            st.write("No schedule pattern issues detected.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="card">
                <h4>Operations Snapshot</h4>
                <p><strong>Coverage:</strong> {get_coverage_status()}</p>
                <p><strong>Check-In State:</strong> {get_checkin_text()}</p>
                <p><strong>NFHS Pulse:</strong> Obstruction / interference communication emphasis</p>
                <p><strong>Org Pulse:</strong> Professional appearance and strong pregame presence</p>
                <p><strong>Countdown:</strong> {get_next_game_countdown_text()}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

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
# COVERAGE ENGINE
# =========================================================
def render_coverage_engine(game):
    candidates = get_coverage_candidates(game)
    top_candidate = candidates[0] if candidates else None

    if not top_candidate:
        st.error("No available coverage candidates found in the current pool.")
        return

    st.markdown(
        f"""
        <div class="card agent-warning">
            <h4>Coverage Agent</h4>
            <p><strong>Top replacement: {top_candidate['name']}</strong></p>
            <p>{top_candidate['availability']} • {top_candidate['distance_miles']} miles • fit score {top_candidate['fit_score']}</p>
            <p>{top_candidate['notes']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    candidate_df = pd.DataFrame([
        {
            "Official": c["name"],
            "Availability": c["availability"],
            "Miles": c["distance_miles"],
            "Fit Score": c["fit_score"],
            "Role Skill": c["role_skill_used"],
            "Reliability": c["reliability"],
            "Cert": c["cert"],
            "Urgency": c["urgency"],
        }
        for c in candidates
    ])
    st.dataframe(candidate_df, use_container_width=True, hide_index=True)

    option_map = {
        f"{c['name']} • fit {c['fit_score']} • {c['availability']} • {c['distance_miles']} mi": c["name"]
        for c in candidates
    }
    selected_label = st.selectbox("Select replacement option", list(option_map.keys()), key="coverage_choice")
    selected_name = option_map[selected_label]
    selected_candidate = next(c for c in candidates if c["name"] == selected_name)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Mark as Recommended", key="recommend_coverage", use_container_width=True):
            st.session_state.coverage_selected_official = selected_candidate["name"]
            st.session_state.last_action = f"Coverage recommendation set to {selected_candidate['name']}"
            st.success(f"{selected_candidate['name']} marked as recommended replacement.")
    with c2:
        if st.button("Draft Assignor Message", key="draft_assignor_message", use_container_width=True):
            st.session_state.coverage_selected_official = selected_candidate["name"]
            st.session_state.sub_assignor_notified = True
            st.session_state.last_action = "Assignor coverage draft generated"
            st.info("Assignor draft generated below.")
    with c3:
        if st.button("Scan Again", key="scan_again_coverage", use_container_width=True):
            st.session_state.sub_scan_done = True
            st.session_state.last_action = "Coverage scan refreshed"
            st.success("Coverage scan refreshed.")

    if st.session_state.coverage_selected_official == selected_candidate["name"]:
        st.markdown("### Assignor Draft")
        st.code(build_assignor_message(game, selected_candidate), language="text")

# =========================================================
# INCIDENT ENGINE
# =========================================================
def render_incident_engine(game):
    st.markdown(
        """
        <div class="card agent-warning">
            <h4>Incident Agent</h4>
            <p>Convert rough notes into a cleaner assignor-ready report.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        incident_type = st.selectbox(
            "Incident Type",
            ["Coach Conduct", "Fan Conduct", "Ejection", "Field Safety", "Payment Issue", "Other"],
            key="incident_type_gd"
        )
    with c2:
        severity = st.selectbox(
            "Severity",
            ["Low", "Moderate", "High"],
            key="incident_severity_gd"
        )
    with c3:
        inning = st.text_input(
            "Inning / Timeframe",
            placeholder="Top 4th, pregame, postgame...",
            key="incident_inning_gd"
        )

    notes = st.text_area(
        "Incident Notes",
        height=170,
        placeholder="Describe what happened, who was involved, and what action was taken...",
        key="incident_notes_gd"
    )

    if st.button("Generate Incident Draft", key="generate_incident_draft_gd", use_container_width=True):
        st.session_state.incident_generated_text = build_incident_report(game, incident_type, severity, inning, notes)
        st.session_state.last_action = "Incident draft generated"

    if st.session_state.incident_generated_text:
        st.markdown("### Incident Draft")
        st.code(st.session_state.incident_generated_text, language="text")

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
    plate_status_text, _ = get_plate_status(plate_meeting_countdown, st.session_state.checked_in)
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

    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    with r2c1:
        if st.button("🚨 Emergency", key="gd_emergency", use_container_width=True):
            st.session_state.active_panel = "emergency"
    with r2c2:
        if st.button("🔄 Find Sub", key="gd_sub", use_container_width=True):
            st.session_state.active_panel = "sub"
    with r2c3:
        if st.button("📍 Navigate", key="gd_nav", use_container_width=True):
            st.session_state.active_panel = "nav"
    with r2c4:
        if st.button("📝 Incident", key="gd_incident", use_container_width=True):
            st.session_state.active_panel = "incident"

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
        else:
            mc1, mc2 = st.columns(2)
            with mc1:
                st.metric("Elapsed", "00:00")
            with mc2:
                st.metric("Remaining", f"{limits[st.session_state['game_limit']]}:00")

    elif panel == "weather":
        st.markdown("### Weather Control")
        wc1, wc2, wc3 = st.columns(3)
        with wc1:
            if st.button("Clear", key="weather_clear_btn", use_container_width=True):
                st.session_state.weather_status = "clear"
                st.session_state.last_action = "Weather set to Clear"
        with wc2:
            if st.button("Caution", key="weather_caution_btn", use_container_width=True):
                st.session_state.weather_status = "caution"
                st.session_state.last_action = "Weather set to Caution"
        with wc3:
            if st.button("Lightning", key="weather_lightning_btn", use_container_width=True):
                st.session_state.weather_status = "lightning"
                st.session_state.last_action = "Weather set to Lightning"

        wt, wd = get_weather_summary()
        st.info(f"{wt}: {wd}")

    elif panel == "emergency":
        st.markdown("### Emergency Workflow")
        e1, e2 = st.columns(2)
        with e1:
            if st.button("🚨 Alert Assignor", key="alert_assignor_btn", use_container_width=True):
                st.session_state.emergency_triggered = True
                st.session_state.last_action = "Emergency alert sent to assignor"
                st.error("Assignor emergency alert triggered.")
        with e2:
            if st.button("📞 Contact Crew Chief", key="contact_crew_chief_btn", use_container_width=True):
                st.session_state.crew_chief_contacted = True
                st.session_state.last_action = "Crew chief contact initiated"
                st.success("Crew chief contact lane opened.")

    elif panel == "sub":
        st.markdown("### Substitute Coverage")
        render_coverage_engine(game)

    elif panel == "nav":
        st.markdown("### Navigation + Arrival")
        st.write(f"Navigate to: **{game['site']}**")
        n1, n2 = st.columns(2)
        with n1:
            if st.button("📍 Open Field Navigation", key="open_nav_btn", use_container_width=True):
                st.session_state.nav_opened = True
                st.session_state.last_action = "Field navigation opened"
                st.success("Preferred parking and route workflow opened.")
        with n2:
            if st.button("🧭 View Arrival Notes", key="arrival_notes_btn", use_container_width=True):
                st.session_state.nav_notes_opened = True
                st.session_state.last_action = "Arrival notes opened"
                st.info("Arrival note: park behind first-base side concessions and walk to plate area.")

    elif panel == "incident":
        st.markdown("### Incident Workflow")
        render_incident_engine(game)

# =========================================================
# REPORTS
# =========================================================
def render_reports():
    st.subheader("Reports + Logs")

    game = get_selected_game()
    if game:
        st.markdown(
            f"""
            <div class="card">
                <h4>Active Context</h4>
                <p>Game #{game['game_id']} • {game['home']} vs {game['away']}</p>
                <p>{game['site']} • {format_game_date(game['game_dt'])} • {format_dt(game['game_dt'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    if game:
        render_incident_engine(game)
    else:
        st.info("No game is active right now. Select a game first.")

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