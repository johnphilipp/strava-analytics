import pandas as pd
import polyline


class ActivityList():
    def __init__(self, data):
        self._data = data
        self._df = self.convert_json_to_df()
        self._num_activities = len(self._df)
        self._num_runs = len(self._df[self._df["type"] == "Run"])
        self._num_rides = len(self._df[self._df["type"] == "Ride"])
        self._num_hikes = len(self._df[self._df["type"] == "Hike"])
        self._num_walks = len(self._df[self._df["type"] == "Walk"])

    def get_df(self):
        return self._df

    def get_num_activities(self):
        return self._num_activities

    def get_num_runs(self):
        return self._num_runs

    def get_num_rides(self):
        return self._num_rides

    def get_num_hikes(self):
        return self._num_hikes

    def get_num_walks(self):
        return self._num_walks

    def convert_json_to_df(self):
        """
        Convert json to df
        """
        return pd.json_normalize(self._data)

    def process_df(self):
        """
        Modify df of activities:
        > Remove unnecessary cols
        > Decode polyline
        """
        df = self._df
        df[["start_lat", "start_lng"]] = pd.DataFrame(
            df.start_latlng.tolist(), index=df.index)
        df[["end_lat", "ent_lng"]] = pd.DataFrame(
            df.end_latlng.tolist(), index=df.index)

        if "map.summary_polyline" in df.keys():
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
            df = df[~df["map.summary_polyline"].isnull()]
            df["map.summary_polyline"] = df["map.summary_polyline"].apply(
                lambda x: polyline.decode(x))
            df = df.rename(
                columns={"map.summary_polyline": "summary_polyline"})

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
                     "map"]]
            df = df[~df["map"].isnull()]
            df[["id", "summary_polyline", "resource_state"]] = pd.DataFrame(
                df.map.tolist(), index=df.index)
            df["summary_polyline"] = df["summary_polyline"].apply(
                lambda x: polyline.decode(x))
            df = df.drop(columns=["map", "id", "resource_state"])

        df = df.drop(columns=["start_latlng", "end_latlng"])
        return df
