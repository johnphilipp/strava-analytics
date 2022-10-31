import pandas as pd
import polyline


def convert_json_to_df(json_data):
    """
    Convert json to df
    """
    return pd.json_normalize(json_data)


def process_data(df):
    """
    Return modified df of activities
    """
    if "map" in df.keys():
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
                 "map"]]
        df[["start_lat", "start_lng"]] = pd.DataFrame(
            df.start_latlng.tolist(), index=df.index)
        df[["end_lat", "ent_lng"]] = pd.DataFrame(
            df.end_latlng.tolist(), index=df.index)
        df = df[~df["map"].isnull()]
        df[["id", "summary_polyline", "resource_state"]] = pd.DataFrame(
            df.map.tolist(), index=df.index)
        df = df.drop(columns=["start_latlng", "end_latlng",
                              "map", "id", "resource_state"])
        df["summary_polyline"] = df["summary_polyline"].apply(
            lambda x: polyline.decode(x))
    else:
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
        df["summary_polyline"] = df["map.summary_polyline"].apply(
            lambda x: polyline.decode(x))
    return df
