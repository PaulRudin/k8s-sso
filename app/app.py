from aiohttp import web

from settings import Settings
from commento import setup_commento
import views


def setup_routes(app):
    app.router.add_routes([
        web.get('/commento', views.commento_handler),
        web.get('/test', views.test_hander)
    ])


def make_app():
    app = web.Application()
    app['settings'] = Settings()
    setup_routes(app)
    setup_commento(app)
    return app


def main():
    app = make_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
