-- 重命名 password 列为 hashed_password
ALTER TABLE users CHANGE COLUMN password hashed_password VARCHAR(255); 