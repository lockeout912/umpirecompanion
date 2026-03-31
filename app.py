import streamlit as st

st.set_page_config(page_title="UmpCompanion", layout="centered")

st.title("🧢 UmpCompanion")
st.subheader("Your Umpire Pocket Best Friend")

st.markdown("---")

# Tabs like a phone app
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📖 Rule Advisor", "⚾ Game Day", "💬 Chat"])

with tab1:
    st.header("Welcome!")
    st.write("Quick access to everything you need on game day.")
    if st.button("Start a Game"):
        st.success("Game loaded! (demo)")

with tab2:
    st.header("Instant Rule Advisor")
    situation = st.text_input("Describe the play (1-2 sentences):", 
                              "Runner on first, ground ball to shortstop with obstruction")
    if st.button("Get Ruling"):
        st.success("**NFHS Rule 2-32 (Obstruction)**\nDead ball immediately. Award the obstructed runner at least one base.")
        st.info("This is for your Varsity HS game.")

with tab3:
    st.header("Game Day Toolkit")
    st.write("**Field 7 at Big Park**")
    st.button("📍 Navigate to Exact Field")
    st.button("⏱ Partner ETA: 8 min away")
    st.button("🚨 Emergency Alert")
    st.button("📝 Quick Incident Report")
    st.button("🔄 Need a Sub")

with tab4:
    st.header("Private Crew Chat")
    st.write("Messages stay in the app — no texts or emails.")
    message = st.text_input("Type a message:")
    if st.button("Send"):
        st.write("✅ Message sent to crew (demo)")

st.caption("Demo visual — built with Streamlit | We will add real features later")
