from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    JWT_SECRET: str = "mysecretkey"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TTL_MIN: int = 15
    REFRESH_TTL_DAYS: int = 30
    EMAIL_SENDER: str
    EMAIL_SENDER_PASS: str
    SENDGRID_API: str


settings = Settings()
