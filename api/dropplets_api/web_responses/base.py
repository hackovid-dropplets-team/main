from aiohttp import web
from functools import wraps

from dropplets_api.db import DBRecordNotFound, DBConflict, Forbidden
from dropplets_api.db_requests.users import read_user_by_username

from aiohttp_security import authorized_userid


class SimpleRequest:
    """
    Simple request object for using when no request is present and we just need
    an object with 'app' as an attribute
    """
    def __init__(self, app):
        self.app = app


async def handle_operation(request, operation_coroutine, role_name=None):
    """
    Returns a json response if operation succeed.
    Otherwise, raises an exception.
    """
    try:
        response = await operation_coroutine
    except DBRecordNotFound as e:
        raise web.HTTPNotFound(text=str(e))
    except DBConflict as e:
        raise web.HTTPConflict(text=str(e))
    except Forbidden as e:
        raise web.HTTPForbidden(text=str(e))

    if role_name is not None:
        response.set_role_name(role_name)
    return response


async def get_authenticated_user(request):
    username = await authorized_userid(request)

    operation_coroutine = read_user_by_username(request, username)
    user = await handle_operation(request, operation_coroutine)

    return user


def get_id_param(request):
    id = None
    try:
        id = int(request.match_info['id'])
    except TypeError as e:
        raise web.HTTPUnprocessableEntity(text=str(e))
    return id


def get_ordering_params(request):
    order = request.query.get('order', '')
    sort = request.query.get('sort', 'desc')
    if (sort != 'asc') or (sort != 'desc'):
        sort = 'desc'

    return {
        'order': order,
        'sort': sort
    }


def get_paging_params(request):
    if ((request.query.get('limit') is not None) and
        (request.query.get('page') is not None)):
        limit = request.query.get('limit', '25')
        page = request.query.get('page', '1')
        offset = str((int(page) * int(limit)) - int(limit))

        return {
            'limit': limit,
            'page': page,
            'offset': offset
        }
    return None
