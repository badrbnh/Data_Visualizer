-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS dv_dev_db;
CREATE USER IF NOT EXISTS 'dv_dev'@'localhost' IDENTIFIED BY 'dv_dev_pwd';
GRANT ALL PRIVILEGES ON `dv_dev_db`.* TO 'dv_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'dv_dev'@'localhost';
FLUSH PRIVILEGES;

USE dv_dev_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id VARCHAR(60) PRIMARY KEY,
    username VARCHAR(128) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    email VARCHAR(128) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS data;
CREATE TABLE data (
    id VARCHAR(60) PRIMARY KEY,
    file_name VARCHAR(128) NOT NULL,
    user_id VARCHAR(60) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);




