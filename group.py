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
        raise Exception(f"Error refreshing token: {response.status_code} - {response.text}")
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
        raise Exception(f"Error getting households: {households_response.status_code} - {households_response.text}")
    households_data = households_response.json()
    household_id = households_data['households'][0]['id']
    print(f"Household ID retrieved: {household_id}")
    return household_id

def get_groups(household_id, access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error getting groups: {response.status_code} - {response.text}")
    groups = response.json().get('groups', [])
    return groups

def poll_for_group(household_id, access_token, player_ids, timeout=30, interval=2):
    """
    Poll the groups endpoint until a group that contains all specified player_ids appears,
    or until timeout (in seconds) is reached.
    """
    start_time = time.time()
    target_set = set(player_ids)
    while time.time() - start_time < timeout:
        groups = get_groups(household_id, access_token)
        for group in groups:
            group_set = set(group.get('playerIds', []))
            # Check if the new group contains all desired players.
            if target_set.issubset(group_set):
                return group['id']
        time.sleep(interval)
    raise Exception("Timed out waiting for the group to be created.")

def create_group(household_id, player_ids, access_token):
    print("Creating a new group with all players...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json"
    }
    create_group_url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups/createGroup"
    payload = {
        "playerIds": player_ids
    }
    print(f"Create group request: householdId={household_id}, playerIds={player_ids}")
    response = requests.post(create_group_url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Error creating group: {response.status_code} - {response.text}")
    
    try:
        group_data = response.json()
    except ValueError:
        group_data = {}

    # First, check if a group id is directly returned.
    group_id = group_data.get('id')
    if group_id:
        print(f"New group created with group ID: {group_id}")
        return group_id

    # If not, check for a controlId, indicating the command was accepted asynchronously.
    control_id = group_data.get('controlId')
    if control_id:
        print(f"Command accepted. Control ID: {control_id}. Polling for group creation...")
        group_id = poll_for_group(household_id, access_token, player_ids)
        print(f"New group created with group ID: {group_id}")
        return group_id

    raise Exception("No group ID or control ID returned in response.")

# Usage:
refresh_token_value = "pWPbYeKxsAsQQGemUiAzuTTxltXOisfu"
client_id = "1b66f808-68aa-47db-92dd-13ee474757ba"
client_secret = "61510ebb-aad5-4691-9efa-05c81260df92"

# Hardcoded list of all 8 player IDs
player_ids = [
    "RINCON_C4387580DC4101400",  # RIGHT_POLE_03
    "RINCON_C438755B516401400",  # RIGHT_POLE_01
    "RINCON_347E5C0E7E1601400",  # LEFT_POLE_01
    "RINCON_C438758DAF5201400",  # RIGHT_POLE_02
    "RINCON_804AF2A48D2F01400",  # BATHROOM_DOORS
    "RINCON_C4387580DDA001400",  # LEFT_POLE_03
    "RINCON_C4387557F99B01400",  # LEFT_POLE_02
    "RINCON_C43875560E2801400"   # CENTER_POLE
]

try:
    access_token = refresh_token(refresh_token_value, client_id, client_secret)
    household_id = get_household_id(access_token)
    group_id = create_group(household_id, player_ids, access_token)
    print("Group creation successful. Group ID:", group_id)
except Exception as e:
    print("An error occurred:")
    print(e)