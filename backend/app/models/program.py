from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProgramBase(BaseModel):
    name: str
    volume: int
    program_type: str  # ad, fm, sm, parking, TIGS, adfire, fireparking, pause
    favorite_ids: Optional[str] = None  # JSON array as string
    description: Optional[str] = None


class ProgramCreate(ProgramBase):
    pass


class Program(ProgramBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProgramWithDetails(Program):
    """Program with additional runtime details"""
    is_available: bool = True
    script_exists: bool = True
