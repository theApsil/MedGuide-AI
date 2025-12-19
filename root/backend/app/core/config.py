from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "MedGuide AI"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False


def load_settings() -> Settings:
    return Settings(
        debug=os.getenv("DEBUG", "false").lower() == "true"
    )