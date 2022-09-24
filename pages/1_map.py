import plotly.express as px
import pandas as pd
import streamlit as st
import polyline
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from IPython.display import Image
from utils import list_options
from utils.header import header
from utils.activities import get_activites_from_file


def get_single_lat_lng(df, i):
    df = df["summary_polyline"].iloc[i]
    df = pd.DataFrame(df, columns=["start_lat", "start_lng"])
    return df


def get_fig(df, map_style_selected):
    fig = px.line_mapbox(df,
                         lat="start_lat",
                         lon="start_lng",
                         zoom=3,
                         height=300,
                         color_discrete_sequence=["fuchsia"])
    fig.update_layout(mapbox_style=map_style_selected,
                      mapbox_zoom=12,
                      mapbox_center_lat=df.loc[0][0],
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def main():
    st.set_page_config(layout="centered", page_icon="📊",
                       page_title="senty")

    header()

    # Df
    types_available = list_options.activity_types()
    type_selected = st.multiselect("Select activity types",
                                   types_available,
                                   default=types_available)
    df = get_activites_from_file("data/activities.json")
    df = df = df[df["type"].isin(type_selected)]

    # Single
    activities_available = df["name"].values.tolist()  # start_date_local
    selected_activity = st.selectbox("Select activity", range(len(activities_available)),
                                     format_func=lambda x: activities_available[x])

    # Map
    map_style_selected = st.selectbox("Select map style",
                                      list_options.map_styles(), 0)

    single = get_single_lat_lng(df, selected_activity)
    fig = get_fig(single, map_style_selected)
    # fig.write_image("img/fig1.png")
    img_bytes = fig.to_image(format="png")

    st.plotly_chart(fig,
                    use_container_width=True)


if __name__ == "__main__":
    main()
