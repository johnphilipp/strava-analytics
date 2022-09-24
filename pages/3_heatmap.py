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
from utils.fig import heatmap_fig


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

    map_style_selected = st.selectbox("Select map style",
                                      list_options.map_styles(), 0)

    fig = heatmap_fig(df, map_style_selected)

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
