SET NAMES utf8mb4;
USE cyberlabs;

CREATE TABLE lab_instances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lab_id INT NOT NULL,
    container_id VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'running',
    port INT NOT NULL,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE
); 