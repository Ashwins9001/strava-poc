import os
import time
import requests
from dotenv import load_dotenv
import urllib.parse
import polyline

from . import map_functions

load_dotenv()

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
EXPIRES_AT = int(os.getenv("EXPIRES_AT"))
SCOPE = os.getenv("SCOPE")
AUTH_CODE=os.getenv("AUTHENTICATION_CODE")

def authenticate_to_read_all_scope():
    print('here')

    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': 'http://localhost/exchange_token',
        'response_type': 'code',
        'approval_prompt': 'force',
        'scope': SCOPE
    }

    url = f"https://www.strava.com/oauth/authorize?{urllib.parse.urlencode(params)}"
    print("Go to this URL in your browser to authorize the app:")
    print(url)

def get_refresh_token():
    print("Getting refresh token given authorization code...")
    response = requests.post("https://www.strava.com/api/v3/oauth/token", data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': AUTH_CODE,
        'grant_type': 'authorization_code'
    })
    
    if response.status_code == 200:
        new_tokens = response.json()
        access_token = new_tokens['access_token']
        refresh_token = new_tokens['refresh_token']
        expires_at = new_tokens['expires_at']

        update_env_file(access_token, refresh_token, expires_at)

        return access_token
    else:
        raise Exception("Failed to refresh token: " + response.text)

def update_refresh_token():
    print("Refreshing access token...")
    response = requests.post("https://www.strava.com/api/v3/oauth/token", data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN
    })
    
    if response.status_code == 200:
        new_tokens = response.json()
        access_token = new_tokens['access_token']
        refresh_token = new_tokens['refresh_token']
        expires_at = new_tokens['expires_at']

        update_env_file(access_token, refresh_token, expires_at)
        return access_token
    else:
        raise Exception("Failed to refresh token: " + response.text)

def update_env_file(access_token, refresh_token, expires_at):
    with open(env_path, 'r') as file:
        lines = file.readlines()

    with open(env_path, 'w') as file:
        for line in lines:
            if line.startswith("ACCESS_TOKEN="):
                file.write(f"ACCESS_TOKEN={access_token}\n")
            elif line.startswith("REFRESH_TOKEN="):
                file.write(f"REFRESH_TOKEN={refresh_token}\n")
            elif line.startswith("EXPIRES_AT="):
                file.write(f"EXPIRES_AT={expires_at}\n")
            else:
                file.write(line)

def get_valid_token():
    if time.time() > EXPIRES_AT:
        return update_refresh_token()
    return ACCESS_TOKEN

def get_athlete_information(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get("https://www.strava.com/api/v3/athlete", headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to get athlete information")

    athlete_id = response.json()['id']
    first_name = response.json()['firstname']
    
    return athlete_id, first_name

def get_activity_stats(access_token, athlete_id, athlete_name):
    response = requests.get(f"https://www.strava.com/api/v3/athletes/{athlete_id}/stats", headers = {
    'Authorization': f'Bearer {access_token}'
    })

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to get activity stats for athlete: {0}".format(athlete_id))

def get_activities(access_token):
    response = requests.get("https://www.strava.com/api/v3/athlete/activities", headers = {
    'Authorization': f'Bearer {access_token}'}, params = {"per_page": 100, "page": 1}
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to get activities")

def initialize_responses():
    token = get_valid_token()
    athlete_id, athlete_name = get_athlete_information(token)
    stats_response = get_activity_stats(token, athlete_id, athlete_name)
    activities_response = get_activities(token)
    print("Athlete activities as listed: {0}".format(activities_response))
    show_activities_on_map(activities_response)


def show_activities_on_map(activities):
    coordinates = []
    for activity in activities:
        coordinates = coordinates + polyline.decode(activity['map']['summary_polyline'])
    map_functions.generate_map(coordinates, threshold_km=8)

def main():
    initialize_responses()