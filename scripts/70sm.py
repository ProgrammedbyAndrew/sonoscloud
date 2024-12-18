import requests
import base64
import time

def refresh_token(refresh_token_value, client_id, client_secret):
    print("Refreshing access token...")
    url = "https://api.sonos.com/login/v3/oauth/access"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token_value
    }

    credentials = f"{client_id}:{client_secret}"
    credentials_encoded = base64.b64encode(credentials.encode()).decode()
    headers = {
        "accept": "application/json",
        "Authorization": f"Basic {credentials_encoded}"
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        raise Exception(f"Error refreshing token: {response.text}")

    data = response.json()
    print("Access token refreshed.")
    return data['access_token']

def get_household_id(access_token):
    print("Retrieving household ID...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    get_households_url = "https://api.ws.sonos.com/control/api/v1/households"
    households_response = requests.get(get_households_url, headers=headers)
    if households_response.status_code != 200:
        raise Exception(f"Error getting households: {households_response.text}")

    households_data = households_response.json()
    household_id = households_data['households'][0]['id']
    print(f"Household ID retrieved: {household_id}")
    return household_id

def get_group_id(household_id, access_token):
    print("Retrieving group ID...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    get_groups_url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups"
    groups_response = requests.get(get_groups_url, headers=headers)
    if groups_response.status_code != 200:
        raise Exception(f"Error getting groups: {groups_response.text}")

    groups_data = groups_response.json()
    group_id = groups_data['groups'][0]['id']
    print(f"Group ID retrieved: {group_id}")
    return group_id

def load_favorite_playlist(group_id, favorite_playlist_id, access_token):
    print(f"Loading favorite playlist with ID: {favorite_playlist_id}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    load_favorite_url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/favorites"
    payload = {"favoriteId": favorite_playlist_id}
    response = requests.post(load_favorite_url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Error loading favorite: {response.text}")
    print(f"Favorite playlist {favorite_playlist_id} loaded.")

def set_group_volume(group_id, volume, access_token):
    print(f"Setting group volume to {volume}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    volume_url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/groupVolume"
    volume_payload = {"volume": volume}
    volume_response = requests.post(volume_url, headers=headers, json=volume_payload)
    if volume_response.status_code != 200:
        raise Exception(f"Error setting volume for group {group_id}: {volume_response.text}")
    print(f"Volume set to {volume} for group {group_id}.")

def play_group(group_id, access_token):
    print(f"Starting playback for group {group_id}...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    play_url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/playback/play"
    play_response = requests.post(play_url, headers=headers)
    if play_response.status_code != 200:
        raise Exception(f"Playback error {play_response.status_code}: {play_response.text}")
    print(f"Playback started for group {group_id}.")

# Usage:
refresh_token_value = "pWPbYeKxsAsQQGemUiAzuTTxltXOisfu"
client_id = "1b66f808-68aa-47db-92dd-13ee474757ba"
client_secret = "61510ebb-aad5-4691-9efa-05c81260df92"

access_token = refresh_token(refresh_token_value, client_id, client_secret)
household_id = get_household_id(access_token)
group_id = get_group_id(household_id, access_token)



#### SCHEDULE GOES HERE ####

# Play the Social Media Commercial  
favorite_playlist_id_1 = "30"
desired_volume_1 = 75
load_favorite_playlist(group_id, favorite_playlist_id_1, access_token)
set_group_volume(group_id, desired_volume_1, access_token)
play_group(group_id, access_token)
print("The announceent is playing")
time.sleep(23)

# Play the Social Media Commercial - Spanish 
favorite_playlist_id_1 = "31"
desired_volume_1 = 75
load_favorite_playlist(group_id, favorite_playlist_id_1, access_token)
set_group_volume(group_id, desired_volume_1, access_token)
play_group(group_id, access_token)
print("The announceent is playing")
time.sleep(27)

# PLAY THE MAIN PLAYLIST
favorite_playlist_id_2 = "11"
desired_volume_2 = 70
load_favorite_playlist(group_id, favorite_playlist_id_2, access_token)
set_group_volume(group_id, desired_volume_2, access_token)
play_group(group_id, access_token)
print("The Music is Playing")



