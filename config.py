from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "ContentForge AI Starter"
    openai_api_key: str | None = None
    openai_model: str | None = None
    pexels_api_key: str | None = None
    pixabay_api_key: str | None = None
    elevenlabs_api_key: str | None = None
    elevenlabs_voice_id: str | None = None
    shotstack_api_key: str | None = None
    shotstack_stage_url: str = "https://api.shotstack.io/stage"
    sqlite_path: str = "./app/data/contentforge.sqlite3"
    feedback_log_path: str = "./app/data/feedback.jsonl"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
