CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- Добавьте тестового администратора
INSERT INTO admins (name, password) VALUES ('admin', '1234');
