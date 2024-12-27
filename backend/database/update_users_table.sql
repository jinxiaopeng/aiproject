-- 修改role字段为ENUM类型
ALTER TABLE users 
MODIFY COLUMN role ENUM('admin', 'teacher', 'student', 'guest') NOT NULL DEFAULT 'student';

-- 修改status字段为ENUM类型
ALTER TABLE users 
MODIFY COLUMN status ENUM('active', 'inactive', 'banned', 'pending') NOT NULL DEFAULT 'active';

-- 添加用户个人信息字段
ALTER TABLE users
ADD COLUMN nickname VARCHAR(50),
ADD COLUMN avatar_url VARCHAR(255),
ADD COLUMN bio TEXT;

-- 添加索引
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);

-- 更新现有用户的角色和状态
UPDATE users SET role = 'student' WHERE role NOT IN ('admin', 'teacher', 'student', 'guest');
UPDATE users SET status = 'active' WHERE status NOT IN ('active', 'inactive', 'banned', 'pending'); 