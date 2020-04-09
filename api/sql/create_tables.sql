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
