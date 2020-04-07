from .base import run_query
from .utils import base36encode

from .response import Response


async def read_tickets(request):
    """
    Returns tickets
    """
    sql_query = (
        "SELECT * "
        "FROM tickets "
        "ORDER BY created_at DESC")

    response = await run_query(request, sql_query)

    return response


async def read_ticket(request, id):
    """
    Returns ticket by id
    """
    sql_query = (
        "SELECT * "
        "FROM tickets "
        f"WHERE id={id} ")

    response = await run_query(request, sql_query, single=True)

    return response


async def create_ticket(request, ticket_json):
    """
    Creates ticket from json and returns its object
    """
    keys = ", ".join(map(str, ticket_json.keys()))
    values = "'" + "', '".join(map(str, ticket_json.values())) + "'"
    sql_query = (
        f"INSERT INTO tickets ({keys}) "
        f"VALUES ({values}) "
        "RETURNING * ")

    response = await run_query(request, sql_query, single=True)

    # update ticket with unique barcode for labels & internal usage
    ticket_dict = response.as_dict().get('data')
    barcode = generate_barcode(ticket_dict)
    id = ticket_dict.get('id')
    response = await update_ticket(request, id, {'barcode': barcode})

    return response


async def update_ticket(request, id, ticket_json):
    """
    Updates ticket from json and returns its object
    """
    keys = ", ".join(map(str, ticket_json.keys()))
    values = "'" + "', '".join(map(str, ticket_json.values())) + "'"
    sql_query = (
        f"UPDATE tickets SET ({keys}) "
        f"= ({values}) "
        f"WHERE id = {id} "
        "RETURNING * ")

    if len(ticket_json.keys()) == 1: # don't make use of parenthesis
        sql_query = (
            f"UPDATE tickets SET {keys} "
            f"= {values} "
            f"WHERE id = {id} "
            "RETURNING * ")

    if 'disabled' in ticket_json.keys():
        keys = "ticket_id, user_id, center_id"
        values = f"'{id}', '1', NULL"
        sql_query_extra = (
            f"INSERT INTO tickets_disabled ({keys}) "
            f"VALUES ({values}) "
            "RETURNING * ")
        await run_query(request, sql_query_extra, single=True)

    response = await run_query(request, sql_query, single=True)

    return response


async def delete_ticket(request, id):
    """
    Deletes ticket by id
    """
    sql_query = (
        "DELETE FROM tickets "
        f"WHERE id={id} "
        "RETURNING * ")

    response = await run_query(request, sql_query, single=True)

    return response
