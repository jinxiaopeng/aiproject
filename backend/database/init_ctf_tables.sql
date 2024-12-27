-- 用户靶场档案表
CREATE TABLE IF NOT EXISTS user_ctf_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,           -- 关联到users表的外键
    points INT DEFAULT 0,                  -- 总积分
    ranking INT DEFAULT 0,                 -- 排名（改名避免与保留字冲突）
    last_challenge_time DATETIME NULL,     -- 最后挑战时间
    completed_challenges INT DEFAULT 0,     -- 完成的靶场数
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 靶场信息表
CREATE TABLE IF NOT EXISTS challenges (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    difficulty VARCHAR(20),
    points INTEGER DEFAULT 0,
    flag VARCHAR(200),
    
    -- 训练相关
    objectives JSONB,  -- 学习目标
    prerequisites JSONB,  -- 前置知识
    environment JSONB,  -- 环境信息
    notices JSONB,  -- 注意事项
    steps JSONB,  -- 训练步骤
    hints JSONB,  -- 提示信息
    
    -- 进程相关
    process_config JSONB,  -- 进程配置
    resource_limits JSONB,  -- 资源限制
    timeout_config JSONB,  -- 超时配置
    
    -- 状态
    is_active BOOLEAN DEFAULT TRUE,
    current_status VARCHAR(20) DEFAULT 'stopped',
    last_start_time TIMESTAMP WITH TIME ZONE,
    
    -- 统计
    completions INTEGER DEFAULT 0,
    pass_rate INTEGER DEFAULT 0,
    
    -- 时间
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 用户靶场关系表
CREATE TABLE IF NOT EXISTS user_challenges (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    challenge_id INTEGER REFERENCES challenges(id),
    
    status VARCHAR(20) DEFAULT 'not_started',  -- not_started, in_progress, completed
    start_time TIMESTAMP WITH TIME ZONE,
    complete_time TIMESTAMP WITH TIME ZONE,
    attempts INTEGER DEFAULT 0,
    
    -- 进度追踪
    current_step INTEGER DEFAULT 0,
    completed_steps JSONB DEFAULT '[]'::jsonb,
    
    -- 评分相关
    score INTEGER,
    feedback TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_challenges_category ON challenges(category);
CREATE INDEX IF NOT EXISTS idx_challenges_difficulty ON challenges(difficulty);
CREATE INDEX IF NOT EXISTS idx_challenges_status ON challenges(current_status);
CREATE INDEX IF NOT EXISTS idx_user_challenges_user_id ON user_challenges(user_id);
CREATE INDEX IF NOT EXISTS idx_user_challenges_challenge_id ON user_challenges(challenge_id);
CREATE INDEX IF NOT EXISTS idx_user_challenges_status ON user_challenges(status);

-- 创建更新时间触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为challenges表添加触发器
DROP TRIGGER IF EXISTS update_challenges_updated_at ON challenges;
CREATE TRIGGER update_challenges_updated_at
    BEFORE UPDATE ON challenges
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 为user_challenges表添加触发器
DROP TRIGGER IF EXISTS update_user_challenges_updated_at ON user_challenges;
CREATE TRIGGER update_user_challenges_updated_at
    BEFORE UPDATE ON user_challenges
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 训练进度表
CREATE TABLE IF NOT EXISTS training_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    challenge_id INTEGER REFERENCES challenges(id),
    current_step INTEGER DEFAULT 0,
    completed_tasks JSONB DEFAULT '[]'::jsonb,
    unlocked_hints JSONB DEFAULT '[]'::jsonb,
    start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_active_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, challenge_id)
);

-- 提示解锁表
CREATE TABLE IF NOT EXISTS hint_unlocks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    challenge_id INTEGER REFERENCES challenges(id),
    hint_index INTEGER NOT NULL,
    cost INTEGER NOT NULL,
    unlock_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, challenge_id, hint_index)
);

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_training_progress_user ON training_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_training_progress_challenge ON training_progress(challenge_id);
CREATE INDEX IF NOT EXISTS idx_hint_unlocks_user ON hint_unlocks(user_id);
CREATE INDEX IF NOT EXISTS idx_hint_unlocks_challenge ON hint_unlocks(challenge_id);

-- 用户技能表
CREATE TABLE IF NOT EXISTS user_skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    skill_type VARCHAR(50) NOT NULL,      -- web/system/crypto
    skill_level INT DEFAULT 0,            -- 技能等级
    skill_points INT DEFAULT 0,           -- 技能积分
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE KEY unique_user_skill (user_id, skill_type)
);

-- 提交记录表
CREATE TABLE IF NOT EXISTS submissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    challenge_id INT NOT NULL,
    submitted_flag VARCHAR(255) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    points_awarded INT DEFAULT 0,
    submitted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (challenge_id) REFERENCES challenges(id)
);

-- 添加索引以提高查询性能
CREATE INDEX idx_challenge_category ON challenges(category);
CREATE INDEX idx_challenge_difficulty ON challenges(difficulty);
CREATE INDEX idx_challenge_status ON challenges(current_status);
CREATE INDEX idx_training_progress_step ON training_progress(current_step);
CREATE INDEX idx_training_progress_completion ON training_progress(completed_at);
CREATE INDEX idx_hint_unlocks_time ON hint_unlocks(unlocked_at);
CREATE INDEX idx_skill_type ON user_skills(skill_type);
CREATE INDEX idx_submission_time ON submissions(submitted_at);