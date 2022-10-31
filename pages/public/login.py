import streamlit as st
from bokeh.models.widgets import Div
from auth.auth import get_authorization_url


def login():
    with open("style/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    link = """<a href="{}" class="button">Login and Authenticate</a>""".format(
        get_authorization_url())
    st.markdown(link, unsafe_allow_html=True)