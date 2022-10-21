import toml
from supabase import create_client, Client
import pandas as pd


def init():
    url: str = toml.load(".streamlit/secrets.toml")["SUPABASE_URL"]
    key: str = toml.load(".streamlit/secrets.toml")["SUPABASE_KEY"]
    return create_client(url, key)


def insert_activities(athlete_id, fname, lname, json_data):
    supabase = init()
    data = []
    data.append({"athlete_id": athlete_id,
                 "fname": fname,
                "lname": lname,
                 "activities": json_data})
    supabase.table("A").insert(data).execute()
    return "Insert executed"


# def insert_content(athlete_id, content):
#     supabase = init()
#     content = content.to_dict()
#     data = []
#     for i in range(0, len(content["id"])):
#         data.append(
#             {"video_id": video_id, "car_id": car_id, "comment_id": content["id"][i], "content": content["content"][i]})
#     supabase.table("CONTENT").insert(data).execute()
#     return "Insert executed"


# def get_content(video_id):
#     supabase = init()
#     data = supabase.table("SENTIMENT").select(
#         "content").eq("video_id", video_id).execute()
#     df = []
#     for i in data.data:
#         df.append(i["content"])
#     return df
