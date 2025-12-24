from fastapi import APIRouter, HTTPException
from typing import Optional
from ..database import database, schedule_slots
from ..models import ScheduleSlot, ScheduleSlotCreate, ScheduleSlotUpdate, DaySchedule
from ..services.scheduler_service import scheduler_service

router = APIRouter(prefix="/schedule", tags=["schedule"])

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


@router.get("", response_model=dict)
async def get_full_schedule():
    """Get the complete weekly schedule"""
    query = schedule_slots.select().order_by(schedule_slots.c.time)
    rows = await database.fetch_all(query)

    schedule = {day: [] for day in DAYS}
    for row in rows:
        day = row["day_of_week"].lower()
        if day in schedule:
            schedule[day].append(ScheduleSlot(**dict(row)))

    return schedule


@router.get("/{day}", response_model=DaySchedule)
async def get_day_schedule(day: str):
    """Get schedule for a specific day"""
    day = day.lower()
    if day not in DAYS:
        raise HTTPException(status_code=400, detail=f"Invalid day. Must be one of: {DAYS}")

    query = schedule_slots.select().where(
        schedule_slots.c.day_of_week == day
    ).order_by(schedule_slots.c.time)
    rows = await database.fetch_all(query)

    return DaySchedule(
        day=day,
        slots=[ScheduleSlot(**dict(row)) for row in rows]
    )


@router.post("/{day}", response_model=ScheduleSlot)
async def add_schedule_slot(day: str, slot: ScheduleSlotCreate):
    """Add a new time slot to a day's schedule"""
    day = day.lower()
    if day not in DAYS:
        raise HTTPException(status_code=400, detail=f"Invalid day. Must be one of: {DAYS}")

    # Check for existing slot at same time
    existing = await database.fetch_one(
        schedule_slots.select().where(
            (schedule_slots.c.day_of_week == day) &
            (schedule_slots.c.time == slot.time)
        )
    )
    if existing:
        raise HTTPException(status_code=400, detail=f"Slot already exists at {slot.time} on {day}")

    query = schedule_slots.insert().values(
        day_of_week=day,
        time=slot.time,
        program_name=slot.program_name,
        block_type=slot.block_type,
        is_active=slot.is_active
    )
    last_id = await database.execute(query)

    # Reload scheduler
    await scheduler_service.load_schedule_from_db()

    return ScheduleSlot(
        id=last_id,
        day_of_week=day,
        time=slot.time,
        program_name=slot.program_name,
        block_type=slot.block_type,
        is_active=slot.is_active
    )


@router.put("/{day}/{slot_id}", response_model=ScheduleSlot)
async def update_schedule_slot(day: str, slot_id: int, slot: ScheduleSlotUpdate):
    """Update an existing time slot"""
    day = day.lower()

    # Check slot exists
    existing = await database.fetch_one(
        schedule_slots.select().where(schedule_slots.c.id == slot_id)
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Slot not found")

    # Build update values
    update_data = {}
    if slot.time is not None:
        update_data["time"] = slot.time
    if slot.program_name is not None:
        update_data["program_name"] = slot.program_name
    if slot.block_type is not None:
        update_data["block_type"] = slot.block_type
    if slot.is_active is not None:
        update_data["is_active"] = slot.is_active

    if update_data:
        query = schedule_slots.update().where(
            schedule_slots.c.id == slot_id
        ).values(**update_data)
        await database.execute(query)

    # Reload scheduler
    await scheduler_service.load_schedule_from_db()

    # Fetch updated record
    updated = await database.fetch_one(
        schedule_slots.select().where(schedule_slots.c.id == slot_id)
    )
    return ScheduleSlot(**dict(updated))


@router.delete("/{day}/{slot_id}")
async def delete_schedule_slot(day: str, slot_id: int):
    """Delete a time slot"""
    existing = await database.fetch_one(
        schedule_slots.select().where(schedule_slots.c.id == slot_id)
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Slot not found")

    query = schedule_slots.delete().where(schedule_slots.c.id == slot_id)
    await database.execute(query)

    # Reload scheduler
    await scheduler_service.load_schedule_from_db()

    return {"message": "Slot deleted successfully"}


@router.post("/reset")
async def reset_schedule():
    """Reset schedule to default (from original scheduler.py)"""
    # This will be populated during initialization
    from ..data.default_schedule import DEFAULT_BLOCKS

    # Clear existing schedule
    await database.execute(schedule_slots.delete())

    # Insert default schedule
    for day, blocks in DEFAULT_BLOCKS.items():
        for block_name, rows in blocks.items():
            for time_str, program_name in rows:
                query = schedule_slots.insert().values(
                    day_of_week=day,
                    time=time_str,
                    program_name=program_name,
                    block_type=block_name,
                    is_active=True
                )
                await database.execute(query)

    # Reload scheduler
    await scheduler_service.load_schedule_from_db()

    return {"message": "Schedule reset to default"}


@router.post("/reload")
async def reload_schedule():
    """Reload schedule from database into scheduler"""
    job_count = await scheduler_service.load_schedule_from_db()
    return {"message": f"Reloaded {job_count} jobs"}
