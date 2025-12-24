from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # Sonos API Credentials
    sonos_client_id: str = "1b66f808-68aa-47db-92dd-13ee474757ba"
    sonos_client_secret: str = "61510ebb-aad5-4691-9efa-05c81260df92"
    sonos_refresh_token: str = "pWPbYeKxsAsQQGemUiAzuTTxltXOisfu"

    # API Settings
    api_secret_key: str = "sonos-cloud-secret-key-change-in-production"

    # Database
    database_url: str = "sqlite:///./sonos_cloud.db"

    # Timezone
    timezone: str = "America/New_York"

    # CORS Origins (for frontend)
    cors_origins: list[str] = ["*"]

    # Speaker Configuration
    speakers: dict = {
        "BATHROOM_DOORS": "RINCON_804AF2A48D2F01400",
        "STAGE": "RINCON_804AF2AB699401400",
        "RIGHT_POLE_01": "RINCON_804AF2A52DDC01400",
        "RIGHT_POLE_02": "RINCON_804AF2A52D7901400",
        "RIGHT_POLE_03": "RINCON_C4387580DC4101400",
        "LEFT_POLE_01": "RINCON_347E5C0E7E1601400",
        "LEFT_POLE_02": "RINCON_C4387557F99B01400",
        "LEFT_POLE_03": "RINCON_C4387580DDA001400",
        "CENTER_POLE": "RINCON_C43875560E2801400"
    }

    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
