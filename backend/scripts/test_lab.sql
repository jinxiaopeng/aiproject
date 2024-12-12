USE cyberlabs;

-- 插入靶场数据
INSERT INTO labs (name, description, category, difficulty, docker_image, internal_port, environment, points, is_active) VALUES
('SQL注入基础训练', '通过一系列精心设计的SQL注入挑战，掌握SQL注入的基本原理和技巧', 'web', 'easy', 'webgoat/webgoat-8.0', 8080, '{"flag": "flag{sql_injection_basic_done}", "hints": ["尝试使用单引号", "注意SQL语句的闭合"]}', 100, true),
('XSS跨站脚本训练', '学习和实践各种类型的XSS攻击，提高Web安全防护能力', 'web', 'medium', 'webgoat/webgoat-8.0', 8080, '{"flag": "flag{xss_challenge_completed}", "hints": ["尝试插入JavaScript代码", "注意HTML编码"]}', 200, true),
('文件上传漏洞训练', '通过实践掌握文件上传漏洞的利用和防护方法', 'web', 'hard', 'webgoat/webgoat-8.0', 8080, '{"flag": "flag{file_upload_master}", "hints": ["检查文件类型验证", "尝试绕过前端验证"]}', 300, true),
('Linux提权训练', '在模拟环境中练习Linux系统的权限提升技术', 'system', 'medium', 'vulnerables/cve-2021-4034', 22, '{"flag": "flag{privilege_escalation_done}", "hints": ["查找SUID文件", "检查系统服务"]}', 250, true),
('密码破解训练', '学习各种密码破解技术和工具的使用方法', 'crypto', 'easy', 'webgoat/webgoat-8.0', 8080, '{"flag": "flag{password_cracked}", "hints": ["尝试使用字典攻击", "注意密码复杂度"]}', 150, true),
('网络嗅探训练', '学习使用网络嗅探工具分析网络流量', 'network', 'medium', 'vulnerables/metasploitable2', 80, '{"flag": "flag{network_sniffer_pro}", "hints": ["使用Wireshark分析", "关注HTTP流量"]}', 200, true),
('Web Shell训练', '学习Web Shell的原理和防护方法', 'web', 'hard', 'webgoat/webgoat-8.0', 8080, '{"flag": "flag{webshell_detected}", "hints": ["检查文件上传功能", "注意文件解析漏洞"]}', 300, true),
('缓冲区溢出训练', '学习基础的缓冲区溢出漏洞利用技术', 'system', 'hard', 'vulnerables/protostar', 22, '{"flag": "flag{buffer_overflow_master}", "hints": ["检查输入长度", "分析程序栈"]}', 350, true),
('CSRF漏洞训练', '学习跨站请求伪造漏洞的原理和防护', 'web', 'medium', 'webgoat/webgoat-8.0', 8080, '{"flag": "flag{csrf_challenge_done}", "hints": ["检查Token验证", "分析请求来源"]}', 200, true),
('Docker逃逸训练', '学习Docker容器逃逸技术和防护方法', 'system', 'hard', 'vulnerables/cve-2019-5736', 22, '{"flag": "flag{docker_escape_success}", "hints": ["检查容器权限", "分析Docker配置"]}', 400, true);

-- 插入一些用户成就数据
INSERT INTO user_achievements (user_id, category, achievement_type, points) VALUES
(1, 'web', 'first_blood', 100),
(1, 'system', 'quick_learner', 50),
(2, 'web', 'persistent', 75),
(2, 'crypto', 'code_breaker', 150),
(3, 'network', 'explorer', 80);

-- 插入系统日志
INSERT INTO system_logs (level, module, message, metadata) VALUES
('INFO', 'lab_manager', '新靶场环境已创建', '{"lab_id": 1, "user_id": 1}'),
('WARNING', 'container_manager', '容器资源使用率较高', '{"container_id": "abc123", "cpu_usage": 85}'),
('ERROR', 'lab_manager', '靶场环境启动失败', '{"lab_id": 3, "error": "端口被占用"}'); 