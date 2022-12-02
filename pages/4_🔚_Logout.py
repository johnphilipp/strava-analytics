import streamlit as st
from pages.private.get_started import get_started
from pages.private.logout import logout


def main():
    if "df" in st.session_state:
        st.write("# Logout")
        st.write("#### 👋 See you next time")
        logout()
    else:
        get_started()
    with open("pages/style/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
