import asyncio
from fastapi import APIRouter, HTTPException
from ..models import Speaker, SpeakerVolume, AllSpeakersVolume
from ..services.sonos_api import sonos_api
from ..config import get_settings

router = APIRouter(prefix="/speakers", tags=["speakers"])
settings = get_settings()


@router.get("", response_model=list[Speaker])
async def get_speakers():
    """Get all speakers with their status and live volumes"""
    try:
        # Get groups and volumes in parallel
        groups, volumes = await asyncio.gather(
            sonos_api.get_groups(),
            sonos_api.get_all_volumes()
        )

        # Build set of all grouped player IDs
        grouped_players = set()
        for group in groups:
            grouped_players.update(group.get("playerIds", []))

        speakers = []
        for name, player_id in settings.speakers.items():
            speakers.append(Speaker(
                id=player_id,
                name=name,
                is_online=player_id in grouped_players,
                is_grouped=len(grouped_players) == len(settings.speakers),
                volume=volumes.get(name)  # Live volume from Sonos
            ))

        return speakers

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{speaker_name}")
async def get_speaker(speaker_name: str):
    """Get a specific speaker by name"""
    speaker_name = speaker_name.upper()
    if speaker_name not in settings.speakers:
        raise HTTPException(status_code=404, detail=f"Speaker not found: {speaker_name}")

    player_id = settings.speakers[speaker_name]

    try:
        groups = await sonos_api.get_groups()
        grouped_players = set()
        for group in groups:
            grouped_players.update(group.get("playerIds", []))

        return Speaker(
            id=player_id,
            name=speaker_name,
            is_online=player_id in grouped_players,
            is_grouped=len(grouped_players) == len(settings.speakers),
            volume=None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/group")
async def group_all_speakers():
    """Group all speakers together"""
    try:
        group_id = await sonos_api.ensure_group()
        return {"message": "All speakers grouped", "group_id": group_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{speaker_name}/volume")
async def set_speaker_volume(speaker_name: str, volume: SpeakerVolume):
    """Set volume for a specific speaker"""
    speaker_name = speaker_name.upper()
    if speaker_name not in settings.speakers:
        raise HTTPException(status_code=404, detail=f"Speaker not found: {speaker_name}")

    if volume.volume < 0 or volume.volume > 100:
        raise HTTPException(status_code=400, detail="Volume must be between 0 and 100")

    try:
        player_id = settings.speakers[speaker_name]
        await sonos_api.set_player_volume(player_id, volume.volume)
        return {"message": f"Volume set to {volume.volume} for {speaker_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/volume/all")
async def set_all_speakers_volume(command: AllSpeakersVolume):
    """Set volume for all speakers"""
    if command.volume < 0 or command.volume > 100:
        raise HTTPException(status_code=400, detail="Volume must be between 0 and 100")

    try:
        await sonos_api.set_all_volumes(command.volume)
        return {"message": f"All speakers set to volume {command.volume}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config/layout")
async def get_speaker_layout():
    """Get speaker layout configuration for UI display"""
    # Returns the speaker positions for visual display
    return {
        "layout": [
            ["LEFT_POLE_01", "CENTER_POLE", "RIGHT_POLE_01"],
            ["LEFT_POLE_02", "STAGE", "RIGHT_POLE_02"],
            ["LEFT_POLE_03", "BATHROOM_DOORS", "RIGHT_POLE_03"]
        ],
        "speakers": settings.speakers
    }
