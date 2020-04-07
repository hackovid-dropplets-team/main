## Setup

Follow instructions of */README.md* file from repository root directory for cloning project and preparing the environment.

## dropplets_api/ APP structure

Top/First level modules:
- main.py : Application starting point
- settings.py : Provides configuration from config/ directory and interprets it using trafaret from utils
- db.py : Handles connections either to PostgreSQL and Redis
- routes.py : Sets all application api routes with its handlers
- utils.py : Maps/models configuration to trafaret

### db_requests/

Contains the major part of the application logic. base.py and utils.py are defined to abstract generic processes. Functions defined here, are called mainly from web_responses handlers. Others are used internally. See */db_requests/README.md*

### policies/

Holds an authorization policy defined for using in this application. Overrides needed methods from an abstract authorization policy and defines a check_credentials function. Search on documentation from *aiohttp_security* library for more info.

### scripts/

Contains bash sh scripts

### static/

As its name suggests, is used to hold static files. A specific route to serve name agnostic files which points to this directory is defined into routes.py. For now, a swagger configuration file is served, that is used in swagger-ui and swagger-editor containers (swagger-editor does not allow, at the moment of writing this lines, to save and persist changes onto a file, so it must be done manually when using it)

### web_responses/

Contains all application api routes (public) handlers. base.py and utils.py modules are defined here too for ordering, pagination and other helpful features. Handler classes defined here are imported in *routes.py* and instantiated with the current aplication instance.
