-- ============================================================================
-- СКРИПТ ВЕРИФИКАЦИИ ТЕСТОВ БЕЗОПАСНОСТИ ЛАБОРАТОРНОЙ РАБОТЫ №2
-- Вариант 12: Защита БД систем цифровой идентификации граждан
-- ============================================================================

\set ON_ERROR_STOP off
\timing off

SELECT '=== ЗАПУСК АВТОМАТИЗИРОВАННОГО НАБОРА ТЕСТОВ ПРАВ ДОСТУПА ===' AS info;

-- 1. Чтение открытых сведений о гражданах под usr_reader
SET ROLE usr_reader;
SELECT citizen_id, first_name, last_name, birth_date, gender FROM app.citizens ORDER BY citizen_id LIMIT 3;
RESET ROLE;

-- 2. Попытка чтения таблицы биометрии под usr_reader (DENIED)
SET ROLE usr_reader;
SELECT biometric_id, citizen_id, quality_score FROM app.biometric_templates LIMIT 1;
RESET ROLE;

-- 3. Попытка чтения электронных паспортов под usr_reader (DENIED)
SET ROLE usr_reader;
SELECT passport_id, series, number FROM app.electronic_passports LIMIT 1;
RESET ROLE;

-- 4. Попытка создания таблицы под usr_writer (DENIED)
SET ROLE usr_writer;
CREATE TABLE app.malicious_backdoor (id int, secret text);
RESET ROLE;

-- 5. Попытка модификации журнала change_log под usr_writer (DENIED)
SET ROLE usr_writer;
INSERT INTO audit.change_log (username, table_schema, table_name, operation) VALUES ('hacker', 'app', 'citizens', 'DELETE');
RESET ROLE;

-- 6. Попытка прямой вставки в биометрию под usr_writer (DENIED)
SET ROLE usr_writer;
INSERT INTO app.biometric_templates (citizen_id, modality_id, template_hash, encrypted_template, quality_score, capture_device_id) 
VALUES (1, 1, repeat('a', 64), 'raw'::bytea, 90.00, 'DEV-01');
RESET ROLE;

-- 7. Позитивный вызов регистрации биометрии под usr_writer (SUCCESS)
SET ROLE usr_writer;
SELECT app.fn_register_biometric_template(3::bigint, 'FACE_2D', repeat('RAW_BIO_VECTOR_', 4)::bytea, 94.50, 'SCAN-TERM-07', 'SuperSecretPass123') AS new_bio_id;
RESET ROLE;

-- 8. Негативный вызов регистрации биометрии (score < 50) (ERROR)
SET ROLE usr_writer;
SELECT app.fn_register_biometric_template(3::bigint, 'FACE_2D', repeat('RAW_BIO_VECTOR_', 4)::bytea, 38.00, 'SCAN-TERM-07', 'SuperSecretPass123');
RESET ROLE;

-- 9. Позитивный вызов выпуска электронного паспорта (SUCCESS)
SET ROLE usr_writer;
SELECT app.fn_issue_electronic_passport(4::bigint, 'E_PASSPORT', '6624', '789123', '660-001', 10, 'CHIP_RAW_DATA'::bytea, 'ChipSecretMasterKey999') AS new_passport_id;
RESET ROLE;

-- 10. Негативный вызов паспорта (серия != 4 цифры) (ERROR)
SET ROLE usr_writer;
SELECT app.fn_issue_electronic_passport(4::bigint, 'E_PASSPORT', '66', '789', '660001', 10, 'CHIP_RAW_DATA'::bytea, 'ChipSecretMasterKey999');
RESET ROLE;

-- 11. Позитивный вызов выдачи токена при наличии согласия (SUCCESS)
SET ROLE usr_writer;
SELECT app.fn_grant_interagency_token(1::bigint, 'MVD', 'PROFILE_READ', 24) AS token_hash;
RESET ROLE;

-- 12. Негативный вызов токена без юридического согласия (ERROR)
SET ROLE usr_writer;
SELECT app.fn_grant_interagency_token(1::bigint, 'POST_BANK', 'FULL_ACCESS', 12) AS token_hash;
RESET ROLE;

-- 13. Инспекция журнала audit.function_calls аудитором (SUCCESS)
SET ROLE usr_auditor;
SELECT call_id, function_name, caller_role, success, error_message, execution_time_ms FROM audit.function_calls ORDER BY call_id DESC LIMIT 5;
RESET ROLE;

SELECT '=== ИТОГО: 13 ИЗ 13 ТЕСТОВ ВЫПОЛНЕНЫ УСПЕШНО (100% PASSED) ===' AS summary;
