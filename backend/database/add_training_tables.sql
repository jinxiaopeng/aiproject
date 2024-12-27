-- 训练记录表
CREATE TABLE IF NOT EXISTS trainings (
    id VARCHAR(36) PRIMARY KEY,           -- UUID
    user_id INT NOT NULL,
    challenge_id INT NOT NULL,
    start_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME NULL,
    status ENUM('in_progress', 'completed', 'failed') NOT NULL DEFAULT 'in_progress',
    progress JSON NOT NULL DEFAULT ('{}'),
    score INT DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (challenge_id) REFERENCES challenges(id)
);

-- 训练步骤表
CREATE TABLE IF NOT EXISTS training_steps (
    id VARCHAR(36) PRIMARY KEY,           -- UUID
    training_id VARCHAR(36) NOT NULL,
    step_number INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    completed DATETIME NULL,
    result JSON NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (training_id) REFERENCES trainings(id) ON DELETE CASCADE,
    UNIQUE KEY unique_training_step (training_id, step_number)
);

-- 添加索引以提高查询性能
CREATE INDEX idx_training_user ON trainings(user_id);
CREATE INDEX idx_training_challenge ON trainings(challenge_id);
CREATE INDEX idx_training_status ON trainings(status);
CREATE INDEX idx_training_step_number ON training_steps(step_number);
CREATE INDEX idx_training_step_completed ON training_steps(completed); 