import time

import aiohttp
from aiohttp_session import get_session
from jose import jwt
import yarl


class Client:

    id_keys = ['email', 'email_verified', 'name', 'nickname', 'picture']

    def __init__(self, client_id: str, client_secret: str, base_url: str,
                 session=None):

        if session is None:
            self.session = aiohttp.ClientSession()

        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = yarl.URL(base_url)
        self.make_urls()

    def make_urls(self):
        # Make as a much of the urls as we can. Some query parameters depend on
        # the request, so have to be added on the fly.
        self.signin_url = (self.base_url / 'authorize').with_query(
            response_type='code', client_id=self.client_id,
            scope='openid profile email'
        )
        self.token_url = self.base_url / 'oauth' / 'token'
        self.redirect_path = '/oauth2/callback'

        self.token_payload = dict(
            grant_type='authorization_code', client_id=self.client_id,
            client_secret=self.client_secret, scope='openid'
        )

    def make_original_url(self, request):
        headers = request.headers
        return yarl.URL(f'{headers["X-Forwarded-Proto"]}://{headers["X-Forwarded-Host"]}')

    def redirect_uri(self, request):
        rd = request.query['rd']
        original_url = self.make_original_url(request)
        return str(
            yarl.URL(original_url).with_path(self.redirect_path).with_query(
                rd=rd)
        )

    async def exchange_auth_code(self, request):
        payload = dict(
            code=request.query['code'],
            redirect_uri=self.redirect_uri(request),
            **self.token_payload
        )
        async with self.session.post(self.token_url, json=payload) as resp:
            if resp.status == 200:
                body = await resp.json()
                return jwt.decode(body['id_token'], self.client_secret,
                                  algorithms=['HS256'],audience=self.client_id)

        return None

    async def get_id_token(self, request):
        session = await get_session(request)
        if 'id_token' in session:   
            id_token = session['id_token']
            if id_token['exp'] > time.time():
                return id_token
            else:
                del(session['id_token'])

    def profile_data(self, id_token):
        return dict((k, id_token[k]) for k in self.id_keys if k in id_token)


def setup_client(app):
    settings = app['settings']
    app['oidc_client'] = Client(
        settings.client_id, settings.client_secret, settings.client_base_url
    )


def get_client(request):
    return request.app['oidc_client']
