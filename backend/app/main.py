from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import get_settings
from .database import database, create_tables, schedule_slots
from .routes import (
    schedule_router,
    playback_router,
    speakers_router,
    favorites_router,
    programs_router,
    system_router,
)
from .services.scheduler_service import scheduler_service
from .data.default_schedule import DEFAULT_BLOCKS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()


async def initialize_default_schedule():
    """Initialize database with default schedule if empty"""
    # Check if schedule is empty
    count = await database.fetch_val("SELECT COUNT(*) FROM schedule_slots")
    if count == 0:
        logger.info("Initializing default schedule...")
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
        logger.info("Default schedule initialized")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown"""
    # Startup
    logger.info("Starting Sonos Cloud Backend...")

    # Create database tables
    create_tables()
    logger.info("Database tables created")

    # Connect to database
    await database.connect()
    logger.info("Database connected")

    # Initialize default schedule if empty
    await initialize_default_schedule()

    # Start scheduler and load schedule
    scheduler_service.start()
    await scheduler_service.load_schedule_from_db()
    logger.info("Scheduler started and loaded")

    yield

    # Shutdown
    logger.info("Shutting down Sonos Cloud Backend...")
    scheduler_service.stop()
    await database.disconnect()
    logger.info("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Sonos Cloud Control API",
    description="API for controlling Sonos speakers and managing audio schedules",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(schedule_router, prefix="/api/v1")
app.include_router(playback_router, prefix="/api/v1")
app.include_router(speakers_router, prefix="/api/v1")
app.include_router(favorites_router, prefix="/api/v1")
app.include_router(programs_router, prefix="/api/v1")
app.include_router(system_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Sonos Cloud Control API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/system/health"
    }


@app.get("/api/v1")
async def api_root():
    """API root - list available endpoints"""
    return {
        "endpoints": {
            "schedule": "/api/v1/schedule",
            "playback": "/api/v1/playback",
            "speakers": "/api/v1/speakers",
            "favorites": "/api/v1/favorites",
            "programs": "/api/v1/programs",
            "system": "/api/v1/system"
        }
    }
