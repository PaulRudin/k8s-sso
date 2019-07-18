import hmac
import json

from aiohttp import web
import yarl

# see https://docs.commento.io/configuration/frontend/sso.html. Expected setup:
# we'll be behind nginx and this service will be only be hit once the user has
# authenticated via oidc (auth0 atm, but it could be another oidc provider), so
# we're extracting the information that commento wants and then redirecting
# back


def setup_commento(app):
    app['commento_hmac'] = hmac.new(app['settings'].commento_secret)
    app['commento_url'] = yarl.URL(app['settings'].commento_url)


def verify_params_present(request):
    try:
        return request.query['token'], request.query['hmac']
    except KeyError:
        raise web.HTTPBadRequest(text='Provide token and hmac query params')


def verify(request):
    token, hmac = verify_params_present(request)
    digest = request.app['commento_hmac'].digest(token)
    if hmac.compare_digest(digest, hmac):
        payload, payload_digest = make_payload(request, token) 
        return request.app['commento_url'].with_query(
            payload=payload, hmac=payload_digest
        )


def make_payload(request, token, hmac):
    print(request)
    user_data = dict(
        token=token,
        email='',
        name='',
        link='',
        photo=''
    )
    json_data = json.dumps(user_data)
    digest = hmac.digest(json)
    return json_data, digest
