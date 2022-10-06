from pydantic import BaseSettings


class Settings(BaseSettings):
    origin_0: str
    environment: str

    api_data_url: str
    api_auth_url: str
    app_url: str
    connection_uri: str
    api_key: str
    cookie_secure: bool
    cookie_domain: str
    cookie_same_site: str

    google_client_id: str
    google_client_secret: str

    email_verification: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
