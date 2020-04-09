from aiohttp import web

from aiohttp_security import (
    remember, forget, authorized_userid,
    has_permission, login_required
)

from dropplets_api.web_responses import base

from dropplets_api.policies.authorization import (check_credentials, encrypt_password)

from dropplets_api.db_requests.users import (read_user_by_username, create_user)

import datetime
import re


class AuthHandler:

    app = None

    def __init__(self, app):
        self.app = app
        self.setup_routes(app)

    def setup_routes(self, app):
        app.router.add_routes([
            web.get('/', self.get_index),
            web.get('/auth', self.get_auth),
            web.post('/auth/login', self.post_auth_login),
            web.get('/auth/logout', self.get_auth_logout),
            web.post('/auth/register', self.post_auth_register)
        ])


    async def get_index(self, request):
        username = await authorized_userid(request)
        if username:
            response = web.Response(body='Logged in as {username}'.format(username=username))
        else:
            response = web.Response(body='Not logged in')
        return response


    @login_required
    async def get_auth(self, request):
        response = await base.get_authenticated_user(request)
        response_dict = response.as_dict()
        if response_dict is not None:
            del response_dict['data']['password']
        return web.json_response(response_dict)


    async def post_auth_register(self, request):
        json = await request.json()

        email = json.get('email')
        username = json.get('username')
        password = json.get('password')

        regex_pattern = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$")

        if regex_pattern.match(password) and username and password and email:
            encrypted_pwd = await encrypt_password(password)

            await create_user(request, username, encrypted_pwd, email)

            response = web.Response(body='Register succeed')
        else:
            response = web.Response(body='Register process failed')
        return response


    async def post_auth_login(self, request):
        import pdb; pdb.set_trace()
        json = await request.json()
        username = json.get('username')
        password = json.get('password')
        if await check_credentials(request, username, password):
            # init response with user json
            operation_coroutine = read_user_by_username(request, username)
            response_dict = (await base.handle_operation(request,
                operation_coroutine)).as_dict()

            #if response_dict['data']['unsubscribed_at'] is not None:
            #    return web.Response(status=401, text="Usuari inactiu")

            del response_dict['data']['password']
            response = web.json_response(response_dict)

            # enable cookie and alter response with proper set-cookie header
            await remember(request, response, username)
            return response

        return web.HTTPUnauthorized()


    @login_required
    async def get_auth_logout(self, request):
        response = web.HTTPNoContent()
        await forget(request, response)
        return response
