import streamlit as st
from bokeh.models.widgets import Div
from auth.auth import get_authorization_url


def login():
    if st.button("Login and Authorize"):
        js = "window.location.href = '{}'".format(get_authorization_url())
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)
