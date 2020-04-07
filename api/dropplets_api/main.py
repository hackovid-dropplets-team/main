import argparse
import asyncio
import logging
import sys

from collections import defaultdict

from aiohttp import web
from dropplets_api.db import init_redis, close_redis, init_pg, close_pg
from dropplets_api.routes import setup_routes
from dropplets_api.settings import get_config


async def init_app(argv=None):

    config = get_config(argv)

    # setup middlewares
    middlewares = []

    # setup application
    app = web.Application(middlewares=middlewares)

    # load config from yaml file in current dir
    app['config'] = config

    # create connection to the database and redis
    app.on_startup.append(init_pg)
    app.on_startup.append(init_redis)

    # shutdown db connection on exit
    app.on_cleanup.append(close_pg)
    app.on_cleanup.append(close_redis)

    # setup views and routes
    setup_routes(app)

    return app


def main(argv):
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    #app = init_app(argv)
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app(argv))

    web.run_app(app, host=app['config']['host'], port=app['config']['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
