SET ROLE 'dropplets_user';

INSERT INTO public.users (role_id,username,firstname,lastname,password,email,phone,created_at,updated_at,last_login) VALUES
(1,'acomas','Arnau','Comas Codina','0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5','comas1992@gmail.com','662284138','2020-04-07 17:14:33.978',NULL,NULL)
,(1,'prova','Prova','Prova','0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5','prova@prova.com','','2020-04-07 19:09:14.807',NULL,NULL)
,(1,'nom.cognoms','Nom','Cognoms','0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5','test@test.com','','2020-04-07 19:10:02.017',NULL,NULL)
;

--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: polls
--

-- SELECT pg_catalog.setval('user_id_seq', 1, true);
