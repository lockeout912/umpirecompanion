import streamlit as st
from datetime import datetime

st.set_page_config(page_title="UmpCompanion", page_icon="🧢", layout="centered")

# Custom styling to look more like a mobile app
st.markdown("""
<style>
    .big-button {
        font-size: 18px !important;
        padding: 15px !important;
        margin: 8px 0 !important;
    }
    .rule-box {
        background-color: #1e3a8a;
        color: white;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧢 UmpCompanion")
st.subheader("Your Umpire Pocket Best Friend")
st.caption("Demo for Assignors • Built for Saratoga Springs Area Umpires")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📖 Rule Advisor", "⚾ Game Day", "💬 Chat & Tracker"])

with tab1:
    st.header("Welcome Back!")
    st.success("Today's Game: Varsity HS • 4:00 PM at Big Park Complex - Field 7")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Partner ETA", "8 min away", "🟢 On time")
    with col2:
        st.metric("Weather", "72°F • Clear", "No lightning risk")
    
    st.button("✅ I'm On Site", type="primary", use_container_width=True)

with tab2:
    st.header("Instant AI Rule Advisor")
    st.write("**Context-aware for your current game (Varsity HS - NFHS rules)**")
    
    situation = st.text_area("Describe the play (1-2 sentences):", 
                             "Runner on first, ground ball to shortstop. F6 obstructs the runner while fielding.", 
                             height=100)
    
    if st.button("🔍 Get Exact Ruling", type="primary", use_container_width=True):
        st.markdown("""
        <div class="rule-box">
        <strong>NFHS Rule 2-32 (Obstruction - Type A)</strong><br><br>
        Dead ball immediately.<br>
        Award the obstructed runner at least one base beyond the base they would have reached without the obstruction.<br>
        All other runners advance if forced.
        </div>
        """, unsafe_allow_html=True)
        st.info("✅ Accurate for Varsity HS. Little League version would differ on award.")

with tab3:
    st.header("Game Day Toolkit")
    st.write("**Game: Varsity HS • Field 7 • 4:00 PM**")
    
    st.button("📍 Navigate to Exact Field 7", type="secondary", use_container_width=True)
    st.button("⏱ Partner ETA Tracker (Live)", type="secondary", use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🚨 Emergency Alert", type="primary"):
            st.error("🚨 Alert sent to Assignor + Safety Officer")
    with col2:
        if st.button("📝 Incident Report", type="secondary"):
            st.success("Report generated & ready to email")
    with col3:
        if st.button("🔄 Need Sub", type="secondary"):
            st.info("Nearest available umps notified (ranked by GPS)")
    
    st.subheader("Live Counter")
    st.write("Balls: 2   Strikes: 1   Outs: 0   Pitch Count: 47")

with tab4:
    st.header("Private Crew Chat")
    st.write("Messages stay in the app — no text/email spam.")
    
    st.text_input("Type message to crew:", "Anyone worked this field before? Parking tips?")
    if st.button("Send to Crew"):
        st.success("Message posted in 'General' channel")
    
    st.subheader("Certification Tracker")
    st.write("2025 NFHS Annual Test: **92%** (Passed ✓)")
    st.write("Last Clinic Attendance: Marked ✓")
    st.button("Add New Test Score / Attendance")

st.sidebar.success("Demo Version • Ready to show your assignor!")
st.sidebar.info("Features shown: Rule lookup, Game Day tools, Chat, Test tracking")
st.caption("This is a live Streamlit demo. We can make it a real mobile app next.")