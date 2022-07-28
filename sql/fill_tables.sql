INSERT INTO users (email) VALUES ('seananchabra@hotmail.com');

INSERT INTO invites (user_id, first_name, last_name) VALUES
((select id from users where email = 'seananchabra@hotmail.com'), 'Seanan', 'Chabra'),
((select id from users where email = 'seananchabra@hotmail.com'), 'Nirmala', 'Chabra'),
((select id from users where email = 'seananchabra@hotmail.com'), 'Prabhjot', 'Mudhar'),
((select id from users where email = 'seananchabra@hotmail.com'), 'Jason', 'Chabra');
