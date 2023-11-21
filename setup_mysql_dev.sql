-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS dv_dev_db;
CREATE USER IF NOT EXISTS 'dv_dev'@'localhost' IDENTIFIED BY 'dv_dev_pwd';
GRANT ALL PRIVILEGES ON `dv_dev_db`.* TO 'dv_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'dv_dev'@'localhost';
FLUSH PRIVILEGES;
