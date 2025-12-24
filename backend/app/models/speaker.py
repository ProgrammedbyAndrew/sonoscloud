from pydantic import BaseModel
from typing import Optional


class Speaker(BaseModel):
    id: str
    name: str
    is_online: bool = True
    is_grouped: bool = False
    volume: Optional[int] = None


class SpeakerVolume(BaseModel):
    speaker_id: str
    volume: int  # 0-100


class SpeakerGroup(BaseModel):
    group_id: str
    player_ids: list[str]
    coordinator_id: Optional[str] = None


class AllSpeakersVolume(BaseModel):
    volume: int  # 0-100 - applies to all speakers
