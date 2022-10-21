import streamlit as st
from bokeh.models.widgets import Div
from auth.auth import get_authorization_url


def login():
    link = '[Login and Authorize]({})'.format(get_authorization_url())
    st.markdown(link, unsafe_allow_html=True)
