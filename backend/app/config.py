from pydantic_settings import BaseSettings
from pydantic import Field
import os


class Settings(BaseSettings):
    # Sonos API Credentials - load from env vars with explicit names
    sonos_client_id: str = Field(
        default="1b66f808-68aa-47db-92dd-13ee474757ba",
        validation_alias="SONOS_CLIENT_ID"
    )
    sonos_client_secret: str = Field(
        default="61510ebb-aad5-4691-9efa-05c81260df92",
        validation_alias="SONOS_CLIENT_SECRET"
    )
    sonos_refresh_token: str = Field(
        default="pWPbYeKxsAsQQGemUiAzuTTxltXOisfu",
        validation_alias="SONOS_REFRESH_TOKEN"
    )

    # API Settings
    api_secret_key: str = Field(
        default="sonos-cloud-secret-key-change-in-production",
        validation_alias="API_SECRET_KEY"
    )

    # Database
    database_url: str = Field(
        default="sqlite:///./sonos_cloud.db",
        validation_alias="DATABASE_URL"
    )

    # Timezone
    timezone: str = Field(
        default="America/New_York",
        validation_alias="TIMEZONE"
    )

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


# Create settings instance - no caching to ensure env vars are always read
_settings = None

def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
