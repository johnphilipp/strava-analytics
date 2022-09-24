import plotly.express as px
import pandas as pd
import streamlit as st
import polyline
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from IPython.display import Image
from utils import list_options
import imgkit
import io
import PIL.Image
from utils.header import header


def get_df(type_selected):
    df = pd.read_json('data/data.json')
    df = df[["name", "distance", "moving_time", "type", "start_date_local", "achievement_count",
            "kudos_count", "start_latlng", "average_heartrate", "kilojoules", "total_elevation_gain", "map"]]
    df = df[df["type"].isin(type_selected)]
    df[["start_lat", "start_lng"]] = pd.DataFrame(
        df.start_latlng.tolist(), index=df.index)
    df[["id", "summary_polyline", "resource_state"]] = pd.DataFrame(
        df.map.tolist(), index=df.index)
    df = df.drop(columns=["start_latlng", "map", "id", "resource_state"])
    df["summary_polyline"] = df["summary_polyline"].apply(
        lambda x: polyline.decode(x))
    return df


def get_single_lat_lng(df, i):
    df = df["summary_polyline"].iloc[i]
    df = pd.DataFrame(df, columns=["start_lat", "start_lng"])
    return df


def get_fig(df, map_style_selected):
    fig = px.density_mapbox(df, lat='start_lat', lon='start_lng', radius=10,
                            center=dict(lat=30, lon=0), zoom=1)
    fig.update_layout(mapbox_style=map_style_selected,
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
    df = get_df(type_selected)

    map_style_selected = st.selectbox("Select map style",
                                      list_options.map_styles(), 0)

    fig = get_fig(df, map_style_selected)

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
