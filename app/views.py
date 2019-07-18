from aiohttp import web
import commento


async def commento_handler(request):
    redirect = commento.verify(request)
    if not redirect:
        return web.HTTPUnauthorized()
    else:
        return web.HTTPFound(redirect)


async def test_hander(request):
    print(request)
    return web.Response(text='OK')
