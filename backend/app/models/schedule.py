from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScheduleSlotBase(BaseModel):
    day_of_week: str
    time: str  # HH:MM format
    program_name: str
    block_type: str  # AM, DAY, PM_FIRE
    is_active: bool = True


class ScheduleSlotCreate(ScheduleSlotBase):
    pass


class ScheduleSlotUpdate(BaseModel):
    time: Optional[str] = None
    program_name: Optional[str] = None
    block_type: Optional[str] = None
    is_active: Optional[bool] = None


class ScheduleSlot(ScheduleSlotBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DaySchedule(BaseModel):
    day: str
    slots: list[ScheduleSlot]


class WeeklySchedule(BaseModel):
    monday: list[ScheduleSlot]
    tuesday: list[ScheduleSlot]
    wednesday: list[ScheduleSlot]
    thursday: list[ScheduleSlot]
    friday: list[ScheduleSlot]
    saturday: list[ScheduleSlot]
    sunday: list[ScheduleSlot]
