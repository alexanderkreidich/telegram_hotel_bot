import os

from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr

load_dotenv()


class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv('SITE_API', None)
    host_api: SecretStr = os.getenv('HOST_API', None)
    token: SecretStr = os.getenv('TOKEN_API', None)

