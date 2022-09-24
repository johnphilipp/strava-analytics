import requests
import json
import time
import yaml
import pandas as pd
import polyline


def _get_access_token():
    """
    Get Strava authorization token
    """
    config = yaml.safe_load(open("config.yaml"))

    with open('data/strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)

    def _refresh_strava_tokens():
        """
        Make Strava auth API call with current refresh token
        Return new strava_tokens
        """
        response = requests.post(
            url='https://www.strava.com/oauth/token',
            data={
                'client_id': config["CLIENT_ID"],
                'client_secret': config["CLIENT_SECRET"],
                'code': config["AUTH_CODE"],
                'grant_type': 'authorization_code'
            }
        )
        new_strava_tokens = response.json()

        with open('strava_tokens.json', 'w') as f:
            json.dump(new_strava_tokens, f)

        return new_strava_tokens

    if strava_tokens['expires_at'] < time.time():
        strava_tokens = _refresh_strava_tokens()

    return strava_tokens['access_token']


def _get_df(path):
    """
    Return modified df of activities
    """
    df = pd.read_json(path)
    df = df[["name", "distance", "moving_time", "type", "start_date_local", "achievement_count", "kudos_count",
             "start_latlng", "end_latlng", "average_heartrate", "kilojoules", "total_elevation_gain", "map"]]
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
    return df


def get_activites_from_api():
    """
    Return activities via Strava API
    Use Strava ACCESS_TOKEN to loop though all activities
    """
    URL = "https://www.strava.com/api/v3/activities"
    ACCESS_TOKEN = _get_access_token()
    page = 1
    activities = []

    while True:
        r = requests.get(URL + '?access_token=' + ACCESS_TOKEN +
                         '&per_page=200' + '&page=' + str(page))
        r = r.json()
        if (not r):
            break
        else:
            for i in range(0, len(r)):
                activities.append(r[i])
            page += 1

    with open("data/activities.json", "w") as f:
        json.dump(activities, f)

    return _get_df("data/activities.json")


def get_activites_from_file(path):
    """
    Return activities from path
    """
    return _get_df(path)


def main():
    get_activites_from_file("data/activities.json")


if __name__ == "__main__":
    main()
