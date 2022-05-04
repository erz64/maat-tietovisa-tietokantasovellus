CREATE TABLE questions (id SERIAL PRIMARY KEY, question_id INTEGER, question TEXT, answer TEXT);
CREATE TABLE images (id SERIAL PRIMARY KEY, question_id INTEGER, question_answer TEXT, name TEXT, data BYTEA);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, admin INTEGER);
CREATE TABLE scores (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, question TEXT, username TEXT, score INTEGER);
CREATE TABLE reviews (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, star TEXT, question_id INTEGER REFERENCES questions);