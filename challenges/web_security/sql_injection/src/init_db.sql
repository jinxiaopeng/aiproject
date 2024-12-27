DROP DATABASE IF EXISTS ctf_db;
CREATE DATABASE ctf_db;
USE ctf_db;

-- 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 单独的 flag 表
CREATE TABLE secret_flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag_key VARCHAR(50) NOT NULL,
    flag_value VARCHAR(100) NOT NULL,
    hint TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入一些普通用户
INSERT INTO users (username, password, email) VALUES 
    ('admin', 'admin123', 'admin@test.com'),
    ('test', 'test123', 'test@test.com'),
    ('guest', 'guest123', 'guest@test.com');

-- 插入 flag
INSERT INTO secret_flags (flag_key, flag_value, hint) VALUES 
    ('sql_injection_flag', 'flag{n0w_y0u_c4n_sql_1nj3ct}', 'Try to find me using UNION SELECT'); 