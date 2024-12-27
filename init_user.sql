USE aiproject;

INSERT INTO users (
    username,
    email,
    hashed_password,
    role,
    status,
    created_at,
    updated_at
) VALUES (
    'admin',
    'admin@example.com',
    'admin123',
    'admin',
    'active',
    NOW(),
    NOW()
); 