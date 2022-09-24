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
from utils.activities import get_activites_from_file
from utils.fig import line_fig


def get_single_lat_lng(df, i):
    df = df["summary_polyline"].iloc[i]
    df = pd.DataFrame(df, columns=["start_lat", "start_lng"])
    return df


def main():
    st.set_page_config(layout="centered", page_icon="📊",
                       page_title="senty")

    header()

    # Df
    types_available = list_options.activity_types()
    type_selected = st.multiselect("Select activity types",
                                   types_available,
                                   default=types_available)
    path = "data/activities_public.json"
    df = get_activites_from_file(path)
    df = df = df[df["type"].isin(type_selected)]

    # Map
    map_style_selected = st.selectbox("Select map style",
                                      list_options.map_styles(), 0)

    if len(df) < 12:
        preselected = len(df)
    else:
        preselected = 12

    num_items = st.select_slider(
        "Select number of items", list(range(0, len(df) + 1)), preselected)

    cols = st.columns(3)
    for i in range(0, num_items):
        single = get_single_lat_lng(df, i)
        fig = line_fig(single, map_style_selected)
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


if __name__ == "__main__":
    main()
