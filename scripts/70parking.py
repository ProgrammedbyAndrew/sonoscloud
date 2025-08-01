import asyncio
import aiohttp
import base64
import certifi
import ssl
import time

# Create an SSL context using certifi's CA bundle.
ssl_context = ssl.create_default_context(cafile=certifi.where())

# ----------------- ASYNC GROUPING AND PLAYBACK FUNCTIONS -----------------

async def refresh_token(refresh_token_value, client_id, client_secret, session):
    print("Refreshing access token...")
    url = "https://api.sonos.com/login/v3/oauth/access"
    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token_value}
    credentials = f"{client_id}:{client_secret}"
    credentials_encoded = base64.b64encode(credentials.encode()).decode()
    headers = {"accept": "application/json", "Authorization": f"Basic {credentials_encoded}"}
    async with session.post(url, headers=headers, data=payload, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Error refreshing token: {response.status} - {text}")
        data = await response.json()
        print("Access token refreshed.")
        return data['access_token']

async def get_household_id(access_token, session):
    print("Retrieving household ID...")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    url = "https://api.ws.sonos.com/control/api/v1/households"
    async with session.get(url, headers=headers, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Error getting households: {response.status} - {text}")
        households_data = await response.json()
        household_id = households_data['households'][0]['id']
        print(f"Household ID retrieved: {household_id}")
        return household_id

async def get_groups(household_id, access_token, session):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups"
    async with session.get(url, headers=headers, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Error getting groups: {response.status} - {text}")
        groups_data = await response.json()
        groups = groups_data.get('groups', [])
        return groups

async def find_existing_group(household_id, access_token, player_ids, session):
    groups = await get_groups(household_id, access_token, session)
    target_set = set(player_ids)
    for group in groups:
        if set(group.get('playerIds', [])) == target_set:
            print(f"Found existing group with ID: {group['id']}")
            return group['id']
    return None

async def poll_for_group(household_id, access_token, player_ids, session, timeout=30, interval=2):
    start_time = time.time()
    target_set = set(player_ids)
    while time.time() - start_time < timeout:
        groups = await get_groups(household_id, access_token, session)
        for group in groups:
            if target_set.issubset(set(group.get('playerIds', []))):
                return group['id']
        await asyncio.sleep(interval)
    raise Exception("Timed out waiting for the group to be created.")

async def create_group(household_id, player_ids, access_token, session):
    print("Creating a new group with all players...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json"
    }
    url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups/createGroup"
    payload = {"playerIds": player_ids}
    print(f"Create group request: householdId={household_id}, playerIds={player_ids}")
    async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Error creating group: {response.status} - {text}")
        try:
            group_data = await response.json()
        except Exception:
            group_data = {}
    group_id = group_data.get('id')
    if group_id:
        print(f"New group created with group ID: {group_id}")
        return group_id
    control_id = group_data.get('controlId')
    if control_id:
        print(f"Command accepted. Control ID: {control_id}. Polling for group creation...")
        group_id = await poll_for_group(household_id, access_token, player_ids, session)
        print(f"New group created with group ID: {group_id}")
        return group_id
    print("No group ID or control ID returned, waiting 3 seconds for group formation...")
    await asyncio.sleep(3)
    group_id = await poll_for_group(household_id, access_token, player_ids, session)
    print(f"New group created with group ID: {group_id}")
    return group_id

async def load_favorite_playlist(group_id, favorite_playlist_id, access_token, session):
    print(f"Loading favorite playlist with ID: {favorite_playlist_id}...")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/favorites"
    payload = {"favoriteId": favorite_playlist_id}
    async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Error loading favorite: {response.status} - {text}")
        print(f"Favorite playlist {favorite_playlist_id} loaded.")

async def set_player_volume(player_id, volume, access_token, session):
    print(f"Setting volume to {volume} for player {player_id}...")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    url = f"https://api.ws.sonos.com/control/api/v1/players/{player_id}/playerVolume"
    payload = {"volume": volume}
    async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Error setting volume for player {player_id}: {response.status} - {text}")
        print(f"Volume set to {volume} for player {player_id}")

async def play_group(group_id, access_token, session):
    print(f"Starting playback for group {group_id}...")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/playback/play"
    async with session.post(url, headers=headers, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Playback error {response.status}: {text}")
        print(f"Playback started for group {group_id}")

# ----------------- MAIN ASYNC LOGIC -----------------

async def main():
    # Credentials and player IDs for grouping
    refresh_token_value = "pWPbYeKxsAsQQGemUiAzuTTxltXOisfu"
    client_id = "1b66f808-68aa-47db-92dd-13ee474757ba"
    client_secret = "61510ebb-aad5-4691-9efa-05c81260df92"
    player_ids = [
        "RINCON_C4387580DC4101400",  # RIGHT_POLE_03
        "RINCON_804AF2A52DDC01400",  # RIGHT_POLE_01
        "RINCON_804AF2A52D7901400",  # RIGHT_POLE_02
        "RINCON_804AF2A48D2F01400",  # BATHROOM_DOORS
        "RINCON_347E5C0E7E1601400",  # LEFT_POLE_01
        "RINCON_C4387580DDA001400",  # LEFT_POLE_03
        "RINCON_C43875560E2801400",  # CENTER_POLE
        "RINCON_804AF2AB699401400"   # STAGE
    ]

    async with aiohttp.ClientSession() as session:
        access_token = await refresh_token(refresh_token_value, client_id, client_secret, session)
        household_id = await get_household_id(access_token, session)

        # Check if speakers are already grouped.
        existing_group = await find_existing_group(household_id, access_token, player_ids, session)
        if existing_group:
            group_id = existing_group
            print("Speakers are already grouped. Using group ID:", group_id)
        else:
            group_id = await create_group(household_id, player_ids, access_token, session)
            print("Group creation successful. Group ID:", group_id)

        # Define speakers (for display purposes)
        speakers = {
            "BATHROOM_DOORS": {"id": "RINCON_804AF2A48D2F01400"},
            "STAGE":          {"id": "RINCON_804AF2AB699401400"},
            "RIGHT_POLE_01":  {"id": "RINCON_804AF2A52DDC01400"},
            "RIGHT_POLE_02":  {"id": "RINCON_804AF2A52D7901400"},
            "RIGHT_POLE_03":  {"id": "RINCON_C4387580DC4101400"},
            "LEFT_POLE_01":   {"id": "RINCON_347E5C0E7E1601400"},
            "LEFT_POLE_03":   {"id": "RINCON_C4387580DDA001400"},
            "CENTER_POLE":    {"id": "RINCON_C43875560E2801400"}
        }
        print("Speakers:")
        for name, info in speakers.items():
            print(f" - {name}: ID = {info['id']}")

        # Define separate volume settings for announcements and main playlist.
        announcement_volumes = {
            "BATHROOM_DOORS": 85,
            "STAGE":          85,
            "RIGHT_POLE_01":  85,
            "RIGHT_POLE_02":  85,
            "RIGHT_POLE_03":  85,
            "LEFT_POLE_01":   85,
            "LEFT_POLE_03":   85,
            "CENTER_POLE":    85
        }

        main_volumes = {
            "BATHROOM_DOORS": 65,
            "STAGE":          65,
            "RIGHT_POLE_01":  65,
            "RIGHT_POLE_02":  65,
            "RIGHT_POLE_03":  65,
            "LEFT_POLE_01":   65,
            "LEFT_POLE_03":   65,
            "CENTER_POLE":    65
        }

 

        # 2. Second announcement (playlist "35")
        await load_favorite_playlist(group_id, "41", access_token, session)
        await asyncio.gather(*[
            set_player_volume(info["id"], announcement_volumes[name], access_token, session)
            for name, info in speakers.items()
        ])
        await play_group(group_id, access_token, session)
        print("The second announcement is playing")
        await asyncio.sleep(16)

        # 3. Main playlist (playlist "36")
        await load_favorite_playlist(group_id, "36", access_token, session)
        await asyncio.gather(*[
            set_player_volume(info["id"], main_volumes[name], access_token, session)
            for name, info in speakers.items()
        ])
        await play_group(group_id, access_token, session)
        print("The music is now playing")

if __name__ == "__main__":
    asyncio.run(main())

