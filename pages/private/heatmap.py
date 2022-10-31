import pandas as pd
import streamlit as st
from utils import list_options
from utils.fig import heatmap_fig


def get_single_lat_lng(df, i):
    df = df["summary_polyline"].iloc[i]
    df = pd.DataFrame(df, columns=["start_lat", "start_lng"])
    return df


def heatmap(df):
    # Df
    types_available = list_options.activity_types()
    type_selected = st.multiselect("Select activity types",
                                   types_available,
                                   default=types_available)

    df = df[df["type"].isin(type_selected)]

    map_style_selected = st.selectbox("Select map style",
                                      list_options.map_styles(), 0)

    fig = heatmap_fig(df, map_style_selected)

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    heatmap()
