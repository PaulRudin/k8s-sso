from aiohttp import web

async def test_hc(cli, loop):
    resp = await cli.get('/hc')
    assert resp.status == 200
    text = await resp.text()
    assert 'OK' in text
