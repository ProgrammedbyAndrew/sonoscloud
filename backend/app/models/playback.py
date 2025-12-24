from pydantic import BaseModel
from typing import Optional


class PlaybackStatus(BaseModel):
    is_playing: bool
    current_program: Optional[str] = None
    current_volume: Optional[int] = None
    group_id: Optional[str] = None
    next_scheduled: Optional[str] = None
    next_scheduled_time: Optional[str] = None


class PlaybackCommand(BaseModel):
    program_name: Optional[str] = None
    favorite_id: Optional[str] = None


class VolumeCommand(BaseModel):
    volume: int  # 0-100


class PlayFavoriteCommand(BaseModel):
    favorite_id: str
    volume: Optional[int] = 75
