Un cop arrencat Docker de la Postgres, entrar dins el contenidor amb

Docker exec -it <id_contenidor> bash

Dins executar:

psql -U postgres

i copiar el codi SQL de setup.sql
