from lib2to3.pgen2.pgen import DFAState
import streamlit as st
from streamlit_option_menu import option_menu
from public_pages.login import login
from private_pages.dashboard import dashboard
from private_pages.poster import poster
from private_pages.heatmap import heatmap
from auth.auth import get_refresh_token_and_access_token, get_athlete_activities
from datetime import datetime
from utils.process_data import process_data
from database import db


with open("style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# st.set_page_config(layout="centered", page_icon="🏃‍♀️",
#                    page_title="Strava Analytics")

if "code" in st.experimental_get_query_params() or 'user_authenticated' in st.session_state:
    if "df" in st.session_state:
        df = st.session_state["df"]
        json_data = st.session_state["data"]
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
            print(tokens)
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

        if "data" in st.session_state:
            json_data = st.session_state["data"]
            df = st.session_state["df"]
        else:
            num_activities = 200
            epoch = ""
            nested_list = []
            with st.spinner('Hang tight {}, we are retrieving your activities!'.format(athlete_fname)):
                for i in range(15):
                    new = get_athlete_activities(
                        access_token, num_activities, epoch)
                    nested_list.append(new)

                    if len(new) == 0:
                        break
                    else:
                        timestamp_last = new[len(new) - 1]["start_date"]
                        utc = datetime.strptime(
                            timestamp_last, "%Y-%m-%dT%H:%M:%SZ")
                        epoch = str(
                            int((utc - datetime(1970, 1, 1)).total_seconds()))

                json_data = [
                    item for sublist in nested_list for item in sublist]
                df = process_data(json_data)

                st.session_state["data"] = json_data
                st.session_state["df"] = df

                db.insert_activities(athlete_id,
                                     athlete_fname,
                                     athlete_lname,
                                     json_data)

                st.session_state["user_authenticated"] = auth_code
                # print(json_data)
                # print(len(json_data))

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

    # menu_selection = option_menu("Strava Analytics",
    #                              ["Dashboard", "Heatmap", "Poster"],
    #                              menu_icon="bicycle",
    #                              icons=["speedometer", "map", "card-image"])
    # if menu_selection == "Dashboard":
    #     dashboard(df)
    # if menu_selection == "Heatmap":
    #     heatmap(df)
    # if menu_selection == "Poster":
    #     poster(df)

else:
    menu_selection = option_menu("Strava Analytics",
                                 ["Login"],
                                 menu_icon="bicycle",
                                 icons=["user"])

    st.write("#")

    if menu_selection == "Login":
        login()

# Make a cURL request to exchange the authorization code and scope for a refresh token, access token, and access token expiration date (step 7a from the graph).
