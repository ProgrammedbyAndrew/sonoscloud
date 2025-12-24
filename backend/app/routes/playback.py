from fastapi import APIRouter, HTTPException
from ..models import PlaybackStatus, PlaybackCommand, VolumeCommand, PlayFavoriteCommand
from ..services.sonos_api import sonos_api
from ..services.scheduler_service import scheduler_service

router = APIRouter(prefix="/playback", tags=["playback"])


@router.get("/status", response_model=PlaybackStatus)
async def get_playback_status():
    """Get current playback status"""
    try:
        # Get current group
        group_id = await sonos_api.ensure_group()

        # Get playback info
        status = await sonos_api.get_playback_status(group_id)

        # Get next scheduled item
        next_job = scheduler_service.get_next_job()

        is_playing = status.get("playbackState") == "PLAYBACK_STATE_PLAYING"

        return PlaybackStatus(
            is_playing=is_playing,
            current_program=scheduler_service.current_program,
            current_volume=None,  # Would need to query individual speakers
            group_id=group_id,
            next_scheduled=next_job["program"] if next_job else None,
            next_scheduled_time=f"{next_job['day']} {next_job['time']}" if next_job else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/play")
async def play(command: PlaybackCommand = None):
    """Start playback or play a specific program"""
    try:
        group_id = await sonos_api.ensure_group()

        if command and command.program_name:
            # Run specific program
            await scheduler_service.run_program(command.program_name)
            return {"message": f"Playing program: {command.program_name}"}

        if command and command.favorite_id:
            # Play specific favorite
            await sonos_api.load_favorite(group_id, command.favorite_id)
            await sonos_api.play(group_id)
            return {"message": f"Playing favorite: {command.favorite_id}"}

        # Just resume playback
        await sonos_api.play(group_id)
        return {"message": "Playback started"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/play-favorite")
async def play_favorite(command: PlayFavoriteCommand):
    """Play a favorite with specified volume"""
    try:
        await sonos_api.play_favorite_with_volume(
            command.favorite_id,
            command.volume or 75
        )
        return {"message": f"Playing favorite {command.favorite_id} at volume {command.volume}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pause")
async def pause():
    """Pause all playback"""
    try:
        await sonos_api.pause_all()
        return {"message": "Playback paused"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/volume")
async def set_volume(command: VolumeCommand):
    """Set master volume for all speakers"""
    try:
        if command.volume < 0 or command.volume > 100:
            raise HTTPException(status_code=400, detail="Volume must be between 0 and 100")

        await sonos_api.set_all_volumes(command.volume)
        return {"message": f"Volume set to {command.volume}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/skip")
async def skip_to_next():
    """Skip to next scheduled program (runs it immediately)"""
    try:
        next_job = scheduler_service.get_next_job()
        if not next_job:
            raise HTTPException(status_code=404, detail="No upcoming scheduled programs")

        await scheduler_service.run_program(next_job["program"])
        return {"message": f"Skipped to: {next_job['program']}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/run-program/{program_name}")
async def run_program(program_name: str):
    """Run a specific program immediately"""
    try:
        await scheduler_service.run_program(program_name)
        return {"message": f"Running program: {program_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
