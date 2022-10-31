import streamlit as st
from streamlit_option_menu import option_menu
from pages.public.login import login
from pages.public.upload import upload
from pages.private.dashboard import dashboard
from pages.private.poster import poster
from pages.private.heatmap import heatmap
from auth.auth import get_refresh_token_and_access_token, get_athlete_activities
from datetime import datetime
from utils.process_data import process_data, convert_json_to_df
from database import db


with open("style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# st.set_page_config(layout="centered", page_icon="🏃‍♀️",
#                    page_title="Strava Analytics")

print(st.session_state)

if "code" in st.experimental_get_query_params() \
        or "user_authenticated" in st.session_state \
        or "json_data" in st.session_state \
        or "df" in st.session_state:

    if "df" in st.session_state:
        df = st.session_state["df"]
        print(df.keys())
    elif "json_data" in st.session_state:
        json_data = st.session_state["json_data"]
        df = convert_json_to_df(json_data)
        df = process_data(json_data)
        print(df.keys())
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
                        timestamp_last = new[len(new) - 1]["start_date_local"]
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

    menu_selection = option_menu("Strava Analytics",
                                 ["Dashboard", "Heatmap", "Poster"],
                                 menu_icon="bicycle",
                                 icons=["speedometer", "map", "card-image"])
    st.write("#")

    if menu_selection == "Dashboard":
        dashboard(df)
    if menu_selection == "Heatmap":
        heatmap(df)
    if menu_selection == "Poster":
        poster(df)

    # TODO: Add logout -- kill all states, reboot app

else:
    menu_selection = option_menu("Strava Analytics",
                                 ["Login", "Upload"],
                                 menu_icon="bicycle",
                                 icons=["person-check-fill", "upload"])

    st.write("#")

    if menu_selection == "Login":
        login()
    if menu_selection == "Upload":
        upload()
