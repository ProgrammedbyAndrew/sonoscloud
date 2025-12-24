from .schedule import router as schedule_router
from .playback import router as playback_router
from .speakers import router as speakers_router
from .favorites import router as favorites_router
from .programs import router as programs_router
from .system import router as system_router

__all__ = [
    "schedule_router",
    "playback_router",
    "speakers_router",
    "favorites_router",
    "programs_router",
    "system_router",
]
