import streamlit as st
from pages.private.get_started import get_started
from pages.private.logout import logout
from utils.switch_page import switch_page


def main():
    if "df" in st.session_state:
        st.write("# Logout")
        st.write("#### 👋 See you next time")
        logout()
        st.write("####")
        if st.button("🏠 Home"):
            switch_page("home")
        if st.button("📍 Heatmap Visualizer"):
            switch_page("heatmap visualizer")
        if st.button("🌌 Poster Maker"):
            switch_page("poster maker")
        if st.button("📅 Calendar Tracker"):
            switch_page("calendar tracker")

    else:
        get_started()
    with open("pages/style/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
