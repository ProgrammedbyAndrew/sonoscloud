import databases
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from .config import get_settings

settings = get_settings()

# Database URL - convert sqlite:/// to sqlite+aiosqlite:/// for async
DATABASE_URL = settings.database_url
if DATABASE_URL.startswith("sqlite:///"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
else:
    ASYNC_DATABASE_URL = DATABASE_URL

database = databases.Database(ASYNC_DATABASE_URL)
metadata = MetaData()

# Schedule Slots Table
schedule_slots = sqlalchemy.Table(
    "schedule_slots",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("day_of_week", sqlalchemy.String(20), nullable=False),
    sqlalchemy.Column("time", sqlalchemy.String(5), nullable=False),
    sqlalchemy.Column("program_name", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("block_type", sqlalchemy.String(20), nullable=False),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=sqlalchemy.func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()),
)

# Programs Table
programs = sqlalchemy.Table(
    "programs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(50), unique=True, nullable=False),
    sqlalchemy.Column("volume", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("program_type", sqlalchemy.String(20), nullable=False),
    sqlalchemy.Column("favorite_ids", sqlalchemy.String(100)),  # JSON array as string
    sqlalchemy.Column("description", sqlalchemy.String(255)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=sqlalchemy.func.now()),
)

# Execution Logs Table
execution_logs = sqlalchemy.Table(
    "execution_logs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("program_name", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("executed_at", sqlalchemy.DateTime, default=sqlalchemy.func.now()),
    sqlalchemy.Column("status", sqlalchemy.String(20), nullable=False),
    sqlalchemy.Column("error_message", sqlalchemy.String(500)),
)

# Settings Table
app_settings = sqlalchemy.Table(
    "app_settings",
    metadata,
    sqlalchemy.Column("key", sqlalchemy.String(50), primary_key=True),
    sqlalchemy.Column("value", sqlalchemy.String(500), nullable=False),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()),
)

# Create engine for table creation
sync_engine = create_engine(DATABASE_URL.replace("+aiosqlite", ""))


def create_tables():
    """Create all tables in the database"""
    metadata.create_all(sync_engine)


async def connect_db():
    """Connect to database"""
    await database.connect()


async def disconnect_db():
    """Disconnect from database"""
    await database.disconnect()
