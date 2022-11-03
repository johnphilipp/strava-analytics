from utils.activities import get_activites_from_file
from utils import fig
from utils import list_options
import streamlit as st


def poster(df):
    # Df
    types_available = list_options.activity_types()
    type_selected = st.multiselect(
        "Select activity types", types_available, default=types_available)

    df = df[df["type"].isin(type_selected)]

    # Map
    map_style_selected = st.selectbox(
        "Select map style", list_options.map_styles_poster(), 0)

    # Line color
    line_color = st.selectbox(
        "Select line color", ["Black", "Green", "Red"])
    
    # Invert colors
    invert_colors = st.selectbox(
        "Invert colors? (Black background)", ["No", "Yes"])

    # Line thickness
    line_thickness = st.selectbox(
        "Select line thickness", [1, 2, 5, 10, 20, 30])

    # Grid size
    size_selected = st.radio(
        "Select poster size", ("3x3", "5x5", "5x10", "10x10", "10x20", "20x20", "20x40", "20x50", "25x25", "50x20"))

    if size_selected == "3x3":
        specs = {"len": 9, "w": 1800, "h": 1800, "wh_single": 600}
    elif size_selected == "5x5":
        specs = {"len": 25, "w": 2000, "h": 2000, "wh_single": 400}
    elif size_selected == "5x10":
        specs = {"len": 50, "w": 2000, "h": 1000, "wh_single": 200}
    elif size_selected == "10x10":
        specs = {"len": 100, "w": 2500, "h": 2500, "wh_single": 250}
    elif size_selected == "10x20":
        specs = {"len": 200, "w": 2000, "h": 1000, "wh_single": 100}
    elif size_selected == "20x20":
        specs = {"len": 400, "w": 2000, "h": 2000, "wh_single": 100}
    elif size_selected == "20x40":
        specs = {"len": 800, "w": 2000, "h": 4000, "wh_single": 100}
    elif size_selected == "20x50":
        specs = {"len": 1000, "w": 1000, "h": 2500, "wh_single": 50}
    elif size_selected == "25x25":
        specs = {"len": 625, "w": 2500, "h": 2500, "wh_single": 100}
    elif size_selected == "50x20":
        specs = {"len": 1000, "w": 2500, "h": 1000, "wh_single": 50}

    if specs["len"] > len(df):
        st.warning("You don't have enough activities to display a {}".format(size_selected))
    else:
        # TODO: Progress bar
        collage_fig = fig.collage_fig(df, map_style_selected, specs, line_color, line_thickness)
        if invert_colors == "Yes":
            collage_fig = fig.invert_colors_collage(collage_fig)
        st.image(collage_fig)


if __name__ == "__main__":
    poster()
