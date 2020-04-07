from aiohttp_security.abc import AbstractAuthorizationPolicy
import hashlib, binascii


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, app):
        self.app = app

    async def authorized_userid(self, identity):
        """Retrieve authorized username (not id!).
        Return the user_id of the user identified by the identity (= username)
        or 'None' if no user exists related to the identity.
        """
        # mirar que l'usuari existeix i no està deshabilitat. retornar
        # l'identitat en aquest cas, o None
        sql_query = (
            "SELECT COUNT(*) "
            "FROM users "
            f"WHERE username='{identity}' ")
        ret = None
        async with self.app['db_pool_dropplets'].acquire() as conn:
            ret = await conn.fetchval(sql_query, column=0)

        if ret:
            return identity
        return None

    async def permits(self, identity, roles, context=None):
        """Check user roles.
        Return wheter if the identity has its role contained in 'roles'.

        Roles are defined as follow:
        - id: 1 name: admin
        - id: 2 name: normal
        """
        if identity is None:
            return False

        roles_array = roles.split(',')

        sql_query = (
            "SELECT role_id "
            "FROM users "
            f"WHERE username='{identity}' ")
        role_id = None
        async with self.app['db_pool_dropplets'].acquire() as conn:
            role_id = await conn.fetchval(sql_query, column=0)

        if role_id is not None:
            sql_query = (
                "SELECT name "
                "FROM roles "
                f"WHERE id='{role_id}' ")
            role_name = None
            async with self.app['db_pool_dropplets'].acquire() as conn:
                role_name = await conn.fetchval(sql_query, column=0)

            if role_name in roles_array:
                return True

        return False


async def check_credentials(request, username, password):
    """
    Use sha256 crypt to verify credentials
    """
    sql_query = (
        "SELECT password "
        "FROM users "
        f"WHERE username='{username}' ")
    record = None
    async with request.app['db_pool_dropplets'].acquire() as conn:
        record = await conn.fetchrow(sql_query)

    if record is None: # user not found or error
        return False

    password_a = record.get('password') # from DB
    password_b = await encrypt_password(password) # plain, entered by user

    return password_a == password_b


async def encrypt_password(password):
    """
    Use sha256 crypt
    """
    # The following function provides PKCS#5 password-based key derivation.
    # It uses HMAC as pseudorandom function
    dk = hashlib.pbkdf2_hmac(
        'sha256', bytes(password, 'utf-8'), b'salt', 100000)
    enc_password = binascii.hexlify(dk).decode()

    return enc_password
