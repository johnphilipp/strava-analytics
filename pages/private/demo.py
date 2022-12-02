import streamlit as st
import pandas as pd
from utils.process_data import process_data


def demo():
    if st.button("▶️ Start a demo tour"):
        with open("pages/style/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        df = pd.read_json("data/activities_public.json")
        df = process_data(df)
        st.session_state["df"] = df
        st.experimental_rerun()
