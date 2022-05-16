from pydantic import BaseSettings


class Setting(BaseSettings):
    DATABASE_URL = 'sqlite:///data.db'
    MAX_LOGIN_LENGTH = 15
    MAX_PASSWORD_LENGTH = 15
    MAX_HEADER_LENGTH = 30
    DEFAULT_POSTS_PER_PAGE = 10
    START_PAGE = 1
    FILE_LOGS_NAME = 'logs.log'
    ADMIN_FILE = 'admin'


settings = Setting()
