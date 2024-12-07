# Crear la base de datos
CREATE DATABASE datadb;

# Usar la base de datos creada
USE datadb;

# Crear la tabla con UUID como ID
CREATE TABLE alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    aprobado BOOLEAN NOT NULL,
    nota FLOAT NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



# Insertar 10 registros en la tabla 'tweets'
INSERT INTO alumnos (nombre, apellido, aprobado, nota, fecha) VALUES
('Juan', 'Pérez', TRUE, 7.5, '2024-09-01 00:00:00'),
('María', 'López', FALSE, 4.2, '2024-09-02 00:00:00'),
('Carlos', 'García', TRUE, 8.9, '2024-09-03 00:00:00'),
('Lucía', 'Martínez', TRUE, 9.1, '2024-09-04 00:00:00'),
('Sofía', 'Fernández', FALSE, 5.0, '2024-09-05 00:00:00');