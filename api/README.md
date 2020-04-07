# BACKEND API

Made with AIOHTTP: Asynchronous HTTP Client/Server for asyncio and Python

## Local developing

### Virtual environment

Create a virtual environment with *venv* standard python3 module and activate it:

```
python3 -m venv ./venv-dropplets
source venv-dropplets/bin/activate
```

### Install library and dependencies

From inside our virtual environment, upgrade pip to latest version and install aiohttp library and dependencies. Since *venv* is python3-only we don't need to add *3* suffix from now on

```
(venv-dropplets) pip install --upgrade pip
(venv-dropplets) pip install -e .
```

Last command installs aiohttp with some dependencies specified in setup.py and core package named dropplets-api in editable mode

#### Some of the packages used (relevant):

Additional destacable packages that are used and required in this project are:

- trafaret-config --> library for easily managing configuration options
- aioredis --> library for handling Redis
- aiohttp_session[aioredis] --> library for managing user sessions and storing to Redis
- aiohttp_security[session] --> library for managing authorizations with roles, groups, permissions, etc.

### Run server

```
(venv-dropplets) python -m dropplets_api
```
