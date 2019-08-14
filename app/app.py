import base64
import logging

import aiohttp
from aiohttp import web
import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from settings import Settings
import client
import views


def setup_routes(app):
    app.router.add_routes([
        web.get('/hc', views.hc),
        web.get('/oauth2/auth', views.auth_handler),
        web.get('/oauth2/start', views.signin_handler),
        web.get('/oauth2/callback', views.callback_handler),
    ])


def setup_sessions(app):
    secret_key = app['settings'].session_cookie_secret
    aiohttp_session.setup(
        app, EncryptedCookieStorage(base64.urlsafe_b64decode(secret_key))
    )


def setup_client_session(app):
    async def make_client_session(app):
        app['client_session'] = aiohttp.ClientSession()
    app.on_startup.append(make_client_session)


def make_app(log_level=logging.DEBUG):
    logging.basicConfig(level=log_level)
    app = web.Application()
    app['settings'] = Settings()
    setup_sessions(app)
    setup_client_session(app)
    setup_routes(app)
    client.setup_client(app)
    return app


def main():
    app = make_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
