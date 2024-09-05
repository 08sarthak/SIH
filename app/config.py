from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
        DATABASE_URL: str
        MONGO_INITDB_DATABASE: str
        OPENAI_API_KEY: str
        CLIENT_ORIGIN: str
        EMAIL_FROM: EmailStr

        # Existing settings
        CLIENT_ORIGIN: str

        # Cognito settings
        COGNITO_USER_POOL_ID: str
        COGNITO_REGION: str
        COGNITO_CLIENT_ID: str
        COGNITO_CLIENT_SECRET: str
        AWS_ACCESS_KEY_ID: str
        AWS_SECRET_ACCESS_KEY: str
        AZURE_ENDPOINT: str
        API_KEY: str
        API_VERSION: str

        class Config:
                env_file = './.env'

 
settings = Settings()
