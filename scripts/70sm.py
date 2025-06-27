import asyncio
import aiohttp
import base64
import certifi
import ssl
import time

ssl_context = ssl.create_default_context(cafile=certifi.where())

async def refresh_token(refresh_token_value, client_id, client_secret, session):
    print("Refreshing access token...")
    url = "https://api.sonos.com/login/v3/oauth/access"
    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token_value}
    credentials = f"{client_id}:{client_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()
    headers = {"accept": "application/json", "Authorization": f"Basic {encoded}"}
    async with session.post(url, headers=headers, data=payload, ssl=ssl_context) as resp:
        if resp.status != 200:
            raise Exception(await resp.text())
        data = await resp.json()
        return data["access_token"]

async def get_household_id(access_token, session):
    url = "https://api.ws.sonos.com/control/api/v1/households"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with session.get(url, headers=headers, ssl=ssl_context) as resp:
        data = await resp.json()
        return data["households"][0]["id"]

async def get_groups(household_id, access_token, session):
    url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with session.get(url, headers=headers, ssl=ssl_context) as resp:
        data = await resp.json()
        return data.get("groups", [])

async def find_existing_group(household_id, access_token, player_ids, session):
    groups = await get_groups(household_id, access_token, session)
    target_set = set(player_ids)
    for group in groups:
        if set(group.get("playerIds", [])) == target_set:
            return group["id"]
    return None

async def poll_for_group(household_id, access_token, player_ids, session, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        groups = await get_groups(household_id, access_token, session)
        for group in groups:
            if set(player_ids).issubset(set(group.get("playerIds", []))):
                return group["id"]
        await asyncio.sleep(2)
    raise Exception("Timed out waiting for group formation.")

async def create_group(household_id, player_ids, access_token, session):
    url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups/createGroup"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {"playerIds": player_ids}
    async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as resp:
        data = await resp.json()
        return data.get("id") or await poll_for_group(household_id, access_token, player_ids, session)

async def load_favorite_playlist(group_id, favorite_id, access_token, session):
    url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/favorites"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {"favoriteId": favorite_id}
    async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as resp:
        if resp.status != 200:
            raise Exception(await resp.text())

async def set_player_volume(player_id, volume, access_token, session):
    url = f"https://api.ws.sonos.com/control/api/v1/players/{player_id}/playerVolume"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {"volume": volume}
    async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as resp:
        if resp.status != 200:
            raise Exception(await resp.text())

async def play_group(group_id, access_token, session):
    url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/playback/play"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with session.post(url, headers=headers, ssl=ssl_context) as resp:
        if resp.status != 200:
            raise Exception(await resp.text())

async def main():
    refresh_token_value = "pWPbYeKxsAsQQGemUiAzuTTxltXOisfu"
    client_id = "1b66f808-68aa-47db-92dd-13ee474757ba"
    client_secret = "61510ebb-aad5-4691-9efa-05c81260df92"

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

    player_ids = [info["id"] for info in speakers.values()]

    announcement_volumes = {
        "BATHROOM_DOORS": 85,
        "STAGE": 85,
        "RIGHT_POLE_01": 85,
        "RIGHT_POLE_02": 85,
        "RIGHT_POLE_03": 85,
        "LEFT_POLE_01": 85,
        "LEFT_POLE_03": 85,
        "CENTER_POLE": 85
    }

    main_volumes = {
        "BATHROOM_DOORS": 70,
        "STAGE": 70,
        "RIGHT_POLE_01": 70,
        "RIGHT_POLE_02": 70,
        "RIGHT_POLE_03": 70,
        "LEFT_POLE_01": 70,
        "LEFT_POLE_03": 70,
        "CENTER_POLE": 70
    }

    async with aiohttp.ClientSession() as session:
        access_token = await refresh_token(refresh_token_value, client_id, client_secret, session)
        household_id = await get_household_id(access_token, session)

        group_id = await find_existing_group(household_id, access_token, player_ids, session)
        if not group_id:
            group_id = await create_group(household_id, player_ids, access_token, session)

        # Announcement 1
        await load_favorite_playlist(group_id, "30", access_token, session)
        await asyncio.gather(*[
            set_player_volume(info["id"], announcement_volumes[name], access_token, session)
            for name, info in speakers.items()
        ])
        await play_group(group_id, access_token, session)
        print("Announcement 1 is playing")
        await asyncio.sleep(23)

        # Announcement 2
        await load_favorite_playlist(group_id, "31", access_token, session)
        await asyncio.gather(*[
            set_player_volume(info["id"], announcement_volumes[name], access_token, session)
            for name, info in speakers.items()
        ])
        await play_group(group_id, access_token, session)
        print("Announcement 2 is playing")
        await asyncio.sleep(27)

        # Main Playlist
        await load_favorite_playlist(group_id, "36", access_token, session)
        await asyncio.gather(*[
            set_player_volume(info["id"], main_volumes[name], access_token, session)
            for name, info in speakers.items()
        ])
        await play_group(group_id, access_token, session)
        print("Main playlist is playing")

if __name__ == "__main__":
    asyncio.run(main())
