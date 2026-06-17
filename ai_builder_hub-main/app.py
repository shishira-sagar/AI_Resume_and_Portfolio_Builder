import streamlit as st
import subprocess
import sys
import os

# Page Configuration
st.set_page_config(
    page_title="AI Resume, Portfolio & Cover Letter Builder",
    layout="wide"
)

# ===== Header Section =====
st.markdown("""
# 🤖 Welcome to the AI Builder Hub!
Craft your professional assets with the power of AI.
""")

st.markdown("##### What would you like to build today?")
st.markdown("---")

# ===== Option Cards =====
col1, col2, col3 = st.columns(3)

def launch_script(script_name, app_name):
    script_path = os.path.join(os.getcwd(), script_name)
    try:
        subprocess.Popen([sys.executable, "-m", "streamlit", "run", script_path])
        st.info(f"🚀 Launching {app_name} in a new tab...")
    except Exception as e:
        st.error(f"❌ Could not launch {app_name}. Error: {e}")

# --- Resume Builder ---
with col1:
    with st.container(border=True):
        st.subheader("📄 Resume Builder")
        st.write("Create a personalized, professional resume powered by AI.")
        if st.button("🚀 Launch Resume Builder", use_container_width=True):
            launch_script("resume.py", "Resume Builder")

# --- Portfolio Builder ---
with col2:
    with st.container(border=True):
        st.subheader("🌐 Portfolio Builder")
        st.write("Build a sleek online portfolio to showcase your skills.")
        if st.button("🚀 Launch Portfolio Builder", use_container_width=True):
            launch_script("portfolio.py", "Portfolio Builder")

# --- Cover Letter Builder ---
with col3:
    with st.container(border=True):
        st.subheader("🧾 Cover Letter Builder")
        st.write("Generate customized cover letters tailored to each job.")
        if st.button("🚀 Launch Cover Letter Builder", use_container_width=True):
            launch_script("coverletter.py", "Cover Letter Builder")

# ===== Footer =====
st.markdown("---")
st.caption("🔧 Built with [Streamlit](https://streamlit.io/) | © 2025 AI Builder Tools")
