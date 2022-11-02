import numpy as np
import pandas as pd
from io import BytesIO
import plotly.express as px
from PIL import Image, ImageOps  
import streamlit as st





@st.cache
def line_fig(df, map_style_selected, line_color, line_thickness, height=500):
    """
    Return plotly map
    """
    fig = px.line_mapbox(df,
                         lat="start_lat",
                         lon="start_lng",
                         height=height,
                         color_discrete_sequence=px.colors.qualitative.Set1)
    zoom, center = _zoom_center(df)
    fig.update_layout(mapbox_style=map_style_selected,
                      mapbox_zoom=zoom,
                      mapbox_center=center,
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_traces(line=dict(color=line_color, width=line_thickness))
    return fig


@st.cache
def heatmap_fig(df, map_style_selected):
    """
    Return plotly heatmap
    """
    fig = px.density_mapbox(df,
                            lat='start_lat',
                            lon='start_lng',
                            radius=10,
                            height=500,
                            center=dict(lat=30, lon=0),
                            zoom=1)
    zoom, center = _zoom_center(df)
    fig.update_layout(mapbox_style=map_style_selected,
                      mapbox_zoom=zoom,
                      mapbox_center=center,
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


@st.cache()
def collage_fig(df, map_style_selected, specs, line_color, line_thickness):
    """
    Return a collage of size specs["len"] with cropped images of polylines
    """
    def _get_single_lat_lng(df, i):
        """
        Return df of single activity with only lat lng data
        """
        df = df["summary_polyline"].iloc[i]
        df = pd.DataFrame(df, columns=["start_lat", "start_lng"])
        return df

    def _get_imgs(df):
        """
        Return list with images as bytes
        """
        imgs = []
        for i in range(0, specs["len"]):
            def get_img(fig, crop=False):
                img_bytes = fig.to_image(format="png")
                str_file = BytesIO(img_bytes)
                if crop == True:
                    pimg = Image.open(str_file)
                    left = 0
                    top = 0
                    right = 700
                    bottom = 680
                    pimg = pimg.crop((left, top, right, bottom))
                    return pimg
                return str_file

            single = _get_single_lat_lng(df, i)
            if len(single > 0):
                fig = line_fig(single, map_style_selected,
                               line_color, line_thickness, 700)
                img = get_img(fig, crop=True)
                imgs.append(img)
        return imgs

    def _get_collage(imgs, specs):
        """
        Return final collage 
        """
        collage = Image.new("RGBA",
                            (specs["w"], specs["h"]),
                            color=(255, 255, 255, 255))
        c = 0
        for i in range(0, specs["h"], specs["wh_single"]):
            for j in range(0, specs["w"], specs["wh_single"]):
                if c < len(imgs):
                    photo = imgs[c].convert("RGBA")
                    photo = photo.resize(
                        (specs["wh_single"], specs["wh_single"]))

                    collage.paste(photo, (j, i))
                    c += 1

        return collage

    imgs = _get_imgs(df)
    collage = _get_collage(imgs, specs)
    return collage


def invert_colors(collage_fig):
    return ImageOps.invert(collage_fig.convert('RGB'))