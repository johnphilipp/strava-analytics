from utils.activities import get_activites_from_file
from utils.fig import collage_fig
from utils import list_options
import streamlit as st


def poster(df):
    # Df
    types_available = list_options.activity_types()
    type_selected = st.multiselect("Select activity types",
                                   types_available,
                                   default=types_available)

    df = df[df["type"].isin(type_selected)]

    # Map
    map_style_selected = st.selectbox("Select map style",
                                      list_options.map_styles_poster(), 0)

    # Grid size
    size_selected = st.radio(
        "Select poster size", ("3x3", "5x5", "10x10", "20x20"))
    if size_selected == "3x3":
        specs = {"len": 9, "wh_all": 1800, "wh_single": 600}
        if specs["len"] > len(df):
            st.warning(
                "You don't have enough activities to display a " + size_selected)
        else:
            st.image(collage_fig(df, map_style_selected, specs))
    elif size_selected == "5x5":
        specs = {"len": 25, "wh_all": 2000, "wh_single": 400}
        if specs["len"] > len(df):
            st.warning(
                "You don't have enough activities to display a " + size_selected)
        else:
            st.image(collage_fig(df, map_style_selected, specs))
    elif size_selected == "10x10":
        specs = {"len": 100, "wh_all": 2500, "wh_single": 250}
        if specs["len"] > len(df):
            st.warning(
                "You don't have enough activities to display a " + size_selected)
        else:
            st.image(collage_fig(df, map_style_selected, specs))
    elif size_selected == "20x20":
        specs = {"len": 400, "wh_all": 2000, "wh_single": 100}
        if specs["len"] > len(df):
            st.warning(
                "You don't have enough activities to display a " + size_selected)
        else:
            st.image(collage_fig(df, map_style_selected, specs))


if __name__ == "__main__":
    poster()
