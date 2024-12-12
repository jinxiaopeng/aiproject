SET NAMES utf8mb4;
USE cyberlabs;
INSERT INTO labs (name, description, category, difficulty, docker_image, internal_port, environment, points, is_active) 
VALUES ('SQL注入基础训练', '通过一系列精心设计的SQL注入挑战，掌握SQL注入的基本原理和技巧', 'web', 'easy', 'webgoat/webgoat-8.0', 8080, '{"flag":"test"}', 100, 1); 