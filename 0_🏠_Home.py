import streamlit as st
from pages.private.logout import logout
from pages.private.get_started import get_started
from auth.auth import get_refresh_token_and_access_token, get_athlete_activities
from datetime import datetime
from utils.process_data import process_data, convert_json_to_df
from database import db
import pandas as pd
import altair as alt
from utils.switch_page import switch_page


def activities_top(df):
    st.write(
        "### Your Top Activities:".format(len(df)))
    st.write("#####")

    cols = st.columns(6)  # len(df["type"].unique()) + 1
    for i, col in enumerate(cols):
        if i == 0:
            col.metric("All Activites", len(df), "Wow!")
        elif i <= len(df["type"].unique()):
            col.metric("{}s".format(df["type"].value_counts().index.tolist()[i-1]), str(
                df["type"].value_counts()[i-1]))


def activities_bar(df):
    st.write("#####")
    st.write(
        "### All Your Activities:".format(len(df)))

    types_selected = st.multiselect("Select activities",
                                    df["type"].value_counts().index.tolist(), df["type"].value_counts().index.tolist())
    st.write("#####")

    df = pd.DataFrame({
        "Type": df[df["type"].isin(types_selected)]["type"].value_counts().index.tolist(),
        "Number of Activites": df[df["type"].isin(types_selected)]["type"].value_counts()
    })

    c = alt.Chart(df).mark_bar().encode(
        x='Type',
        y='Number of Activites',
        color=alt.Color('Type', legend=alt.Legend(
            title="Type", orient="bottom"))
    ).configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)

    st.altair_chart(c, use_container_width=True)


def dashboard(df):
    activities_top(df)
    activities_bar(df)


def new_auth():
    if "code" in st.experimental_get_query_params() \
            or "user_authenticated" in st.session_state \
            or "json_data" in st.session_state \
            or "df" in st.session_state:

        if "df" in st.session_state:
            df = st.session_state["df"]
        elif "json_data" in st.session_state:
            json_data = st.session_state["json_data"]
            df = convert_json_to_df(json_data)
            df = process_data(json_data)
        else:
            auth_code = st.experimental_get_query_params()["code"][0]
            st.experimental_set_query_params()

            if "refresh_token" in st.session_state and "access_token" in st.session_state:
                refresh_token = st.session_state["refresh_token"]
                access_token = st.session_state["access_token"]
                athlete_id = st.session_state["athlete_id"]
                athlete_fname = st.session_state["athlete_fname"]
                athlete_lname = st.session_state["athlete_lname"]
                athlete_image_url = st.session_state["athlete_image_url"]

            else:
                tokens = get_refresh_token_and_access_token(auth_code)
                athlete_id = tokens["athlete"]["id"]
                athlete_fname = tokens["athlete"]["firstname"]
                athlete_lname = tokens["athlete"]["lastname"]
                athlete_image_url = tokens["athlete"]["profile"]
                refresh_token = tokens["refresh_token"]
                access_token = tokens["access_token"]
                st.session_state["athlete_id"] = athlete_id
                st.session_state["athlete_fname"] = athlete_fname
                st.session_state["athlete_lname"] = athlete_lname
                st.session_state["athlete_image_url"] = athlete_image_url
                st.session_state["refresh_token"] = refresh_token
                st.session_state["access_token"] = access_token

            if "json_data" in st.session_state:
                json_data = st.session_state["json_data"]
                df = st.session_state["df"]
            else:
                num_activities = 200
                epoch = round(
                    (datetime.now() - datetime(1970, 1, 1)).total_seconds())
                nested_list = []
                with st.spinner('Hang tight, {}! We are retrieving your activities'.format(athlete_fname)):
                    for i in range(15):  # while len(new) != 0
                        new = get_athlete_activities(
                            access_token, num_activities, epoch)
                        nested_list.append(new)

                        if len(new) == 0:
                            break
                        else:
                            timestamp_last = new[len(
                                new) - 1]["start_date_local"]
                            utc = datetime.strptime(
                                timestamp_last, "%Y-%m-%dT%H:%M:%SZ")
                            epoch = str(
                                int((utc - datetime(1970, 1, 1)).total_seconds()))

                    json_data = [
                        item for sublist in nested_list for item in sublist]
                    df = convert_json_to_df(json_data)
                    df = process_data(df)

                    st.session_state["json_data"] = json_data
                    st.session_state["df"] = df

                    db.insert_activities(athlete_id,
                                         athlete_fname,
                                         athlete_lname,
                                         json_data)

                    st.session_state["user_authenticated"] = auth_code

        st.experimental_rerun()


def main():
    st.set_page_config(layout="centered",
                       page_icon="🏃‍♀️",
                       page_title="Strava Analytics")
    if "df" in st.session_state:
        st.write("# Dashboard")
        df = st.session_state["df"]
        dashboard(df)
        st.write("####")
        if st.button("📍 Heatmap Visualizer"):
            switch_page("heatmap visualizer")
        if st.button("🌌 Poster Maker"):
            switch_page("poster maker")
        if st.button("📅 Calendar Tracker"):
            switch_page("calendar tracker")
        if st.button("🔚 Logout.py"):
            switch_page("logout")
    else:
        get_started()
        new_auth()
    with open("pages/style/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
