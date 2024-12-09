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

def get_favorites(household_id, access_token):
    print("Retrieving favorites...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    favorites_url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/favorites"
    favorites_response = requests.get(favorites_url, headers=headers)
    if favorites_response.status_code != 200:
        raise Exception(f"Error retrieving favorites: {favorites_response.text}")

    favorites_data = favorites_response.json()
    favorites = favorites_data.get("items", [])
    print(f"Retrieved {len(favorites)} favorites.")
    for i, favorite in enumerate(favorites, start=1):
        print(f"{i}. ID: {favorite['id']}, Name: {favorite['name']}, Type: {favorite.get('type', 'Unknown')}")
    return favorites

# Usage
refresh_token_value = "pWPbYeKxsAsQQGemUiAzuTTxltXOisfu"
client_id = "1b66f808-68aa-47db-92dd-13ee474757ba"
client_secret = "61510ebb-aad5-4691-9efa-05c81260df92"

try:
    access_token = refresh_token(refresh_token_value, client_id, client_secret)
    household_id = get_household_id(access_token)
    favorites = get_favorites(household_id, access_token)
    print("Favorites retrieved successfully.")
except Exception as e:
    print("An error occurred:", str(e))