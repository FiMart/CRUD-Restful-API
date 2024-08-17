CREATE DATABASE userdb;

USE userdb;

CREATE TABLE users (
    uid INT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);

INSERT INTO users (uid, name, age) VALUES
(121, 'Alice', 18),
(122, 'Bob', 17),
(123, 'Cindy', 25),
(124, 'Dan', 21);
