import pandas as pd
import streamlit as st
from utils import list_options
from utils.fig import heatmap_fig
from pages.private.get_started import get_started
from utils.switch_page import switch_page


def get_single_lat_lng(df, i):
    df = df["summary_polyline"].iloc[i]
    df = pd.DataFrame(df, columns=["start_lat", "start_lng"])
    return df


def heatmap(df):
    types_available = list_options.activity_types()
    type_selected = st.multiselect("Select activity types",
                                   types_available,
                                   default=types_available)

    df = df[df["type"].isin(type_selected)]

    map_style_selected = st.selectbox("Select map style",
                                      list_options.map_styles(), 0)

    fig = heatmap_fig(df, map_style_selected)

    st.plotly_chart(fig, use_container_width=True)


def main():
    if "df" in st.session_state:
        st.write("# Heatmap")
        df = st.session_state["df"]
        heatmap(df)
        st.write("####")
        if st.button("🏠 Home"):
            switch_page("home")
        if st.button("🌌 Poster Maker"):
            switch_page("poster maker")
        if st.button("📅 Calendar Tracker"):
            switch_page("calendar tracker")
        if st.button("🔚 Logout.py"):
            switch_page("logout")
    else:
        get_started()
    with open("pages/style/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
