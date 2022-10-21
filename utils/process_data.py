from email.policy import default
import pandas as pd
import polyline


def process_data(json_data):
    """
    Return modified df of activities
    """
    df = pd.json_normalize(json_data)
    df = df[["name",
             "distance",
             "moving_time",
             "type",
             "start_date_local",
             "achievement_count",
             "kudos_count",
             "start_latlng",
             "end_latlng",
             "average_heartrate",
             "total_elevation_gain",
             "map.summary_polyline"]]
    df[["start_lat", "start_lng"]] = pd.DataFrame(
        df.start_latlng.tolist(), index=df.index)
    df[["end_lat", "ent_lng"]] = pd.DataFrame(
        df.end_latlng.tolist(), index=df.index)
    # df = df[~df["map.summary_polyline"].isnull()]
    # df[["id", "summary_polyline", "resource_state"]] = pd.DataFrame(
    #     df.map.tolist(), index=df.index)
    df["summary_polyline"] = df["map.summary_polyline"].apply(
        lambda x: polyline.decode(x))
    return df
