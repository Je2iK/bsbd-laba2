# Команды для создания скриншотов (28 штук)

Все команды выполняются в интерактивном терминале **`psql`** (или в окне Query Tool pgAdmin) при подключении к базе данных:
```bash
psql -U postgres -p 5433 -h 127.0.0.1 -d university_db
```
*(Пароль для пользователя `postgres`: **`password`**, порт: **`5433`**)*

---

## 📸 Раздел 2: Тестирование матрицы прав доступа (Рисунки 1–16)

### Рисунок 1 (`pgadmin_fig01.png`)
*Чтение открытых данных гражданина под ролью `app_reader`*
```sql
RESET ROLE;
SET ROLE app_reader;
SELECT citizen_id, first_name, last_name, birth_date, gender FROM app.citizens ORDER BY citizen_id LIMIT 5;
```

### Рисунок 2 (`pgadmin_fig02.png`)
*Запрет прямой вставки (INSERT) в защищённую таблицу `app.digital_profiles` под ролью `app_reader`*
```sql
SET ROLE app_reader;
INSERT INTO app.digital_profiles (citizen_id, snils, trust_level_id, profile_status) VALUES (99, '99988877700', 1, 'ACTIVE');
```

### Рисунок 3 (`pgadmin_fig03.png`)
*Чтение журнала аудита под ролью `auditor`*
```sql
SET ROLE auditor;
SELECT call_id, call_time, function_name, caller_role, success FROM audit.function_calls ORDER BY call_id LIMIT 5;
```

### Рисунок 4 (`pgadmin_fig04.png`)
*Запрет модификации/удаления (DELETE) записей аудита под ролью `auditor`*
```sql
SET ROLE auditor;
DELETE FROM audit.function_calls WHERE call_id = 1;
```

### Рисунок 5 (`pgadmin_fig05.png`)
*Запрет прямого изменения (UPDATE) таблицы `app.biometric_templates` под ролью `app_writer`*
```sql
SET ROLE app_writer;
UPDATE app.biometric_templates SET quality_score = 99.00 WHERE template_id = 1;
```

### Рисунок 6 (`pgadmin_fig06.png`)
*Успешная регистрация биометрического шаблона через SECURITY DEFINER функцию `fn_register_biometric_template`*
```sql
SET ROLE app_writer;
SELECT app.fn_register_biometric_template(1, 'FINGERPRINT', '\x0123456789abcdef'::bytea, 94.50, 'BIO-SCAN-01', 'sec-master-key-2026');
```

### Рисунок 7 (`pgadmin_fig07.png`)
*Отказ регистрации биометрии с недостаточным качеством (quality < 60)*
```sql
SET ROLE app_writer;
SELECT app.fn_register_biometric_template(1, 'FINGERPRINT', '\x0123456789abcdef'::bytea, 45.00, 'BIO-SCAN-01', 'sec-master-key-2026');
```

### Рисунок 8 (`pgadmin_fig08.png`)
*Запрет прямого удаления (DELETE) паспортов из таблицы `app.electronic_passports` под ролью `app_writer`*
```sql
SET ROLE app_writer;
DELETE FROM app.electronic_passports WHERE passport_id = 1;
```

### Рисунок 9 (`pgadmin_fig09.png`)
*Успешная выдача электронного паспорта через SECURITY DEFINER функцию `fn_issue_electronic_passport`*
```sql
SET ROLE app_writer;
SELECT app.fn_issue_electronic_passport(2, '2026', '123456', 'CHIP-RU-9921', 'MVD-770-001', '2026-01-01', '2036-01-01');
```

### Рисунок 10 (`pgadmin_fig10.png`)
*Блокировка повторной выдачи паспорта при наличии действующего документа*
```sql
SET ROLE app_writer;
SELECT app.fn_issue_electronic_passport(2, '2026', '999999', 'CHIP-RU-9922', 'MVD-770-001', '2026-01-01', '2036-01-01');
```

### Рисунок 11 (`pgadmin_fig11.png`)
*Запрет прямой вставки (INSERT) токена в `app.interagency_tokens` под ролью `app_writer`*
```sql
SET ROLE app_writer;
INSERT INTO app.interagency_tokens (citizen_id, agency_id, token_hash, scope, expires_at) VALUES (1, 1, 'hash_sample_val', 'PROFILE_READ', now() + interval '1 hour');
```

### Рисунок 12 (`pgadmin_fig12.png`)
*Успешная генерация межведомственного токена через SECURITY DEFINER функцию `fn_grant_interagency_token`*
```sql
SET ROLE app_writer;
SELECT app.fn_grant_interagency_token(1, 'FTS_RU', 'PROFILE_READ', 60);
```

