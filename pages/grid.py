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


# Df
types_available = list_options.activity_types()
type_selected = st.multiselect("Select activity types",
                               types_available,
                               default=types_available)
df = get_df(type_selected)

# Map
map_style_selected = st.selectbox("Select map style",
                                  list_options.map_styles(), 0)
num_items = st.select_slider(
    "Select number of items", list(range(0, len(df))), 3)

cols = st.columns(3)
for i in range(0, num_items):
    single = get_single_lat_lng(df, i)
    fig = get_fig(single, map_style_selected)
    # fig.write_image("img/fig1.png")

    def get_img(fig, crop=False):
        img_bytes = fig.to_image(format="png")
        str_file = io.BytesIO(img_bytes)
        if crop == True:
            pimg = PIL.Image.open(str_file)
            left = 0
            top = 0
            right = 700
            bottom = 280
            pimg = pimg.crop((left, top, right, bottom))
            return pimg
        return str_file

    img = get_img(fig, crop=False)
    cols[i % 3].image(img)
