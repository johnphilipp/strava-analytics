import streamlit as st
from pages.private.login import login
from pages.private.upload import upload
from pages.private.demo import demo


def get_started():
    st.write("# Get started")
    login()
    upload()
    demo()
