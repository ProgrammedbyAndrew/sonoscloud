from fastapi import APIRouter, HTTPException
from pathlib import Path
from ..database import database, programs
from ..models import Program, ProgramCreate

router = APIRouter(prefix="/programs", tags=["programs"])

# Scripts directory path
SCRIPTS_DIR = Path(__file__).parent.parent.parent.parent / "scripts"


@router.get("")
async def get_programs():
    """Get all available programs"""
    # First get from database
    query = programs.select()
    db_programs = await database.fetch_all(query)

    # Also scan scripts directory for available scripts
    available_scripts = []
    if SCRIPTS_DIR.exists():
        for script in SCRIPTS_DIR.glob("*.py"):
            name = script.name
            if name != "__init__.py":
                # Parse program info from name
                volume = 75
                prog_type = "unknown"

                name_no_ext = name.replace(".py", "")
                digits = ""
                for char in name_no_ext:
                    if char.isdigit():
                        digits += char
                    else:
                        break

                if digits:
                    volume = int(digits)
                    prog_type = name_no_ext[len(digits):]
                else:
                    prog_type = name_no_ext

                available_scripts.append({
                    "name": name,
                    "volume": volume,
                    "program_type": prog_type,
                    "script_exists": True
                })

    return {
        "programs": [dict(p) for p in db_programs],
        "available_scripts": available_scripts
    }


@router.get("/types")
async def get_program_types():
    """Get all program types with descriptions"""
    return {
        "types": [
            {"type": "ad", "name": "Advertisement", "description": "Commercial announcements"},
            {"type": "fm", "name": "Music (FM)", "description": "Main music programming"},
            {"type": "sm", "name": "Sustained Music", "description": "Background music"},
            {"type": "parking", "name": "Parking", "description": "Parking announcements"},
            {"type": "TIGS", "name": "TIGS", "description": "Special TIGS programs"},
            {"type": "adfire", "name": "Fire Ad", "description": "Fire show advertisements"},
            {"type": "fireparking", "name": "Fire Parking", "description": "Fire show parking announcements"},
            {"type": "pause", "name": "Pause", "description": "Stop all playback"}
        ]
    }


@router.get("/by-type/{program_type}")
async def get_programs_by_type(program_type: str):
    """Get all programs of a specific type"""
    available_scripts = []
    if SCRIPTS_DIR.exists():
        for script in SCRIPTS_DIR.glob("*.py"):
            name = script.name
            name_no_ext = name.replace(".py", "")

            # Extract type
            digits = ""
            for char in name_no_ext:
                if char.isdigit():
                    digits += char
                else:
                    break

            script_type = name_no_ext[len(digits):] if digits else name_no_ext

            if script_type.lower() == program_type.lower():
                volume = int(digits) if digits else 75
                available_scripts.append({
                    "name": name,
                    "volume": volume,
                    "program_type": script_type
                })

    return {"programs": available_scripts}


@router.get("/volumes")
async def get_volume_presets():
    """Get available volume presets"""
    return {
        "presets": [50, 65, 70, 75, 80, 85, 90, 95],
        "descriptions": {
            "50": "Quiet - Late night",
            "65": "Low - Background",
            "70": "Medium-Low",
            "75": "Medium - Default",
            "80": "Medium-High",
            "85": "High - Announcements",
            "90": "Very High - Peak times",
            "95": "Maximum"
        }
    }


@router.post("")
async def create_program(program: ProgramCreate):
    """Create a new program entry"""
    # Check if exists
    existing = await database.fetch_one(
        programs.select().where(programs.c.name == program.name)
    )
    if existing:
        raise HTTPException(status_code=400, detail="Program already exists")

    query = programs.insert().values(
        name=program.name,
        volume=program.volume,
        program_type=program.program_type,
        favorite_ids=program.favorite_ids,
        description=program.description
    )
    last_id = await database.execute(query)

    return Program(
        id=last_id,
        name=program.name,
        volume=program.volume,
        program_type=program.program_type,
        favorite_ids=program.favorite_ids,
        description=program.description
    )
