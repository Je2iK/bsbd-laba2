# Точные команды для создания скриншотов (28 штук)

Подключение к базе данных в терминале:
```bash
psql -U postgres -p 5433 -h 127.0.0.1 -d university_db
```
*(Пароль: `password`)*

---

## 📸 РАЗДЕЛ 2: Тестирование матрицы прав доступа (Рисунки 1–16)

### Рис. 1 (`pgadmin_fig01.png`)
*Чтение открытых данных граждан ролью `app_reader`*
```sql
RESET ROLE;
SET ROLE app_reader;
SELECT citizen_id, first_name, last_name, birth_date, gender FROM app.citizens ORDER BY citizen_id LIMIT 5;
```

### Рис. 2 (`pgadmin_fig02.png`)
*Запрет прямой вставки (INSERT) в `app.digital_profiles` для роли `app_reader`*
```sql
SET ROLE app_reader;
INSERT INTO app.digital_profiles (citizen_id, snils, trust_level_id, profile_status) VALUES (99, '99988877700', 1, 'ACTIVE');
```

### Рис. 3 (`pgadmin_fig03.png`)
*Просмотр журнала вызовов функций аудитором (`auditor`)*
```sql
SET ROLE auditor;
SELECT call_id, call_time, function_name, caller_role, success FROM audit.function_calls ORDER BY call_id DESC LIMIT 5;
```

### Рис. 4 (`pgadmin_fig04.png`)
*Запрет удаления (DELETE) записей аудита для роли `auditor`*
```sql
SET ROLE auditor;
DELETE FROM audit.function_calls WHERE call_id = 1;
```

### Рис. 5 (`pgadmin_fig05.png`)
*Запрет прямого изменения (UPDATE) биометрических шаблонов для `app_writer`*
```sql
SET ROLE app_writer;
UPDATE app.biometric_templates SET quality_score = 99.00 WHERE template_id = 1;
```

### Рис. 6 (`pgadmin_fig06.png`)
*Успешная регистрация биометрии через SECURITY DEFINER функцию*
```sql
SET ROLE app_writer;
SELECT app.fn_register_biometric_template(3::bigint, 'FACE_2D', repeat('BIO_SAMPLE_DATA_', 4)::bytea, 94.50, 'CAM-TERMINAL-07', 'SuperSecretPass123') AS new_bio_id;
```

### Рис. 7 (`pgadmin_fig07.png`)
*Отказ регистрации биометрии при низком качестве (качество 38.00 < 50.00)*
```sql
SET ROLE app_writer;
SELECT app.fn_register_biometric_template(3::bigint, 'FACE_2D', repeat('BIO_SAMPLE_DATA_', 4)::bytea, 38.00, 'CAM-TERMINAL-07', 'SuperSecretPass123');
```

### Рис. 8 (`pgadmin_fig08.png`)
*Запрет прямого удаления (DELETE) паспортов для `app_writer`*
```sql
SET ROLE app_writer;
DELETE FROM app.electronic_passports WHERE passport_id = 1;
```

### Рис. 9 (`pgadmin_fig09.png`)
*Успешная выдача электронного паспорта через SECURITY DEFINER функцию*
```sql
SET ROLE app_writer;
SELECT app.fn_issue_electronic_passport(4::bigint, 'E_PASSPORT', '6624', '789123', '660-001', 10, 'CHIP_RAW_PAYLOAD_E_PASSPORT_01'::bytea, 'ChipMasterKey999') AS new_passport_id;
```

### Рис. 10 (`pgadmin_fig10.png`)
*Отказ выпуска паспорта при нарушении формата серии (`'66'` вместо 4 цифр)*
```sql
SET ROLE app_writer;
SELECT app.fn_issue_electronic_passport(4::bigint, 'E_PASSPORT', '66', '789', '660-001', 10, 'CHIP_RAW_DATA'::bytea, 'ChipMasterKey999');
```

### Рис. 11 (`pgadmin_fig11.png`)
*Запрет прямой вставки (INSERT) токена в оригинальную `app.access_tokens` для `app_writer`*
```sql
SET ROLE app_writer;
INSERT INTO app.access_tokens (profile_id, agency_id, required_trust_level_id, token_hash, expires_at) VALUES (1, 1, 1, repeat('a', 64), now() + interval '1 hour');
```

### Рис. 12 (`pgadmin_fig12.png`)
*Успешная генерация токена через SECURITY DEFINER функцию (ведомство МВД при активном согласии)*
```sql
SET ROLE app_writer;
SELECT app.fn_grant_interagency_token(1::bigint, 'MVD', 'PROFILE_READ', 24) AS token_hash;
```

