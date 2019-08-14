import os

import pytest
from dotenv import load_dotenv
from app.app import make_app


@pytest.fixture
def cli(loop, aiohttp_client):
    load_dotenv('secrets.env')
    app = make_app()
    return loop.run_until_complete(aiohttp_client(app))
