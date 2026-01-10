from typing import Literal, Optional
import os

from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "MedGuide AI"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False

    # Элелем Элелем Элелем Элелем Элелем Элелем...
    qwen_api_url: Optional[str] = None
    qwen_api_key: Optional[str] = None
    rag_mode: Literal["none"] = "none"

    # Настройки хранилища
    storage_backend: Literal["fs", "sqlite"] = "fs"
    storage_path: str = "storage"


def load_settings() -> Settings:
    return Settings(
        debug=os.getenv("DEBUG", "false").lower() == "true"
    )
