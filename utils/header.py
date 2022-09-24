import streamlit as st


def header():
    """
    Display header
    """
    st.markdown(
        """
        <div>
        <a class="brand" href="/" target="_self">{}</a> &nbsp &nbsp <a class="menu" href="/{}" target="_self">{}</a> &nbsp <a class="menu" href="/{}" target="_self">{}</a> &nbsp <a class="menu" href="/{}" target="_self"">{}</a></div>
        </div>
        """.format("Strava Analytics 🏃", "heatmap", "Heatmap", "grid", "Grid", "map", "Map"), unsafe_allow_html=True)
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.write("")
