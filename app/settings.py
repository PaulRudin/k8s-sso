from pydantic import BaseSettings


class Settings(BaseSettings):
    commento_secret = b''
    commento_url = 'https://comments.xamaral.com'

    class Config:
        env_prefix = 'SSO_HELPER'
