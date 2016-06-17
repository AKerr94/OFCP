CREATE DATABASE ofc;
USE ofc;

CREATE TABLE IF NOT EXISTS games
(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    game_id VARCHAR(40),
    game_state VARCHAR(2000)
) COMMENT='Game states table';

CREATE USER 'ofcdatabaseuser'@'172.18.47.11' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'ofcdatabaseuser'@'172.18.47.11' WITH GRANT OPTION;
