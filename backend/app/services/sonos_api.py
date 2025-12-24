import aiohttp
import base64
import ssl
import certifi
import asyncio
import time
from typing import Optional
from ..config import get_settings

settings = get_settings()

# Create SSL context using certifi's CA bundle
ssl_context = ssl.create_default_context(cafile=certifi.where())


class SonosAPI:
    """Async wrapper for Sonos Control API"""

    def __init__(self):
        self.access_token: Optional[str] = None
        self.token_expires_at: float = 0
        self.household_id: Optional[str] = None
        self.current_group_id: Optional[str] = None
        self._session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        """Close the session"""
        if self._session and not self._session.closed:
            await self._session.close()

    async def refresh_access_token(self) -> str:
        """Refresh the OAuth access token"""
        session = await self.get_session()
        url = "https://api.sonos.com/login/v3/oauth/access"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": settings.sonos_refresh_token
        }
        credentials = f"{settings.sonos_client_id}:{settings.sonos_client_secret}"
        credentials_encoded = base64.b64encode(credentials.encode()).decode()
        headers = {
            "accept": "application/json",
            "Authorization": f"Basic {credentials_encoded}"
        }

        async with session.post(url, headers=headers, data=payload, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error refreshing token: {response.status} - {text}")
            data = await response.json()
            self.access_token = data["access_token"]
            # Token typically expires in 1 hour, refresh 5 minutes early
            self.token_expires_at = time.time() + 3300
            return self.access_token

    async def ensure_valid_token(self) -> str:
        """Ensure we have a valid access token"""
        if not self.access_token or time.time() >= self.token_expires_at:
            await self.refresh_access_token()
        return self.access_token

    async def get_headers(self) -> dict:
        """Get headers with valid auth token"""
        token = await self.ensure_valid_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

    async def get_household_id(self) -> str:
        """Get the household ID"""
        if self.household_id:
            return self.household_id

        session = await self.get_session()
        headers = await self.get_headers()
        url = "https://api.ws.sonos.com/control/api/v1/households"

        async with session.get(url, headers=headers, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error getting households: {response.status} - {text}")
            data = await response.json()
            self.household_id = data["households"][0]["id"]
            return self.household_id

    async def get_groups(self) -> list[dict]:
        """Get all speaker groups"""
        session = await self.get_session()
        headers = await self.get_headers()
        household_id = await self.get_household_id()
        url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups"

        async with session.get(url, headers=headers, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error getting groups: {response.status} - {text}")
            data = await response.json()
            return data.get("groups", [])

    async def get_players(self) -> list[dict]:
        """Get all players in the household"""
        session = await self.get_session()
        headers = await self.get_headers()
        household_id = await self.get_household_id()
        url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups"

        async with session.get(url, headers=headers, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error getting players: {response.status} - {text}")
            data = await response.json()
            return data.get("players", [])

    async def find_existing_group(self, player_ids: list[str]) -> Optional[str]:
        """Find an existing group containing all specified players"""
        groups = await self.get_groups()
        target_set = set(player_ids)
        for group in groups:
            if set(group.get("playerIds", [])) == target_set:
                return group["id"]
        return None

    async def poll_for_group(self, player_ids: list[str], timeout: int = 30, interval: int = 2) -> str:
        """Poll for a group to be created"""
        start_time = time.time()
        target_set = set(player_ids)
        while time.time() - start_time < timeout:
            groups = await self.get_groups()
            for group in groups:
                if target_set.issubset(set(group.get("playerIds", []))):
                    return group["id"]
            await asyncio.sleep(interval)
        raise Exception("Timed out waiting for group creation")

    async def create_group(self, player_ids: list[str]) -> str:
        """Create a new group with specified players"""
        session = await self.get_session()
        headers = await self.get_headers()
        headers["accept"] = "application/json"
        household_id = await self.get_household_id()
        url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/groups/createGroup"
        payload = {"playerIds": player_ids}

        async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error creating group: {response.status} - {text}")
            try:
                data = await response.json()
            except Exception:
                data = {}

        group_id = data.get("id")
        if group_id:
            self.current_group_id = group_id
            return group_id

        # Poll for group creation if no immediate ID returned
        control_id = data.get("controlId")
        if control_id:
            group_id = await self.poll_for_group(player_ids)
            self.current_group_id = group_id
            return group_id

        # Wait and poll
        await asyncio.sleep(3)
        group_id = await self.poll_for_group(player_ids)
        self.current_group_id = group_id
        return group_id

    async def ensure_group(self) -> str:
        """Ensure all speakers are grouped and return the group ID"""
        player_ids = list(settings.speakers.values())

        # Check for existing group
        existing = await self.find_existing_group(player_ids)
        if existing:
            self.current_group_id = existing
            return existing

        # Create new group
        return await self.create_group(player_ids)

    async def get_favorites(self) -> list[dict]:
        """Get all favorites/playlists"""
        session = await self.get_session()
        headers = await self.get_headers()
        household_id = await self.get_household_id()
        url = f"https://api.ws.sonos.com/control/api/v1/households/{household_id}/favorites"

        async with session.get(url, headers=headers, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error getting favorites: {response.status} - {text}")
            data = await response.json()
            return data.get("items", [])

    async def load_favorite(self, group_id: str, favorite_id: str) -> bool:
        """Load a favorite playlist into a group"""
        session = await self.get_session()
        headers = await self.get_headers()
        url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/favorites"
        payload = {"favoriteId": favorite_id}

        async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error loading favorite: {response.status} - {text}")
            return True

    async def set_player_volume(self, player_id: str, volume: int) -> bool:
        """Set volume for a specific player"""
        session = await self.get_session()
        headers = await self.get_headers()
        url = f"https://api.ws.sonos.com/control/api/v1/players/{player_id}/playerVolume"
        payload = {"volume": volume}

        async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error setting volume: {response.status} - {text}")
            return True

    async def set_all_volumes(self, volume: int) -> bool:
        """Set volume for all speakers"""
        tasks = [
            self.set_player_volume(player_id, volume)
            for player_id in settings.speakers.values()
        ]
        await asyncio.gather(*tasks)
        return True

    async def set_group_volume(self, group_id: str, volume: int) -> bool:
        """Set volume for a group"""
        session = await self.get_session()
        headers = await self.get_headers()
        url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/groupVolume"
        payload = {"volume": volume}

        async with session.post(url, headers=headers, json=payload, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error setting group volume: {response.status} - {text}")
            return True

    async def play(self, group_id: str) -> bool:
        """Start playback for a group"""
        session = await self.get_session()
        headers = await self.get_headers()
        url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/playback/play"

        async with session.post(url, headers=headers, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Playback error: {response.status} - {text}")
            return True

    async def pause(self, group_id: str) -> bool:
        """Pause playback for a group"""
        session = await self.get_session()
        headers = await self.get_headers()
        url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/playback/pause"

        async with session.post(url, headers=headers, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Pause error: {response.status} - {text}")
            return True

    async def get_playback_status(self, group_id: str) -> dict:
        """Get playback status for a group"""
        session = await self.get_session()
        headers = await self.get_headers()
        url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/playback"

        async with session.get(url, headers=headers, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error getting playback status: {response.status} - {text}")
            return await response.json()

    async def get_playback_metadata(self, group_id: str) -> dict:
        """Get current track metadata for a group"""
        session = await self.get_session()
        headers = await self.get_headers()
        url = f"https://api.ws.sonos.com/control/api/v1/groups/{group_id}/playbackMetadata"

        async with session.get(url, headers=headers, ssl=ssl_context) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Error getting metadata: {response.status} - {text}")
            return await response.json()

    async def play_favorite_with_volume(self, favorite_id: str, volume: int) -> bool:
        """Load a favorite and play it with specified volume"""
        group_id = await self.ensure_group()
        await self.load_favorite(group_id, favorite_id)
        await self.set_all_volumes(volume)
        await self.play(group_id)
        return True

    async def pause_all(self) -> bool:
        """Pause all playback"""
        groups = await self.get_groups()
        for group in groups:
            try:
                await self.pause(group["id"])
            except Exception:
                pass  # Ignore errors if group isn't playing
        return True


# Global instance
sonos_api = SonosAPI()
