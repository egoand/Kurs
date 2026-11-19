DROP TABLE IF EXISTS task_assignments CASCADE;
DROP TABLE IF EXISTS task_ratings CASCADE;
DROP TABLE IF EXISTS task_status_history CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS task_statuses CASCADE;
DROP TABLE IF EXISTS staff CASCADE;
DROP TABLE IF EXISTS staff_types CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS ratings CASCADE;

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    code VARCHAR(32) UNIQUE NOT NULL,
    name VARCHAR(128) NOT NULL
);

CREATE TABLE staff_types (
    id SERIAL PRIMARY KEY,
    code VARCHAR(32) UNIQUE NOT NULL,
    name VARCHAR(128) NOT NULL
);

CREATE TABLE task_statuses (
    id SERIAL PRIMARY KEY,
    code VARCHAR(32) UNIQUE NOT NULL,
    name VARCHAR(128) NOT NULL,
    badge VARCHAR(32) NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_archived BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE staff (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) UNIQUE NOT NULL,
    type_id INTEGER NOT NULL REFERENCES staff_types(id),
    position VARCHAR(256) NOT NULL,
    department VARCHAR(256) NOT NULL DEFAULT 'Кафедра прикладной информатики'
);

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    login VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(id),
    staff_id INTEGER REFERENCES staff(id),
    name VARCHAR(128) NOT NULL
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(512) NOT NULL,
    description TEXT DEFAULT '',
    status_id INTEGER NOT NULL REFERENCES task_statuses(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    eval_days INTEGER NOT NULL DEFAULT 3,
    eval_deadline DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    archived_at TIMESTAMP
);

CREATE TABLE task_assignments (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    staff_id INTEGER NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_done BOOLEAN NOT NULL DEFAULT FALSE,
    done_at TIMESTAMP,
    UNIQUE (task_id, staff_id)
);

