import streamlit as st


def dashboard(df):
    col1, col2, col3 = st.columns(3)
    col1.metric("# Activites", len(df))
    col2.metric("# Runs", len(df[df["type"] == "Run"]))
    col3.metric("# Rides", len(df[df["type"] == "Ride"]))
