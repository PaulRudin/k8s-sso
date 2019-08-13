from pydantic import BaseSettings


class Settings(BaseSettings):

    class Config:
        env_prefix = 'K8S_SSO_'

    client_id = ''

    client_secret = ''

    client_base_url = ''

    session_cookie_secret = b''
