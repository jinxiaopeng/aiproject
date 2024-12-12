SET NAMES utf8mb4;
USE cyberlabs;

INSERT INTO labs (name, description, category, difficulty, docker_image, internal_port, environment, points, is_active) VALUES
('XSS跨站脚本训练', '学习和实践各种类型的XSS攻击，提高Web安全防护能力', 'web', 'medium', 'webgoat/webgoat-8.0', 8080, '{"flag":"flag{xss_challenge_completed}"}', 200, 1),
('文件上传漏洞训练', '通过实践掌握文件上传漏洞的利用和防护方法', 'web', 'hard', 'webgoat/webgoat-8.0', 8080, '{"flag":"flag{file_upload_master}"}', 300, 1),
('Linux提权训练', '在模拟环境中练习Linux系统的权限提升技术', 'system', 'medium', 'vulnerables/cve-2021-4034', 22, '{"flag":"flag{privilege_escalation_done}"}', 250, 1),
('密码破解训练', '学习各种密码破解技术和工具的使用方法', 'crypto', 'easy', 'webgoat/webgoat-8.0', 8080, '{"flag":"flag{password_cracked}"}', 150, 1); 