CREATE TABLE task_ratings (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    staff_id INTEGER NOT NULL REFERENCES staff(id) ON DELETE CASCADE,
    score INTEGER NOT NULL CHECK (score BETWEEN 1 AND 100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (task_id, staff_id)
);

CREATE TABLE task_status_history (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    status_id INTEGER NOT NULL REFERENCES task_statuses(id),
    changed_at TIMESTAMP NOT NULL DEFAULT NOW(),
    changed_by VARCHAR(128)
);

INSERT INTO roles (code, name) VALUES
('zav', 'Заведующий кафедрой'),
('executor', 'Исполнитель');

INSERT INTO staff_types (code, name) VALUES
('teacher', 'Преподаватель'),
('support', 'Учебно-вспомогательный персонал');

INSERT INTO task_statuses (code, name, badge, sort_order, is_archived) VALUES
('pending', 'Ожидает оценки', 'await', 1, FALSE),
('evaluated', 'Оценена', 'eval', 2, FALSE),
('assigned', 'Назначена', 'asg', 3, FALSE),
('in_progress', 'В процессе', 'prog', 4, FALSE),
('completed', 'Выполнена', 'done', 5, FALSE),
('archived', 'Архив', 'arch', 6, TRUE);

INSERT INTO staff (name, type_id, position) VALUES
('Егоров А.Р.', (SELECT id FROM staff_types WHERE code='teacher'), 'д.н., профессор'),
('Зырянов Д.Д.', (SELECT id FROM staff_types WHERE code='support'), 'доцент'),
('Егерь Д.С.', (SELECT id FROM staff_types WHERE code='teacher'), 'преподаватель'),
('Исмагилов Т.Д.', (SELECT id FROM staff_types WHERE code='support'), 'программист'),
('Попельницкий Б.Е.', (SELECT id FROM staff_types WHERE code='support'), 'доцент');

INSERT INTO accounts (login, password, role_id, staff_id, name) VALUES
('zav@kaf', '12345', (SELECT id FROM roles WHERE code='zav'), NULL, 'Заведующий кафедрой'),
('ismagilov@kaf', '12345', (SELECT id FROM roles WHERE code='executor'), (SELECT id FROM staff WHERE name='Исмагилов Т.Д.'), 'Исмагилов Т.Д.'),
('egorov@kaf', '12345', (SELECT id FROM roles WHERE code='executor'), (SELECT id FROM staff WHERE name='Егоров А.Р.'), 'Егоров А.Р.'),
('zyryanov@kaf', '12345', (SELECT id FROM roles WHERE code='executor'), (SELECT id FROM staff WHERE name='Зырянов Д.Д.'), 'Зырянов Д.Д.'),
('popelnitsky@kaf', '12345', (SELECT id FROM roles WHERE code='executor'), (SELECT id FROM staff WHERE name='Попельницкий Б.Е.'), 'Попельницкий Б.Е.'),
('eger@kaf', '12345', (SELECT id FROM roles WHERE code='executor'), (SELECT id FROM staff WHERE name='Егерь Д.С.'), 'Егерь Д.С.');

INSERT INTO tasks (title, description, status_id, start_date, end_date, eval_days, eval_deadline) VALUES
('Разработка рабочих программ по дисциплине «Проектирование информационных систем»',
 'Подготовить рабочие программы и фонды оценочных средств.',
 (SELECT id FROM task_statuses WHERE code='pending'), CURRENT_DATE + 5, CURRENT_DATE + 15, 3, CURRENT_DATE + 2),
('Проверка лабораторных работ по базам данных',
 'Проверить 35 лабораторных работ.',
 (SELECT id FROM task_statuses WHERE code='evaluated'), CURRENT_DATE - 5, CURRENT_DATE + 3, 3, CURRENT_DATE - 8),
('Настройка учебного сервера кафедры',
 'Монтаж и настройка учебного сервера.',
 (SELECT id FROM task_statuses WHERE code='assigned'), CURRENT_DATE + 4, CURRENT_DATE + 14, 3, CURRENT_DATE + 1),
('Обновление сайта кафедры прикладной информатики',
 'Актуализация разделов сайта.',
 (SELECT id FROM task_statuses WHERE code='in_progress'), CURRENT_DATE + 6, CURRENT_DATE + 20, 3, CURRENT_DATE + 3),
('Перенос учебных планов в электронный формат',
 'Перенос учебных планов.',
 (SELECT id FROM task_statuses WHERE code='completed'), CURRENT_DATE - 12, CURRENT_DATE - 2, 3, CURRENT_DATE - 15),
('Отчёты кафедры за 2024 год',
 'Годовые отчёты сданы в архив.',
 (SELECT id FROM task_statuses WHERE code='archived'), CURRENT_DATE - 45, CURRENT_DATE - 30, 3, CURRENT_DATE - 48),
('Интеграция электронного расписания с сайтом кафедры',
 'Синхронизация расписания.',
 (SELECT id FROM task_statuses WHERE code='in_progress'), CURRENT_DATE + 8, CURRENT_DATE + 22, 3, CURRENT_DATE + 5),
('Проверка компьютерного класса кафедры',
 'Аудит рабочих станций.',
 (SELECT id FROM task_statuses WHERE code='assigned'), CURRENT_DATE + 3, CURRENT_DATE + 11, 3, CURRENT_DATE),
('Тестирование учебного портала кафедры',
 'Нагрузочное тестирование.',
 (SELECT id FROM task_statuses WHERE code='evaluated'), CURRENT_DATE - 3, CURRENT_DATE + 5, 3, CURRENT_DATE - 6),
('Плановое обслуживание компьютерного класса',
 'Замена комплектующих.',
 (SELECT id FROM task_statuses WHERE code='completed'), CURRENT_DATE - 18, CURRENT_DATE - 8, 3, CURRENT_DATE - 21),
('Разработка дашборда успеваемости студентов кафедры',
 'Панель мониторинга успеваемости.',
 (SELECT id FROM task_statuses WHERE code='pending'), CURRENT_DATE + 12, CURRENT_DATE + 24, 3, CURRENT_DATE + 9),
('Обновление методических указаний по курсовым работам',
 'Переработать методические указания.',
 (SELECT id FROM task_statuses WHERE code='assigned'), CURRENT_DATE + 5, CURRENT_DATE + 17, 3, CURRENT_DATE + 2),
('Внедрение автоматической проверки студенческих работ',
 'Настройка системы проверки.',
 (SELECT id FROM task_statuses WHERE code='in_progress'), CURRENT_DATE + 7, CURRENT_DATE + 19, 3, CURRENT_DATE + 4),
('Архив методических материалов кафедры',
 'Устаревшие материалы в архиве.',
 (SELECT id FROM task_statuses WHERE code='archived'), CURRENT_DATE - 55, CURRENT_DATE - 38, 3, CURRENT_DATE - 58);

INSERT INTO task_assignments (task_id, staff_id, is_done) VALUES
(3, (SELECT id FROM staff WHERE name='Зырянов Д.Д.'), FALSE),
(4, (SELECT id FROM staff WHERE name='Егерь Д.С.'), FALSE),
(5, (SELECT id FROM staff WHERE name='Попельницкий Б.Е.'), TRUE),
(6, (SELECT id FROM staff WHERE name='Егоров А.Р.'), TRUE),
(6, (SELECT id FROM staff WHERE name='Зырянов Д.Д.'), TRUE),
(7, (SELECT id FROM staff WHERE name='Исмагилов Т.Д.'), FALSE),
(8, (SELECT id FROM staff WHERE name='Зырянов Д.Д.'), FALSE),
(10, (SELECT id FROM staff WHERE name='Зырянов Д.Д.'), TRUE),
(10, (SELECT id FROM staff WHERE name='Попельницкий Б.Е.'), TRUE),
(12, (SELECT id FROM staff WHERE name='Егерь Д.С.'), FALSE),
(13, (SELECT id FROM staff WHERE name='Исмагилов Т.Д.'), FALSE),
(13, (SELECT id FROM staff WHERE name='Попельницкий Б.Е.'), FALSE),
(14, (SELECT id FROM staff WHERE name='Егоров А.Р.'), TRUE),
(14, (SELECT id FROM staff WHERE name='Егерь Д.С.'), TRUE);

INSERT INTO task_ratings (task_id, staff_id, score) VALUES
(2, (SELECT id FROM staff WHERE name='Егоров А.Р.'), 92),
(2, (SELECT id FROM staff WHERE name='Зырянов Д.Д.'), 85),
(2, (SELECT id FROM staff WHERE name='Попельницкий Б.Е.'), 90),
(9, (SELECT id FROM staff WHERE name='Исмагилов Т.Д.'), 88),
(9, (SELECT id FROM staff WHERE name='Егерь Д.С.'), 91);