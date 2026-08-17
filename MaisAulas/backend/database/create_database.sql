DROP DATABASE IF EXISTS aula_conectada;
CREATE DATABASE aula_conectada CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aula_conectada;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS announcements;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS activities;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS classes;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    grade VARCHAR(40) NOT NULL,
    shift VARCHAR(30) NOT NULL DEFAULT 'Manhã',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    specialty VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    class_id INT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_students_class FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE SET NULL
);

CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(20) NOT NULL DEFAULT '#5b6ff5',
    teacher_id INT NULL,
    CONSTRAINT fk_subjects_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
);

CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(160) NOT NULL,
    description TEXT,
    subject_id INT NOT NULL,
    class_id INT NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    max_score DECIMAL(5,2) NOT NULL DEFAULT 10,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_activities_subject FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    CONSTRAINT fk_activities_class FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    INDEX idx_activities_due_date (due_date),
    INDEX idx_activities_status (status)
);

CREATE TABLE grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    activity_id INT NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    feedback VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_grades_student FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    CONSTRAINT fk_grades_activity FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
    UNIQUE KEY uq_grade_student_activity (student_id, activity_id)
);

CREATE TABLE announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(160) NOT NULL,
    message TEXT NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'Geral',
    published_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO classes (name, grade, shift) VALUES
('Turma 2B', '2º Ano', 'Manhã'),
('Turma 1A', '1º Ano', 'Manhã'),
('Turma 3C', '3º Ano', 'Tarde');

INSERT INTO teachers (name, email, specialty) VALUES
('Lucas Almeida', 'lucas@aula.local', 'Matemática'),
('Juliana Costa', 'juliana@aula.local', 'Português'),
('Marina Souza', 'marina@aula.local', 'Biologia');

INSERT INTO students (name, email, class_id, status) VALUES
('Maria Silva', 'maria@aula.local', 1, 'active'),
('João Pedro', 'joao@aula.local', 1, 'active'),
('Ana Clara', 'ana@aula.local', 1, 'active'),
('Lucas Ferreira', 'lucas.aluno@aula.local', 1, 'active');

INSERT INTO subjects (name, color, teacher_id) VALUES
('Matemática', '#7568F5', 1),
('Português', '#4CC7A5', 2),
('Física', '#F6A74B', 1),
('Biologia', '#6EC6A8', 3);

INSERT INTO activities (title, description, subject_id, class_id, due_date, status, max_score) VALUES
('Exercícios de Matemática', 'Lista de exercícios sobre funções.', 1, 1, CURRENT_DATE + INTERVAL 2 DAY, 'pending', 10),
('Redação - Tema livre', 'Produção textual com tema livre.', 2, 1, CURRENT_DATE + INTERVAL 4 DAY, 'pending', 10),
('Relatório de Biologia', 'Relatório sobre ecossistemas.', 4, 1, CURRENT_DATE + INTERVAL 6 DAY, 'pending', 10),
('Trabalho em grupo', 'Pesquisa e apresentação em grupo.', 3, 1, CURRENT_DATE + INTERVAL 8 DAY, 'pending', 10);

INSERT INTO grades (student_id, activity_id, score, feedback) VALUES
(1, 1, 9.0, 'Excelente domínio do conteúdo.'),
(1, 2, 8.5, 'Boa estrutura textual.'),
(1, 3, 8.2, 'Bom relatório.'),
(2, 1, 7.0, 'Revisar funções.'),
(3, 1, 9.5, 'Ótimo trabalho.'),
(4, 1, 8.0, 'Bom desempenho.');

INSERT INTO announcements (title, message, category) VALUES
('Prova de Matemática', 'Avaliação marcada para a próxima sexta-feira às 08:00.', 'Avaliação'),
('Trabalho em grupo', 'Novo grupo criado para a atividade de Física.', 'Atividade'),
('Reunião de Pais', 'Reunião na quarta-feira às 19:00.', 'Escola');

DROP PROCEDURE IF EXISTS sp_list_activities_filtered;
DROP PROCEDURE IF EXISTS sp_student_performance;
DROP PROCEDURE IF EXISTS sp_dashboard_summary;

DELIMITER $$

CREATE PROCEDURE sp_list_activities_filtered(
    IN p_subject_id INT,
    IN p_status VARCHAR(20),
    IN p_search VARCHAR(160),
    IN p_sort_column VARCHAR(30),
    IN p_sort_direction VARCHAR(4)
)
BEGIN
    SET @sort_expr = CASE
        WHEN p_sort_column = 'title' THEN 'a.title'
        WHEN p_sort_column = 'subject_name' THEN 's.name'
        ELSE 'a.due_date'
    END;

    SET @direction = CASE
        WHEN UPPER(p_sort_direction) = 'DESC' THEN 'DESC'
        ELSE 'ASC'
    END;

    SET @sql = CONCAT(
        'SELECT a.id, a.title, a.description, a.subject_id, s.name AS subject_name, ',
        'a.class_id, c.name AS class_name, a.due_date, a.status, a.max_score ',
        'FROM activities a ',
        'INNER JOIN subjects s ON s.id = a.subject_id ',
        'INNER JOIN classes c ON c.id = a.class_id ',
        'WHERE (? IS NULL OR a.subject_id = ?) ',
        'AND (? IS NULL OR a.status = ?) ',
        'AND (? IS NULL OR a.title LIKE CONCAT(''%'', ?, ''%'')) ',
        'ORDER BY ', @sort_expr, ' ', @direction
    );

    PREPARE stmt FROM @sql;
    SET @p1 = p_subject_id;
    SET @p2 = p_subject_id;
    SET @p3 = p_status;
    SET @p4 = p_status;
    SET @p5 = NULLIF(p_search, '');
    SET @p6 = NULLIF(p_search, '');
    EXECUTE stmt USING @p1, @p2, @p3, @p4, @p5, @p6;
    DEALLOCATE PREPARE stmt;
END$$

CREATE PROCEDURE sp_student_performance(IN p_student_id INT)
BEGIN
    SELECT
        s.id AS student_id,
        s.name AS student_name,
        COUNT(g.id) AS activities_completed,
        ROUND(COALESCE(AVG(g.score), 0), 2) AS average_score,
        ROUND(COALESCE(MIN(g.score), 0), 2) AS lowest_score,
        ROUND(COALESCE(MAX(g.score), 0), 2) AS highest_score
    FROM students s
    LEFT JOIN grades g ON g.student_id = s.id
    WHERE s.id = p_student_id
    GROUP BY s.id, s.name;
END$$

CREATE PROCEDURE sp_dashboard_summary(IN p_student_id INT)
BEGIN
    SELECT
        (SELECT COUNT(*) FROM activities a
         INNER JOIN students st ON st.class_id = a.class_id
         WHERE st.id = p_student_id AND a.status = 'pending') AS pending_activities,
        (SELECT COUNT(*) FROM announcements
         WHERE published_at >= CURRENT_TIMESTAMP - INTERVAL 30 DAY) AS recent_announcements,
        (SELECT ROUND(COALESCE(AVG(g.score), 0), 1)
         FROM grades g WHERE g.student_id = p_student_id) AS average_score,
        (SELECT COUNT(*) FROM students st
         WHERE st.class_id = (SELECT class_id FROM students WHERE id = p_student_id)) AS classmates;
END$$

DELIMITER ;
