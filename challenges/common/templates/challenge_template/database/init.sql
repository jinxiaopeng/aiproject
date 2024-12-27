-- 创建数据库
DROP DATABASE IF EXISTS ctf_db;
CREATE DATABASE ctf_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ctf_db;

-- 创建用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建flag表
CREATE TABLE flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag_key VARCHAR(50) NOT NULL UNIQUE,
    flag_value VARCHAR(100) NOT NULL,
    hint TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入初始数据
INSERT INTO users (username, password, email) VALUES 
    ('admin', 'admin123', 'admin@test.com'),
    ('test', 'test123', 'test@test.com');

INSERT INTO flags (flag_key, flag_value, hint) VALUES 
    ('test_flag', 'flag{test_flag}', '这是一个测试flag');
 