### Рис. 13 (`pgadmin_fig13.png`)
*Отказ выдачи токена при отсутствии юридического согласия гражданина (Почта Банк)*
```sql
SET ROLE app_writer;
SELECT app.fn_grant_interagency_token(1::bigint, 'POST_BANK', 'FULL_ACCESS', 12) AS token_hash;
```

### Рис. 14 (`pgadmin_fig14.png`)
*Отказ выдачи токена с недопустимой областью доступа (`ILLEGAL_ROOT_ACCESS`)*
```sql
SET ROLE app_writer;
SELECT app.fn_grant_interagency_token(1::bigint, 'MVD', 'ILLEGAL_ROOT_ACCESS', 24);
```

### Рис. 15 (`pgadmin_fig15.png`)
*Запрет выполнения DDL (`DROP TABLE`) неадминистратором (`app_reader`)*
```sql
SET ROLE app_reader;
DROP TABLE app.digital_profiles;
```

### Рис. 16 (`pgadmin_fig16.png`)
*Запрет ручной вставки/подделки журнала вызовов для `app_writer`*
```sql
SET ROLE app_writer;
INSERT INTO audit.function_calls (function_name, caller_role, input_params, success) VALUES ('hacked_call', 'app_writer', '{}'::jsonb, true);
```

---

## ⚡ РАЗДЕЛ 3: Сравнение CHECK vs Триггер (Рисунки 17–26)

### Рис. 17 (`pgadmin_fig17.png`)
*Успешная вставка валидной строки в таблицу с ограничением CHECK*
```sql
RESET ROLE;
INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_VALID_ECDSA_CHECK')
RETURNING consent_id, profile_id, agency_id, scope, granted_at, valid_until;
```

### Рис. 18 (`pgadmin_fig18.png`)
*Успешная вставка валидной строки в таблицу с триггером BEFORE INSERT*
```sql
INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_VALID_ECDSA_TRIGGER')
RETURNING consent_id, profile_id, agency_id, scope, granted_at, valid_until;
```

### Рис. 19 (`pgadmin_fig19.png`)
*Перехват недопустимого scope ограничением CHECK*
```sql
INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'SUPER_USER_ROOT', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_INVALID_SCOPE');
```

### Рис. 20 (`pgadmin_fig20.png`)
*Перехват недопустимого scope триггером (с понятным текстом ошибки)*
```sql
INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'SUPER_USER_ROOT', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_INVALID_SCOPE');
```

### Рис. 21 (`pgadmin_fig21.png`)
*Перехват некорректного порядка дат (`valid_until < granted_at`) ограничением CHECK*
```sql
INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2026-08-01 10:00:00+07', 'SIG_INVERTED_DATES');
```

### Рис. 22 (`pgadmin_fig22.png`)
*Перехват некорректного порядка дат триггером с выводом точных дат в сообщении*
```sql
INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2026-08-01 10:00:00+07', 'SIG_INVERTED_DATES');
```

### Рис. 23 (`pgadmin_fig23.png`)
*Перехват превышения срока согласия (> 5 лет) ограничением CHECK*
```sql
INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2033-09-01 10:00:00+07', 'SIG_EXCEEDED_5Y');
```

### Рис. 24 (`pgadmin_fig24.png`)
*Перехват превышения срока согласия триггером с выводом числа запрошенных дней*
```sql
INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2033-09-01 10:00:00+07', 'SIG_EXCEEDED_5Y');
```

### Рис. 25 (`pgadmin_fig25.png`)
*Бенчмарк CHECK: замер пакетной вставки 10 000 строк через EXPLAIN ANALYZE*
```sql
EXPLAIN ANALYZE
INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
SELECT 1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'BATCH_SIG_' || g
FROM generate_series(1, 10000) AS g;
```

### Рис. 26 (`pgadmin_fig26.png`)
*Бенчмарк Trigger: замер пакетной вставки 10 000 строк через EXPLAIN ANALYZE*
```sql
EXPLAIN ANALYZE
INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
SELECT 1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'BATCH_SIG_' || g
FROM generate_series(1, 10000) AS g;
```

---

## 📋 РАЗДЕЛ 4: Журнал вызовов функций (Рисунки 27–28)

### Рис. 27 (`pgadmin_fig27.png`)
*Метаданные и структура таблицы аудита `audit.function_calls`*
```sql
\d audit.function_calls;
```

### Рис. 28 (`pgadmin_fig28.png`)
*Выборка журнала вызовов (демонстрация успешных и отклонённых вызовов)*
```sql
SELECT call_id, call_time, function_name, caller_role, input_params, success, error_message FROM audit.function_calls ORDER BY call_id DESC LIMIT 7;
```
