import streamlit as st
import pandas as pd
from utils.process_data import process_data


def upload():
    with open("pages/style/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Strava activity data as json", "json", False)

    if uploaded_file is not None:
        df = pd.read_json(uploaded_file)
        df = process_data(df)
        st.session_state["df"] = df
        st.experimental_rerun()
