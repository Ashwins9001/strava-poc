import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
EXPIRES_AT = int(os.getenv("EXPIRES_AT"))

def refresh_strava_token():
    print("Refreshing token...")
    response = requests.post("https://www.strava.com/oauth/token", data={
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
    with open('.env', 'r') as file:
        lines = file.readlines()

    with open('.env', 'w') as file:
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
        return refresh_strava_token()
    return ACCESS_TOKEN

def get_athlete_information(access_token):
    headers = {'Authorization': f'Bearer {token}'}
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
    
token = get_valid_token()

athlete_id, athlete_name = get_athlete_information(token)

stats_response = get_activity_stats(token, athlete_id, athlete_name)

print(stats_response)