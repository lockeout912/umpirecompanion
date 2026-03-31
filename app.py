import streamlit as st
from datetime import datetime

st.set_page_config(page_title="UmpCompanion", page_icon="🧢", layout="centered")

# Super cool dark + neon umpire theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        color: #ffffff;
    }
    .big-button {
        font-size: 20px !important;
        padding: 18px !important;
        border-radius: 12px !important;
        background: linear-gradient(90deg, #1e40af, #3b82f6) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
        transition: all 0.2s ease !important;
    }
    .big-button:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.6) !important;
    }
    .rule-box {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 20px;
        border-radius: 16px;
        border-left: 6px solid #60a5fa;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
    }
    .header-glow {
        text-shadow: 0 0 20px #60a5fa;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧢 UmpCompanion")
st.markdown("<h2 class='header-glow'>Your Umpire Pocket Best Friend</h2>", unsafe_allow_html=True)
st.caption("🚀 Demo for Assignors • Saratoga Springs Umpires • Ready for Game Day")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📖 Rule Advisor", "⚾ Game Day", "💬 Chat & Tracker"])

with tab1:
    st.header("Game Day Ready")
    st.success("**Today's Assignment** — Varsity HS • 4:00 PM • Big Park Complex - Field 7")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Partner ETA", "6 min away", "🟢 On time", delta_color="normal")
    with col2:
        st.metric("Field Status", "Clear", "🌤️ No lightning")
    
    st.button("✅ I'm On Site & Ready", type="primary", use_container_width=True, key="onsite")

with tab2:
    st.header("⚡ Instant AI Rule Advisor")
    st.write("**Auto-detected: Varsity High School — NFHS Rules**")
    
    situation = st.text_area("Quickly describe the play:", 
                             "Runner on 1st, grounder to shortstop — F6 obstructs runner while fielding the ball.", 
                             height=110)
    
    if st.button("🔍 Get Exact Ruling Now", type="primary", use_container_width=True):
        st.markdown("""
        <div class="rule-box">
        <strong>NFHS Rule 2-32 — Obstruction (Type A)</strong><br><br>
        <strong>Call:</strong> Immediate dead ball.<br>
        Award the obstructed runner at least one base beyond the base they would have reached.<br>
        All other runners advance if forced.
        </div>
        """, unsafe_allow_html=True)
        st.balloons()  # Fun visual
        st.info("✅ Fast, accurate, and context-aware. No more paper rulebook.")

with tab3:
    st.header("⚾ Game Day Toolkit")
    st.write("**Live Game: Varsity HS • Field 7**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("📍 Navigate to Exact Field 7", use_container_width=True)
        st.button("⏱ Partner ETA Live Tracker", use_container_width=True)
    with col2:
        if st.button("🚨 Emergency Alert", type="primary", use_container_width=True):
            st.error("🚨 EMERGENCY NOTIFICATION SENT to Assignor & Safety Officer")
        if st.button("📝 Quick Incident Report", use_container_width=True):
            st.success("Professional report generated — ready to email")
    
    if st.button("🔄 Need a Sub — Find Nearest Available", type="secondary", use_container_width=True):
        st.info("Scanning local crew... Nearest ump 4.2 miles away notified.")
    
    st.subheader("Live Counter")
    st.write("Balls: **2**   Strikes: **1**   Outs: **0**   Pitch Count: **47**")

with tab4:
    st.header("💬 Private Crew Chat")
    st.write("Safe space for umpires — messages stay in the app only.")
    
    col1, col2 = st.columns([3,1])
    with col1:
        message = st.text_input("Message to crew:")
    with col2:
        if st.button("Send"):
            st.success("Posted in General Channel")
    
    st.subheader("Certification Tracker")
    st.success("2025 NFHS Annual Test: **92%** — Passed")
    st.write("Last Clinic: Attended March 28")
    if st.button("Add Test Score or Attendance"):
        st.toast("Added successfully!")

# Sidebar for extra wow
st.sidebar.title("🚀 UmpCompanion Demo")
st.sidebar.success("Ready for tomorrow's meeting!")
st.sidebar.info("• Instant Rule Lookup\n• One-tap Incident & Sub\n• Private Chat\n• Test Tracking")
st.sidebar.caption("Made for your 96-member org + nearby associations")

st.caption("Live Streamlit Demo • Click around to test features • Real app coming soon")