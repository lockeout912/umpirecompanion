import streamlit as st

st.set_page_config(page_title="UmpCompanion", page_icon="🧢", layout="centered")

# Professional dark theme with clean styling
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    .banner {
        background: linear-gradient(90deg, #1e40af, #3b82f6);
        color: white;
        padding: 12px 0;
        text-align: center;
        font-weight: 600;
        overflow: hidden;
        white-space: nowrap;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .marquee {
        display: inline-block;
        padding-left: 100%;
        animation: marquee 25s linear infinite;
    }
    @keyframes marquee {
        from { transform: translateX(0); }
        to { transform: translateX(-100%); }
    }
    .big-button {
        font-size: 18px !important;
        padding: 16px !important;
        border-radius: 10px !important;
        background: #1e40af !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        margin: 8px 0 !important;
        transition: all 0.2s ease;
    }
    .big-button:hover {
        background: #3b82f6 !important;
        transform: translateY(-2px);
    }
    .rule-box {
        background: #1e3a8a;
        color: #e0f2fe;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #60a5fa;
    }
    .status-card {
        background: #1e2937;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# Scrolling Banner (professional updates)
st.markdown("""
<div class="banner">
    <div class="marquee">
        🚨 2026 NFHS Rule Update: New Obstruction Clarification • 
        📅 Annual Clinic This Saturday 9AM • 
        🌤️ Today's Games: Clear Skies, Low Lightning Risk • 
        ✅ 14 Umpires Completed Annual Test This Week • 
        💡 Tip of the Day: Pre-Game Partner Positioning Check
    </div>
</div>
""", unsafe_allow_html=True)

st.title("🧢 UmpCompanion")
st.subheader("Professional Tools for Serious Umpires")
st.caption("Saratoga Springs Area • Serving 96+ Members & Nearby Associations")

st.markdown("---")

# Quick Status Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="status-card"><strong>Today’s Game</strong><br>Varsity HS • 4:00 PM<br>Field 7</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="status-card"><strong>Partner ETA</strong><br>6 min away 🟢</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="status-card"><strong>Weather</strong><br>68°F • Clear<br>No lightning</div>', unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📖 Rule Advisor", "⚾ Game Day", "💬 Chat & Tracker"])

with tab1:
    st.header("Instant Rule Advisor")
    st.write("**Auto-detected for your current game: Varsity HS — NFHS Rules**")
    
    situation = st.text_area("Describe the play (1–2 sentences):", 
                             "Runner on first, ground ball to shortstop. Fielder obstructs the runner.", 
                             height=100)
    
    if st.button("Get Exact Ruling", key="ruling_btn", use_container_width=True):
        st.markdown("""
        <div class="rule-box">
        <strong>NFHS Rule 2-32 — Obstruction (Type A)</strong><br><br>
        Immediate dead ball.<br>
        Award the obstructed runner at least one base beyond the base they would have reached without the obstruction.<br>
        All other runners advance if forced.
        </div>
        """, unsafe_allow_html=True)
        st.success("Ruling delivered in under 3 seconds — confident call on the field.")

with tab2:
    st.header("Game Day Toolkit")
    
    if st.button("📍 Navigate to Exact Field 7", use_container_width=True):
        st.info("Opening maps with precise pin behind concessions.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🚨 Emergency Alert", use_container_width=True):
            st.error("🚨 Immediate notification sent to Assignor & Safety Officer")
    with col_b:
        if st.button("📝 Quick Incident Report", use_container_width=True):
            st.success("Clean PDF generated — ready to email")
    
    if st.button("🔄 Need a Sub — Scan Nearest Available", use_container_width=True):
        st.info("Nearest qualified ump 4.2 miles away notified. Details sent to Assignor.")
    
    st.subheader("Live Game Counter")
    st.write("Balls: **2** Strikes: **1** Outs: **0** Pitch Count: **47**")

with tab3:
    st.header("Private Crew Chat")
    st.write("All communication stays inside the app — no phone spam.")
    
    message = st.text_input("Type message to crew:")
    if st.button("Send", use_container_width=True):
        st.success("Message posted in General channel")
    
    st.subheader("Certification & Training Tracker")
    st.success("2025 NFHS Annual Test: **92%** — Passed ✓")
    st.write("Last Clinic Attendance: March 28 — Recorded")
    if st.button("Add Test Score or Mark Attendance", use_container_width=True):
        st.toast("Updated successfully — Admin dashboard notified")

st.sidebar.title("UmpCompanion Demo")
st.sidebar.success("Professional • Fast • Reliable")
st.sidebar.info("• Context-aware Rule Lookup\n• One-tap Safety & Incident Tools\n• Sub Helper for Assignors\n• Private Chat & Certification Tracking")
st.sidebar.caption("Built for your organization — ready to scale")

st.caption("Live professional demo • Refresh to see scrolling banner update • Impress your assignor tomorrow!")