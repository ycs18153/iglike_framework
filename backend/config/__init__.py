from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "IG LIKE"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings():
    DB_URL: str = 'mongodb+srv://andy:acdwsx321@groupmagt.cgjzv3a.mongodb.net/?retryWrites=true&w=majority'
    DB_NAME: str = 'iglike_auth'


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
