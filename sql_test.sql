-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS dv_test_db;
CREATE USER IF NOT EXISTS 'dv_test'@'localhost' IDENTIFIED BY 'dv_test_pwd';
GRANT ALL PRIVILEGES ON `dv_test_db`.* TO 'dv_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'dv_test'@'localhost';
FLUSH PRIVILEGES;
