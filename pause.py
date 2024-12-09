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
        "Authorization": f"Basic {credentials_encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
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
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://api.ws.sonos.com/control/api/v1/households"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error getting households: {response.text}")
    data = response.json()
    household_id = data['households'][0]['id']
    print(f"Household ID retrieved: {household_id}")
    return household_id

def get_group_id(household_id, access_token):
    print("Retrieving group ID...")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error getting groups: {response.text}")
    data = response.json()
    group_id = data['groups'][0]['id']
    print(f"Group ID retrieved: {group_id}")
    return group_id

def pause_playback(group_id, access_token):
    print("Pausing playback...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/playback/pause"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Playback paused successfully.")
    else:
        print(f"Failed to pause playback: {response.status_code} {response.text}")

if __name__ == "__main__":
    refresh_token_value = "pWPbYeKxsAsQQGemUiAzuTTxltXOisfu"
    client_id = "1b66f808-68aa-47db-92dd-13ee474757ba"
    client_secret = "61510ebb-aad5-4691-9efa-05c81260df92"

    try:
        # Refresh the access token
        access_token = refresh_token(refresh_token_value, client_id, client_secret)

        # Retrieve the household ID
        household_id = get_household_id(access_token)

        # Get the current group ID using the household ID
        group_id = get_group_id(household_id, access_token)

        # Pause the playback
        pause_playback(group_id, access_token)
    except Exception as e:
        print(f"An error occurred: {e}")
