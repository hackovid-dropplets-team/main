import pathlib

from aiohttp import web

from dropplets_api.web_responses.auth import AuthHandler
from dropplets_api.web_responses.tickets import TicketsHandler
from dropplets_api.web_responses.users import UsersHandler


PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    AuthHandler(app)
    TicketsHandler(app)
    UsersHandler(app)

    setup_static_routes(app)


def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=PROJECT_ROOT / 'static',
                          name='static')
