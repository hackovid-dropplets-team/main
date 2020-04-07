from .base import run_query

from .response import Response


async def read_users(request):
    """
    Returns users
    """
    sql_query = (
        "SELECT * "
        "FROM users ")

    response = await run_query(request, sql_query)

    return response


async def read_user(request, id):
    """
    Returns user by id
    """
    sql_query = (
        "SELECT * "
        "FROM users "
        f"WHERE id={id} ")

    response = await run_query(request, sql_query, single=True)

    return response


async def read_user_by_username(request, username):
    """
    Returns user by username
    """
    sql_query = (
        "SELECT * "
        "FROM users "
        f"WHERE username='{username}' ")

    response = await run_query(request, sql_query, single=True)

    return response


async def create_user(request, user_json):
    """
    Creates user from json and returns its object
    """
    keys = ", ".join(map(str, user_json.keys()))
    values = "'" + "', '".join(map(str, user_json.values())) + "'"
    sql_query = (
        f"INSERT INTO users ({keys}) "
        f"VALUES ({values}) "
        "RETURNING * ")

    response = await run_query(request, sql_query, single=True)

    return response


async def update_user(request, id, user_json):
    """
    Updates user from json and returns its object
    """
    keys = ", ".join(map(str, user_json.keys()))
    values = "'" + "', '".join(map(str, user_json.values())) + "'"
    sql_query = (
        f"UPDATE users SET ({keys}) "
        f"= ({values}) "
        f"WHERE id = {id} "
        "RETURNING * ")

    if len(user_json.keys()) == 1: # don't make use of parenthesis
        sql_query = (
            f"UPDATE users SET {keys} "
            f"= {values} "
            f"WHERE id = {id} "
            "RETURNING * ")

    if 'disabled' in user_json.keys():
        keys = "user_id, by_user_id, center_id"
        values = f"'{id}', '1', NULL"
        sql_query_extra = (
            f"INSERT INTO users_disabled ({keys}) "
            f"VALUES ({values}) "
            "RETURNING * ")
        await run_query(request, sql_query_extra, single=True)

    response = await run_query(request, sql_query, single=True)

    return response


async def delete_user(request, id):
    """
    Deletes user by id
    """
    sql_query = (
        "DELETE FROM users "
        f"WHERE id={id} "
        "RETURNING * ")

    response = await run_query(request, sql_query, single=True)

    return response
