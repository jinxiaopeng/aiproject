-- 创建靶场训练数据库
CREATE DATABASE IF NOT EXISTS cyberlabs DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE cyberlabs;

-- 创建靶场表
CREATE TABLE IF NOT EXISTS labs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category ENUM('web', 'system', 'network', 'crypto', 'reverse') NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL,
    docker_image VARCHAR(255) NOT NULL,
    internal_port INT NOT NULL,
    environment JSON,
    points INT NOT NULL DEFAULT 100,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建靶场实例表
CREATE TABLE IF NOT EXISTS lab_instances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lab_id INT NOT NULL,
    container_id VARCHAR(100) NOT NULL,
    status ENUM('running', 'stopped', 'completed', 'error', 'expired') NOT NULL,
    port INT NOT NULL,
    score INT DEFAULT 0,
    completion_rate DECIMAL(5,2) DEFAULT 0.00,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建实验步骤表
CREATE TABLE IF NOT EXISTS lab_steps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    instance_id INT NOT NULL,
    step_number INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('pending', 'completed', 'skipped') NOT NULL DEFAULT 'pending',
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (instance_id) REFERENCES lab_instances(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建实验报告表
CREATE TABLE IF NOT EXISTS lab_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    instance_id INT NOT NULL,
    content TEXT NOT NULL,
    findings TEXT,
    conclusion TEXT,
    attachments JSON,
    score INT DEFAULT 0,
    feedback TEXT,
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instance_id) REFERENCES lab_instances(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建系统日志表
CREATE TABLE IF NOT EXISTS system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level VARCHAR(20) NOT NULL,
    module VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    metadata JSON,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;