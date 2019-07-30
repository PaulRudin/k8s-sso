import logging

from aiohttp import web
import commento

logger = logging.getLogger(__name__)

async def commento_handler(request):
    redirect = commento.verify(request)
    if not redirect:
        return web.HTTPUnauthorized()
    else:
        return web.HTTPFound(redirect)


async def test_handler(request):
    heads = '\n'.join(f'{k}: {v}' for k, v in request.headers.items())
    logger.debug(heads)
    return web.Response(text='OK')
