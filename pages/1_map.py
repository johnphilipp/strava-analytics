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
from utils.fig import line_fig
from typing import Tuple


def zoom_center(df):
    lats = df["start_lat"]
    lons = df["start_lng"]

    maxlon, minlon = max(lons), min(lons)
    maxlat, minlat = max(lats), min(lats)
    center = {
        'lon': round((maxlon + minlon) / 2, 6),
        'lat': round((maxlat + minlat) / 2, 6)
    }

    # longitudinal range by zoom level (20 to 1)
    # in degrees, if centered at equator
    lon_zoom_range = np.array([
        0.0007, 0.0014, 0.003, 0.006, 0.012, 0.024, 0.048, 0.096,
        0.192, 0.3712, 0.768, 1.536, 3.072, 6.144, 11.8784, 23.7568,
        47.5136, 98.304, 190.0544, 360.0
    ])

    margin = 2.5
    height = (maxlat - minlat) * margin * 2.0
    width = (maxlon - minlon) * margin
    lon_zoom = np.interp(width, lon_zoom_range, range(20, 0, -1))
    lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
    zoom = round(min(lon_zoom, lat_zoom), 2)

    return zoom, center


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

    # Single
    activities_available = df["name"].values.tolist()  # start_date_local
    selected_activity = st.selectbox("Select activity", range(len(activities_available)),
                                     format_func=lambda x: activities_available[x])

    # Map
    map_style_selected = st.selectbox("Select map style",
                                      list_options.map_styles(), 0)

    single = get_single_lat_lng(df, selected_activity)
    fig = line_fig(single, map_style_selected)
    # fig.write_image("img/fig1.png")
    img_bytes = fig.to_image(format="png")

    st.plotly_chart(fig,
                    use_container_width=True)


if __name__ == "__main__":
    main()
