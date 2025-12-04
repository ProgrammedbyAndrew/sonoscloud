import asyncio
import aiohttp
import base64
import certifi
import ssl
import time

# Create an SSL context using certifi's CA bundle.
ssl_context = ssl.create_default_context(cafile=certifi.where())

# ----------------- AUTH & API UTILS -----------------

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
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.ws.sonos.com/control/api/v1/households"
    async with session.get(url, headers=headers, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Error getting households: {response.status} - {text}")
        data = await response.json()
        household_id = data['households'][0]['id']
        print(f"Household ID retrieved: {household_id}")
        return household_id
async def get_groups(household_id, access_token, session):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups"
    async with session.get(url, headers=headers, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Error getting groups: {response.status} - {text}")
        data = await response.json()
        return data.get('groups', [])

async def find_existing_group(household_id, access_token, player_ids, session):
    target_set = set(player_ids)
    groups = await get_groups(household_id, access_token, session)
    for group in groups:
        if set(group.get('playerIds', [])) == target_set:
            print(f"Found existing group: {group['id']}")
            return group['id']
    return None

async def poll_for_group(household_id, access_token, player_ids, session, timeout=30, interval=2):
    target_set = set(player_ids)
    start_time = time.time()
    while time.time() - start_time < timeout:
        groups = await get_groups(household_id, access_token, session)
        for group in groups:
            if target_set.issubset(set(group.get('playerIds', []))):
                return group['id']
        await asyncio.sleep(interval)
    raise Exception("Timed out waiting for group creation.")

async def create_group(household_id, player_ids, access_token, session):
    print("Creating group...")
    headers = {"Authorization": f"Bearer {access_token}", "accept": "application/json"}
    url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups/createGroup"
    payload = {"playerIds": player_ids}
    async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Group creation failed: {response.status} - {text}")
        try:
            data = await response.json()
        except Exception:
            data = {}
    group_id = data.get('id') or data.get('controlId')
    if not group_id:
        await asyncio.sleep(3)
        return await poll_for_group(household_id, access_token, player_ids, session)
    if 'controlId' in data:
        return await poll_for_group(household_id, access_token, player_ids, session)
    return group_id
async def load_favorite_playlist(group_id, favorite_id, access_token, session):
    print(f"Loading playlist ID {favorite_id}...")
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/favorites"
    payload = {"favoriteId": favorite_id}
    async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Error loading playlist: {response.status} - {text}")
    print(f"Playlist {favorite_id} loaded.")

async def set_player_volume(player_id, volume, access_token, session):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.ws.sonos.com/control/api/v1/players/{player_id}/playerVolume"
    payload = {"volume": volume}
    async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Volume error {player_id}: {response.status} - {text}")
    print(f"Volume set to {volume} for {player_id}")

async def play_group(group_id, access_token, session):
    print(f"Starting playback for group {group_id}...")
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/playback/play"
    async with session.post(url, headers=headers, ssl=ssl_context) as response:
        if response.status != 200:
            text = await response.text()
            raise Exception(f"Playback error: {response.status} - {text}")
    print("Playback started.")

# ----------------- MAIN EXECUTION -----------------

async def main():
    refresh_token_value = "pWPbYeKxsAsQQGemUiAzuTTxltXOisfu"
    client_id = "1b66f808-68aa-47db-92dd-13ee474757ba"
    client_secret = "61510ebb-aad5-4691-9efa-05c81260df92"

    player_ids = [
        "RINCON_804AF2A48D2F01400",  # BATHROOM_DOORS
        "RINCON_804AF2AB699401400",  # STAGE
        "RINCON_804AF2A52DDC01400",  # RIGHT_POLE_01
        "RINCON_804AF2A52D7901400",  # RIGHT_POLE_02
        "RINCON_C4387580DC4101400",  # RIGHT_POLE_03
        "RINCON_347E5C0E7E1601400",  # LEFT_POLE_01
        "RINCON_C4387557F99B01400",  # LEFT_POLE_02
        "RINCON_C4387580DDA001400",  # LEFT_POLE_03
        "RINCON_C43875560E2801400"   # CENTER_POLE
    ]

    speakers = {
        "BATHROOM_DOORS": "RINCON_804AF2A48D2F01400",
        "STAGE": "RINCON_804AF2AB699401400",
        "RIGHT_POLE_01": "RINCON_804AF2A52DDC01400",
        "RIGHT_POLE_02": "RINCON_804AF2A52D7901400",
        "RIGHT_POLE_03": "RINCON_C4387580DC4101400",
        "LEFT_POLE_01": "RINCON_347E5C0E7E1601400",
        "LEFT_POLE_02": "RINCON_C4387557F99B01400",
        "LEFT_POLE_03": "RINCON_C4387580DDA001400",
        "CENTER_POLE": "RINCON_C43875560E2801400"
    }

    announcement_volumes = {
        "BATHROOM_DOORS": 85,
        "STAGE": 85,
        "RIGHT_POLE_01": 85,
        "RIGHT_POLE_02": 85,
        "RIGHT_POLE_03": 85,
        "LEFT_POLE_01": 85,
        "LEFT_POLE_02": 85,
        "LEFT_POLE_03": 85,
        "CENTER_POLE": 85
    }

    main_volumes = {
        "BATHROOM_DOORS": 75,
        "STAGE": 75,
        "RIGHT_POLE_01": 75,
        "RIGHT_POLE_02": 75,
        "RIGHT_POLE_03": 75,
        "LEFT_POLE_01": 75,
        "LEFT_POLE_02": 75,
        "LEFT_POLE_03": 75,
        "CENTER_POLE": 75
    }

    async with aiohttp.ClientSession() as session:
        token = await refresh_token(refresh_token_value, client_id, client_secret, session)
        household_id = await get_household_id(token, session)
        group_id = await find_existing_group(household_id, token, player_ids, session) or await create_group(household_id, player_ids, token, session)

        await load_favorite_playlist(group_id, "41", token, session)
        await asyncio.gather(*[set_player_volume(pid, announcement_volumes[name], token, session) for name, pid in speakers.items()])
        await play_group(group_id, token, session)
        await asyncio.sleep(17)

        await load_favorite_playlist(group_id, "44", token, session)
        await asyncio.gather(*[set_player_volume(pid, announcement_volumes[name], token, session) for name, pid in speakers.items()])
        await play_group(group_id, token, session)
        await asyncio.sleep(24)

        await load_favorite_playlist(group_id, "33", token, session)
        await asyncio.gather(*[set_player_volume(pid, main_volumes[name], token, session) for name, pid in speakers.items()])
        await play_group(group_id, token, session)

if __name__ == "__main__":
    asyncio.run(main())
