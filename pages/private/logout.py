import streamlit as st
import pandas as pd


def logout():
    st.write("#")
    if st.button("🔚 Logout"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
