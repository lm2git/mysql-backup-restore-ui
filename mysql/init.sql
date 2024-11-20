-- Crea una tabella di esempio
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Inserisci alcuni dati di esempio
INSERT INTO users (username, email) VALUES
('testuser1', 'test1@example.com'),
('testuser2', 'test2@example.com'),
('testuser3', 'test3@example.com');