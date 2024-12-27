-- 创建主数据库
CREATE DATABASE IF NOT EXISTS ctf_practice DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE ctf_practice;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建靶场信息表
CREATE TABLE IF NOT EXISTS challenges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL,
    points INT NOT NULL DEFAULT 0,
    flag VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建提交记录表
CREATE TABLE IF NOT EXISTS submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    challenge_id INT NOT NULL,
    submitted_flag VARCHAR(255) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (challenge_id) REFERENCES challenges(id)
);

-- 创建用户进度表
CREATE TABLE IF NOT EXISTS user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    challenge_id INT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    complete_time TIMESTAMP NULL,
    attempts INT DEFAULT 0,
    is_completed BOOLEAN DEFAULT false,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (challenge_id) REFERENCES challenges(id),
    UNIQUE KEY unique_user_challenge (user_id, challenge_id)
);

-- 插入一些示例靶场数据
INSERT INTO challenges (title, description, category, difficulty, points, flag) VALUES
('基础SQL注入', '一个简单的SQL注入练习，通过绕过登录验证获取flag', 'SQL注入', 'easy', 100, 'flag{sql_injection_success}'),
('XSS攻击入门', '尝试在留言板中注入JavaScript代码', 'XSS', 'easy', 100, 'flag{xss_basic_complete}'),
('文件上传漏洞', '尝试上传一个WebShell到服务器', '文件上传', 'medium', 200, 'flag{file_upload_success}'); 