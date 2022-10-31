from re import X
import streamlit as st


def dashboard(df):
    num_activities = len(df)
    num_runs = len(df[df["type"] == "Run"])
    num_rides =  len(df[df["type"] == "Ride"])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("# Activites", num_activities)
    col2.metric("# Runs", num_runs)
    col3.metric("# Rides", num_rides)
    col4.metric("# Other", num_activities - num_runs - num_rides)
