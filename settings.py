import os

from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr

load_dotenv()


class SiteSettings(BaseSettings):
    api_key_hotels: SecretStr = os.getenv('SITE_API_HOTELS', None)
    host_api_hotels: SecretStr = os.getenv('HOST_API_HOTELS', None)
    token: SecretStr = os.getenv('TOKEN_API', None)
    api_key_trans: SecretStr = os.getenv('SITE_API_TRANS', None)
    host_api_trans: SecretStr = os.getenv('HOST_API_TRANS', None)

