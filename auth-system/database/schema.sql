CREATE DATABASE auth_system;

USE auth_system;

CREATE TABLE users(
    id INT AUTO_INCREAMENT PRIMARY KEY;
    name VARCHAR (100);
    email VARCHAR (100) UNIQUE;
    password VARCHAR (255)
);