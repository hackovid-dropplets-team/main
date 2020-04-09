DROP DATABASE IF EXISTS dropplets;
DROP ROLE IF EXISTS dropplets_user;
CREATE USER dropplets_user WITH PASSWORD 'dropplets_pass';
CREATE DATABASE dropplets ENCODING 'UTF8';
GRANT ALL PRIVILEGES ON DATABASE dropplets TO dropplets_user;

\connect dropplets

SET ROLE 'dropplets_user';

BEGIN;
--
-- Create model User
--
CREATE TABLE users (
	id SERIAL NOT NULL PRIMARY KEY,
	is_admin BOOLEAN DEFAULT false,
	username VARCHAR (200) UNIQUE NOT NULL,
	firstname VARCHAR (200),
	lastname VARCHAR (200),
	password VARCHAR (200) NOT NULL,
	email VARCHAR (200) UNIQUE,
	phone VARCHAR (200),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	last_login TIMESTAMP,
	disabled BOOLEAN DEFAULT false
);

--
-- Create model Ticket
--
CREATE TABLE tickets (
	id SERIAL NOT NULL PRIMARY KEY,
	user_id INTEGER,
	title VARCHAR (200) UNIQUE,
	description VARCHAR (200) NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	coordinates POINT NOT NULL,
	disabled BOOLEAN DEFAULT false
);

COMMIT;

-- DEFINE FOREIGN KEYS
ALTER TABLE public.tickets ADD CONSTRAINT tickets_fk FOREIGN KEY (user_id) REFERENCES public.users(id);

-- TABLES FOR DISABLED ITEMS
CREATE TABLE tickets_disabled (
	id SERIAL NOT NULL PRIMARY KEY,
	ticket_id INTEGER,
	user_id INTEGER NOT NULL,
	disabled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE users_disabled (
	id SERIAL NOT NULL PRIMARY KEY,
	user_id INTEGER,
	by_user_id INTEGER NOT NULL,
	disabled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE public.tickets_disabled ADD CONSTRAINT tickets_disabled_fk FOREIGN KEY (order_id) REFERENCES public.tickets(id);
ALTER TABLE public.tickets_disabled ADD CONSTRAINT tickets_disabled_fk_1 FOREIGN KEY (user_id) REFERENCES public.users(id);
ALTER TABLE public.users_disabled ADD CONSTRAINT users_disabled_fk FOREIGN KEY (user_id) REFERENCES public.users(id);
ALTER TABLE public.users_disabled ADD CONSTRAINT users_disabled_fk_1 FOREIGN KEY (by_user_id) REFERENCES public.users(id);

INSERT INTO public.users (is_admin,username,firstname,lastname,password,email,phone,created_at,updated_at,last_login) VALUES
(true,'acomas',NULL,NULL,'0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5','comas1992@gmail.com','662284138','2020-04-07 17:14:33.978',NULL,NULL)
,(false,'prova',NULL,NULL,'0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5','prova@prova.com','','2020-04-07 19:09:14.807',NULL,NULL)
,(false,'nom.cognoms',NULL,NULL,'0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5','test@test.com','','2020-04-07 19:10:02.017',NULL,NULL)
;

INSERT INTO public.tickets (user_id,title,description,coordinates) VALUES
(1,'Tasca 1','Descripció 1',point(41.864049, 1.978700))
,(1,'Tasca 2','Descripció 2',point(41.864760, 1.970868))
,(1,'Tasca 3','Descripció 3',point(41.867812, 1.943327))
;
