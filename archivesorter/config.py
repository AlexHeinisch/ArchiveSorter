from pydantic_settings import BaseSettings


class Config(BaseSettings):
    app_name: str = 'PhotoArchiveSorter'

    database_connection_string: str = 'sqlite:///database.db'
    database_echo: bool = True


settings = Config()