### Рисунок 13 (`pgadmin_fig13.png`)
*Отказ генерации токена при отсутствии активного согласия гражданина*
```sql
SET ROLE app_writer;
SELECT app.fn_grant_interagency_token(3, 'FTS_RU', 'BIOMETRIC_MATCH', 60);
```

### Рисунок 14 (`pgadmin_fig14.png`)
*Отказ генерации токена с недопустимой областью доступа (scope)*
```sql
SET ROLE app_writer;
SELECT app.fn_grant_interagency_token(1, 'FTS_RU', 'ILLEGAL_ROOT_ACCESS', 60);
```

### Рисунок 15 (`pgadmin_fig15.png`)
*Запрет DDL-операций (DROP TABLE) неадминистратором под ролью `app_reader`*
```sql
SET ROLE app_reader;
DROP TABLE app.digital_profiles;
```

### Рисунок 16 (`pgadmin_fig16.png`)
*Запрет прямой подделки журнала аудита (INSERT) ролью `app_writer`*
```sql
SET ROLE app_writer;
INSERT INTO audit.function_calls (function_name, caller_role, input_params, success) VALUES ('hacked_call', 'app_writer', '{}'::jsonb, true);
```

---

## ⚡ Раздел 3: Сравнение CHECK vs Триггер (Рисунки 17–26)

### Рисунок 17 (`pgadmin_fig17.png`)
*Успешная вставка валидной строки в таблицу с ограничением CHECK*
```sql
RESET ROLE;
INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_VALID_ECDSA_CHECK')
RETURNING consent_id, profile_id, agency_id, scope, granted_at, valid_until;
```

### Рисунок 18 (`pgadmin_fig18.png`)
*Успешная вставка валидной строки в таблицу с триггером BEFORE INSERT*
```sql
INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_VALID_ECDSA_TRIGGER')
RETURNING consent_id, profile_id, agency_id, scope, granted_at, valid_until;
```

### Рисунок 19 (`pgadmin_fig19.png`)
*Перехват недопустимого scope ограничением CHECK*
```sql
INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'SUPER_USER_ROOT', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_INVALID_SCOPE');
```

### Рисунок 20 (`pgadmin_fig20.png`)
*Перехват недопустимого scope триггером (с понятным сообщением)*
```sql
INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'SUPER_USER_ROOT', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_INVALID_SCOPE');
```

### Рисунок 21 (`pgadmin_fig21.png`)
*Перехват некорректного порядка дат (valid_until < granted_at) ограничением CHECK*
```sql
INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2026-08-01 10:00:00+07', 'SIG_INVERTED_DATES');
```

### Рисунок 22 (`pgadmin_fig22.png`)
*Перехват некорректного порядка дат триггером с выводом точных дат*
```sql
INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2026-08-01 10:00:00+07', 'SIG_INVERTED_DATES');
```

### Рисунок 23 (`pgadmin_fig23.png`)
*Перехват превышения допустимого срока (> 5 лет) ограничением CHECK*
```sql
INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2033-09-01 10:00:00+07', 'SIG_EXCEEDED_5Y');
```

### Рисунок 24 (`pgadmin_fig24.png`)
*Перехват превышения срока триггером с выводом числа запрошенных дней*
```sql
INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2033-09-01 10:00:00+07', 'SIG_EXCEEDED_5Y');
```

### Рисунок 25 (`pgadmin_fig25.png`)
*Замер производительности: пакетная вставка 10 000 строк в таблицу с CHECK (EXPLAIN ANALYZE)*
```sql
EXPLAIN ANALYZE
INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
SELECT 1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'BATCH_SIG_' || g
FROM generate_series(1, 10000) AS g;
```

### Рисунок 26 (`pgadmin_fig26.png`)
*Замер производительности: пакетная вставка 10 000 строк в таблицу с триггером (EXPLAIN ANALYZE)*
```sql
EXPLAIN ANALYZE
INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
SELECT 1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'BATCH_SIG_' || g
FROM generate_series(1, 10000) AS g;
```

---

## 📋 Раздел 4: Журнал вызовов функций (Рисунки 27–28)

### Рисунок 27 (`pgadmin_fig27.png`)
*Структура и метаданные таблицы `audit.function_calls`*
```sql
\d audit.function_calls;
```

### Рисунок 28 (`pgadmin_fig28.png`)
*Выборка журнала аудита вызовов SECURITY DEFINER функций (успешные и отклонённые вызовы)*
```sql
SELECT call_id, call_time, function_name, caller_role, input_params, success, error_message FROM audit.function_calls ORDER BY call_id;
```
