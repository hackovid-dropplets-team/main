SET ROLE 'dropplets_user';

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
