import streamlit as st
import pandas as pd
from utils.process_data import process_data


def upload():
    if "upload" not in st.session_state:
        st.session_state["upload"] = False
    print(st.session_state["upload"])

    if st.button("💾 Upload your own dataset"):
        st.session_state["upload"] = True

    if st.session_state["upload"] == True:
        uploaded_file = st.file_uploader(
            "Upload Strava activity data as json", "json", False)

        if uploaded_file is not None:
            df = pd.read_json(uploaded_file)
            df = process_data(df)
            st.session_state["df"] = df
            st.session_state["upload"] = False
            st.experimental_rerun()
