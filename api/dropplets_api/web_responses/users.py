from aiohttp import web

from dropplets_api.web_responses import base
from dropplets_api.db_requests.response import Response
from dropplets_api.policies.authorization import encrypt_password

import dropplets_api.db_requests.users as db_requests

from aiohttp_security import (login_required, has_permission, authorized_userid,
    forget)


class UsersHandler:

    app = None

    def __init__(self, app):
        self.app = app
        self.setup_routes(app)

    def setup_routes(self, app):
        app.router.add_routes([
            web.get('/users', self.get_users),
            web.get('/users/{id}', self.get_user),
            web.post('/users', self.post_user),
            web.put('/users/{id}', self.put_user),
            web.delete('/users/{id}', self.delete_user),
        ])


    @login_required
    async def get_users(self, request):
        operation_coroutine = db_requests.read_users(request)

        response = await base.handle_operation(request, operation_coroutine)

        response_dict = response.as_dict()
        for user in response_dict['data']:
            if 'password' in user:
                del user['password']

        return web.json_response(response_dict)


    @login_required
    async def get_user(self, request):
        id = base.get_id_param(request)

        operation_coroutine = db_requests.read_user(request, id)

        response = await base.handle_operation(request, operation_coroutine)

        response_dict = response.as_dict()
        if 'password' in response_dict['data']:
            del response_dict['data']['password']

        return web.json_response(response_dict)


    @login_required
    @has_permission('admin,manager')
    async def post_user(self, request):
        user_json = await request.json()
        user_json['role_id'] = 3
        user_json['password'] = await encrypt_password(user_json['password'])
        if not len(user_json):
            raise web.HTTPUnprocessableEntity()

        operation_coroutine = db_requests.create_user(request, user_json)

        response = await base.handle_operation(request, operation_coroutine)

        return web.json_response(response.as_dict())


    @login_required
    @has_permission('admin')
    async def put_user(self, request):
        id = base.get_id_param(request)

        user_json = await request.json()
        if not len(user_json):
            raise web.HTTPUnprocessableEntity()

        operation_coroutine = db_requests.update_user(request, id, user_json)

        response = await base.handle_operation(request, operation_coroutine)

        return web.json_response(response.as_dict())


    @login_required
    @has_permission('admin')
    async def delete_user(self, request):
        id = base.get_id_param(request)

        operation_coroutine = db_requests.delete_user(request, id)

        response = await base.handle_operation(request, operation_coroutine)

        return web.json_response(response.as_dict())
