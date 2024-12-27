-- 创建靶场数据库表
USE challenge_db;

-- 删除已存在的表（如果存在）
DROP TABLE IF EXISTS flag;
DROP TABLE IF EXISTS users;

-- 创建用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(10) NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建flag表
CREATE TABLE flag (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入基础用户数据
INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('guest', 'guest123', 'user'),
('test', 'test123', 'user');

-- 插入flag
INSERT INTO flag (flag) VALUES
('flag{sql_1nj3ct10n_m4st3r_2023}');