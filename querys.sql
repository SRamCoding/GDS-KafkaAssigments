CREATE DATABASE IF NOT EXISTS assKafka_BuyOnline_Company;

USE assKafka_BuyOnline_Company;

CREATE TABLE product 
(
    id INT PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(255),
    price FLOAT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
