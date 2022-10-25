import toml
import urllib
import requests


def get_authorization_url():
    """Generate authorization uri"""
    app_url = "https://strava.streamlitapp.com"  # http://strava.streamlitapp.com os.getenv('APP_URL', 'http://localhost')
    params = {
        "client_id": toml.load(".streamlit/secrets.toml")["STRAVA_CLIENT_ID"],
        "response_type": "code",
        "redirect_uri": "{}".format(app_url),
        "scope": "read,profile:read_all,activity:read",
        "approval_prompt": "force"
    }
    values_url = urllib.parse.urlencode(params)
    base_url = 'https://www.strava.com/oauth/authorize'
    rv = base_url + '?' + values_url
    return rv


def get_refresh_token_and_access_token(auth_code):
    """POST request to retrieve refresh_token and access_token"""
    params = {
        "client_id": toml.load(".streamlit/secrets.toml")["STRAVA_CLIENT_ID"],
        "client_secret": toml.load(".streamlit/secrets.toml")["STRAVA_CLIENT_SECRET"],
        "code": auth_code,
        "grant_type": "authorization_code"
    }
    values_url = urllib.parse.urlencode(params)
    base_url = 'https://www.strava.com/oauth/token'
    rv = base_url + '?' + values_url
    return requests.request("POST", rv).json()


def get_athlete_activities(access_token, per_page=200, after=""):
    """GET request to retrieve athlete activities"""
    if after == "":
        params = {
            "access_token": access_token,
            "per_page": per_page
        }
    else:
        params = {
            "access_token": access_token,
            "after": after,
            "per_page": per_page
        }
    values_url = urllib.parse.urlencode(params)
    base_url = 'https://www.strava.com/api/v3/athlete/activities'
    rv = base_url + '?' + values_url
    return requests.request("GET", rv).json()
