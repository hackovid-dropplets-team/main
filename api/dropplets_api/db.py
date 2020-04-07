import asyncio
import asyncpg
import time
import logging
import datetime

from aioredis import create_pool

from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage

from aiohttp_security import setup as setup_security, SessionIdentityPolicy
from dropplets_api.policies.authorization import DBAuthorizationPolicy


class DBRecordNotFound(Exception):
    """Requested record in database was not found"""

class DBConflict(Exception):
    """There was a conflict/error in database"""

class Forbidden(Exception):
    """User don't have permissions to view info"""


async def init_redis(app):
    conf = app['config']['redis']
    redis_pool = await create_pool(
        (conf['host'], conf['port']))
    app['redis_pool'] = redis_pool
    setup_session(app, RedisStorage(redis_pool))


async def close_redis(app):
    app['redis_pool'].close()
    await app['redis_pool'].wait_closed()


async def init_pg(app):
    await start_pg(app)
    setup_security(app, SessionIdentityPolicy(), DBAuthorizationPolicy(app))


async def start_pg(app):
    conf = app['config']['postgres']

    async def connect():
        try:
            for db_name in conf['databases']:
                pool = await asyncpg.create_pool(
                    dsn='postgres://{user}:{password}@{host}:{port}/{database}'.format(
                        user=conf['user'],
                        password=conf['password'],
                        host=conf['host'],
                        port=conf['port'],
                        database=db_name
                    )
                )
                app['db_pool_'+db_name] = pool
            return True

        except asyncpg.exceptions.CannotConnectNowError as e:
            return False

    max_retry = 10
    while (max_retry > 0) and not await connect():
        max_retry -= 1
        await asyncio.sleep(5)

    if max_retry == 0:
        raise asyncpg.exceptions.CannotConnectNowError


async def close_pg(app, db=None):
    conf = app['config']['postgres']

    if db is not None:
        await app['db_pool_'+db].close()
    else:
        for db_name in conf['databases']:
            await app['db_pool_'+db_name].close()
