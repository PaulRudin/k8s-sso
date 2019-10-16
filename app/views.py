import json
import logging
import secrets

from aiohttp import web
from aiohttp_session import get_session

import client

logger = logging.getLogger(__name__)


async def auth_handler(request):
    '''endpoint for nginx.ingress.kubernetes.io/auth-url. nginx makes a request
    here, if it gets 401 or 403 it redirects to the signin handler, otherwise
    we should give 200 and the response to the original url will proceed.

    '''
    oidc_client = client.get_client(request)

    id_token = await oidc_client.get_id_token(request)

    if id_token:
        headers = {
            'X-Auth-ID': json.dumps(oidc_client.profile_data(id_token))
        }
        return web.Response(text='OK', headers=headers)

    return web.HTTPUnauthorized()


async def signin_handler(request):
    '''endpoint for nginx.ingress.kubernetes.io/auth_signin nginx redirects us here
    if the original auth_request gave something other than 200

    '''
    oidc_client = client.get_client(request)

    redirect = oidc_client.redirect_uri(request)

    state = secrets.token_urlsafe()
    session = await get_session(request)
    session['state'] = state
    redirect_url = oidc_client.signin_url.update_query(
        state=state, redirect_uri=redirect
    )

    return web.HTTPFound(redirect_url)


async def check_state(request):
    '''
    Raises an http exception if the appropriate state hasn't round-tripped
    '''

    if 'state' not in request.query:
        raise web.HTTPBadRequest(text='state query parameter not provided')
    
    session = await get_session(request)
    if 'state' not in session:
        # not sure what error this should be. Either someone has cleared
        # cookies, or this is an attack
        raise web.HTTPUnauthorized(text='state missing')

    if session['state'] != request.query['state']:
        raise web.HTTPUnauthorized(text='state mismatch')


async def callback_handler(request):
    '''endpoint for redirection following successful sign in'''
    await check_state(request)

    if 'code' not in request.query:
        raise web.HTTPBadRequest(text='must provide code')

    oidc_client = client.get_client(request)
    id_token = await oidc_client.exchange_auth_code(request)
    if id_token:
        session = await get_session(request)
        session['id_token'] = id_token
        rd = request.query['rd']
        return web.HTTPFound(rd)
    return web.HTTPUnauthorized(text='bad token exchange')


async def hc(request):
    return web.Response(text='OK')
