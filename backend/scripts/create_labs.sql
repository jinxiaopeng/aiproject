CREATE DATABASE IF NOT EXISTS cyberlabs DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cyberlabs;

DROP TABLE IF EXISTS labs;

CREATE TABLE labs (
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
); 