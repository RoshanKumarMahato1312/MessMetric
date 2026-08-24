from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str ="HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    COLLEGE_EMAIL_DOMAIN: str 

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str

    ESCALATION_THRESHOLD: float = 0.48
    ESCALATION_CONSECUTIVE_DAYS: int = 3

    class Config:
        env_file = ".env" 

settings = Settings()