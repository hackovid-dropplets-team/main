from aiohttp import web

from dropplets_api.web_responses import base
from dropplets_api.db_requests.response import Response

import dropplets_api.db_requests.tickets as db_requests

from aiohttp_security import (login_required, has_permission, authorized_userid,
    forget)


class TicketsHandler:

    app = None

    def __init__(self, app):
        self.app = app
        self.setup_routes(app)

    def setup_routes(self, app):
        app.router.add_routes([
            web.get('/tickets', self.get_tickets),
            web.get('/tickets/{id}', self.get_ticket),
            web.post('/tickets', self.post_ticket),
            web.put('/tickets/{id}', self.put_ticket),
            web.delete('/tickets/{id}', self.delete_ticket),
        ])


    @login_required
    async def get_tickets(self, request):
        operation_coroutine = db_requests.read_tickets(request)

        response = await base.handle_operation(request, operation_coroutine)

        response_dict = response.as_dict()

        return web.json_response(response_dict)


    @login_required
    async def get_ticket(self, request):
        id = base.get_id_param(request)

        operation_coroutine = db_requests.read_ticket(request, id)

        response = await base.handle_operation(request, operation_coroutine)

        response_dict = response.as_dict()

        return web.json_response(response_dict)


    @login_required
    async def post_ticket(self, request):
        ticket_json = await request.json()
        if not len(ticket_json):
            raise web.HTTPUnprocessableEntity()

        operation_coroutine = db_requests.create_ticket(request, ticket_json)

        response = await base.handle_operation(request, operation_coroutine)

        return web.json_response(response.as_dict())


    @login_required
    @has_permission('admin')
    async def put_ticket(self, request):
        id = base.get_id_param(request)

        ticket_json = await request.json()
        if not len(ticket_json):
            raise web.HTTPUnprocessableEntity()

        operation_coroutine = db_requests.update_ticket(request, id, ticket_json)

        response = await base.handle_operation(request, operation_coroutine)

        return web.json_response(response.as_dict())


    @login_required
    @has_permission('admin')
    async def delete_ticket(self, request):
        id = base.get_id_param(request)

        operation_coroutine = db_requests.delete_ticket(request, id)

        response = await base.handle_operation(request, operation_coroutine)

        return web.json_response(response.as_dict())
