from fastapi import APIRouter, HTTPException
from ..services.sonos_api import sonos_api
from ..models.playback import PlayFavoriteCommand

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("")
async def get_favorites():
    """Get all Sonos favorites/playlists"""
    try:
        favorites = await sonos_api.get_favorites()
        return {"favorites": favorites}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{favorite_id}/play")
async def play_favorite(favorite_id: str, volume: int = 75):
    """Play a specific favorite"""
    try:
        if volume < 0 or volume > 100:
            raise HTTPException(status_code=400, detail="Volume must be between 0 and 100")

        await sonos_api.play_favorite_with_volume(favorite_id, volume)
        return {"message": f"Playing favorite {favorite_id} at volume {volume}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/known")
async def get_known_favorites():
    """Get list of known/commonly used favorites with descriptions"""
    # Based on the existing scripts, these are the known favorite IDs
    known = [
        {"id": "28", "name": "Visitors Flea Market Commercial (English)", "type": "announcement"},
        {"id": "29", "name": "Visitors Flea Market Commercial (Spanish)", "type": "announcement"},
        {"id": "30", "name": "Parking Announcement", "type": "announcement"},
        {"id": "31", "name": "TIGS Program", "type": "announcement"},
        {"id": "33", "name": "Main Music Playlist", "type": "music"},
        {"id": "34", "name": "Fire Show Music", "type": "music"},
        {"id": "35", "name": "Secondary Announcement", "type": "announcement"},
    ]
    return {"known_favorites": known}
