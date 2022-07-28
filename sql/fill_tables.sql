INSERT INTO token (email) VALUES ('seananchabra@hotmail.com');

INSERT INTO users (token_id, first_name, last_name) VALUES
((select id from token where email = 'seananchabra@hotmail.com'), 'Seanan', 'Chabra'),
((select id from token where email = 'seananchabra@hotmail.com'), 'Nirmala', 'Chabra'),
((select id from token where email = 'seananchabra@hotmail.com'), 'Prabhjot', 'Mudhar'),
((select id from token where email = 'seananchabra@hotmail.com'), 'Jason', 'Chabra');
