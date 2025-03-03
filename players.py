import requests
import base64

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

def get_all_player_ids(household_id, access_token):
    print("Fetching all player IDs...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    get_groups_url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups"
    groups_response = requests.get(get_groups_url, headers=headers)
    if groups_response.status_code != 200:
        raise Exception(f"Error getting groups: {groups_response.text}")
    
    groups_data = groups_response.json()
    print("Raw groups data:", groups_data)  # Debug output
    
    all_players = []
    for group in groups_data.get('groups', []):
        group_players = group.get('players', [])
        all_players.extend(group_players)
    
    if not all_players:
        print("No players found in any groups.")
    else:
        print("Player IDs found:")
        for player in all_players:
            player_id = player.get('id', 'N/A')
            print(f" - {player_id}")

# Usage:
refresh_token_value = "pWPbYeKxsAsQQGemUiAzuTTxltXOisfu"
client_id = "1b66f808-68aa-47db-92dd-13ee474757ba"
client_secret = "61510ebb-aad5-4691-9efa-05c81260df92"

try:
    access_token = refresh_token(refresh_token_value, client_id, client_secret)
    household_id = get_household_id(access_token)
    get_all_player_ids(household_id, access_token)
except Exception as e:
    print("An error occurred:")
    print(e)