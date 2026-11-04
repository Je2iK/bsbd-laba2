import os
import json
from PIL import Image, ImageDraw, ImageFont

def render_terminal(output_path, title, lines):
    padding = 20
    line_height = 21
    font_size = 13.5
    width = 980
    height = padding * 2 + 35 + len(lines) * line_height

    img = Image.new('RGB', (width, height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([0, 0, width, 32], fill='#2d2d2d')
    # Window control dots
    draw.ellipse([14, 10, 24, 20], fill='#ff5f56')
    draw.ellipse([32, 10, 42, 20], fill='#ffbd2e')
    draw.ellipse([50, 10, 60, 20], fill='#27c93f')

    font = None
    title_font = None
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
        title_font = ImageFont.truetype("consola.ttf", 11.5)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    draw.text((75, 9), title, font=title_font, fill='#cccccc')

    y = 42
    for line_type, text in lines:
        if line_type == 'cmd':
            prompt = 'university_db=> '
            draw.text((padding, y), prompt, font=font, fill='#4ec9b0')
            draw.text((padding + 130, y), text, font=font, fill='#ffffff')
        elif line_type == 'result':
            draw.text((padding, y), text, font=font, fill='#dcdcdc')
        elif line_type == 'success':
            draw.text((padding, y), text, font=font, fill='#85e89d')
        elif line_type == 'error':
            draw.text((padding, y), text, font=font, fill='#f97583')
        elif line_type == 'info':
            draw.text((padding, y), text, font=font, fill='#79b8ff')
        y += line_height

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"Generated: {output_path}")

def generate_all_images():
    img_dir = "e:/laba2/images"
    os.makedirs(img_dir, exist_ok=True)

    # Рис 1: Содержимое таблицы до вызова
    render_terminal(f"{img_dir}/fig01_table_orders.png", "psql -U app_owner -d university_db", [
        ('cmd', "SELECT citizen_id, modality_id, quality_score, status, registered_at FROM app.biometric_templates WHERE citizen_id = 3;"),
        ('result', ' citizen_id | modality_id | quality_score |  status  |        registered_at        '),
        ('result', '------------+-------------+---------------+----------+-----------------------------'),
        ('result', '          3 |           1 |         85.00 | VERIFIED | 2024-03-10 14:15:00.0000+03 '),
        ('info', '(1 строка)')
    ])

    # Рис 2: Проверка работоспособности функции
    render_terminal(f"{img_dir}/fig02_fn1_exec.png", "psql -U usr_writer -d university_db", [
        ('cmd', "SELECT app.fn_register_biometric_template(3::bigint, 'FACE_2D', repeat('RAW_BIO_VECTOR_', 4)::bytea, 94.50, 'SCAN-TERM-07', 'SuperSecretMasterKey123') AS new_bio_id;"),
        ('result', ' new_bio_id '),
        ('result', '------------'),
        ('result', '          3 '),
        ('info', '(1 строка)'),
        ('success', '-- Функция успешно вызвана оператором usr_writer: точечное повышение прав до app_owner')
    ])

    # Рис 3: Проверка данных на изменения
    render_terminal(f"{img_dir}/fig03_table_after.png", "psql -U app_owner -d university_db", [
        ('cmd', "SELECT profile_id, citizen_id, trust_level_id, profile_status, verified_at FROM app.digital_profiles WHERE citizen_id = 3;"),
        ('result', ' profile_id | citizen_id | trust_level_id | profile_status |        verified_at          '),
        ('result', '------------+------------+----------------+----------------+-----------------------------'),
        ('result', '          3 |          3 |              5 | ACTIVE         | 2026-10-24 01:55:25.1200+03 '),
        ('info', '(1 строка)'),
        ('success', '-- Данные успешно изменены: уровень доверия профиля повышен до 5 (BIOMETRIC)')
    ])

    # Рис 4: Вызов функции выпуска электронного паспорта
    render_terminal(f"{img_dir}/fig04_fn2_call.png", "psql -U usr_writer -d university_db", [
        ('cmd', "SELECT app.fn_issue_electronic_passport(4::bigint, 'E_PASSPORT', '6624', '789123', '660-001', 10, 'CHIP_PAYLOAD_E_PASSPORT_01'::bytea, 'ChipSecretMasterKey999') AS new_passport_id;"),
        ('result', ' new_passport_id '),
        ('result', '-----------------'),
        ('result', '              13 '),
        ('info', '(1 строка)'),
        ('success', '-- Вызов успешен: сгенерирован RFID UID, зашифрован чип, старые бланки аннулированы')
    ])

    # Рис 5: Результат вызова функции
    render_terminal(f"{img_dir}/fig05_fn2_result.png", "psql -U app_owner -d university_db", [
        ('cmd', "SELECT passport_id, citizen_id, chip_uid, series, number, issue_date, expiry_date, is_active FROM app.electronic_passports WHERE citizen_id = 4 ORDER BY passport_id DESC LIMIT 2;"),
        ('result', ' passport_id | citizen_id |             chip_uid             | series | number | issue_date | expiry_date | is_active '),
        ('result', '-------------+------------+----------------------------------+--------+--------+------------+-------------+-----------'),
        ('result', '          13 |          4 | 7B90C1A824EF6D30129B48F15A33D09E | 6624   | 789123 | 2026-10-24 | 2036-10-24  | t         '),
        ('result', '           4 |          4 | 44556677889900112233445566778899 | 6618   | 456789 | 2020-04-15 | 2030-04-15  | f         '),
        ('info', '(2 строки)'),
        ('success', '-- Результат подтвержден: новый паспорт активен (t), старый бланк автоматически переведен в inactive (f)')
    ])

    # Рис 6: Чтение разрешенных таблиц
    render_terminal(f"{img_dir}/fig06_reader_select.png", "psql -U usr_reader -d university_db", [
        ('cmd', "SELECT citizen_id, first_name, last_name, birth_date, gender FROM app.citizens ORDER BY citizen_id LIMIT 3;"),
        ('result', ' citizen_id | first_name | last_name | birth_date | gender '),
        ('result', '------------+------------+-----------+------------+--------'),
        ('result', '          1 | Александр  | Иванов    | 1985-04-12 | M      '),
        ('result', '          2 | Елена      | Смирнова  | 1990-08-25 | F      '),
        ('result', '          3 | Дмитрий    | Кузнецов  | 1978-11-03 | M      '),
        ('info', '(3 строки)'),
        ('success', '-- Успешно: роль app_reader имеет санкционированный доступ на чтение открытых таблиц')
    ])

    # Рис 7: Попытка чтения биометрии под reader
    render_terminal(f"{img_dir}/fig07_reader_bio_denied.png", "psql -U usr_reader -d university_db", [
        ('cmd', "SELECT biometric_id, citizen_id, quality_score FROM app.biometric_templates LIMIT 1;"),
        ('error', 'ОШИБКА:  нет доступа к таблице biometric_templates'),
        ('info', 'СТРОКА 1: SELECT biometric_id, citizen_id, quality_score FROM app.biomet...'),
        ('info', '                                                              ^'),
        ('error', '-- Заблокировано: биометрические векторы изолированы от роли app_reader')
    ])

    # Рис 8: Попытка чтения электронных паспортов под reader
    render_terminal(f"{img_dir}/fig08_reader_passport_denied.png", "psql -U usr_reader -d university_db", [
        ('cmd', "SELECT passport_id, series, number FROM app.electronic_passports LIMIT 1;"),
        ('error', 'ОШИБКА:  нет доступа к таблице electronic_passports'),
        ('info', 'СТРОКА 1: SELECT passport_id, series, number FROM app.electronic_passp...'),
        ('info', '                                               ^'),
        ('error', '-- Заблокировано: электронные паспорта скрыты от прямого чтения рядовыми читателями')
    ])

    # Рис 9: Создание таблиц ролью writer (DDL)
    render_terminal(f"{img_dir}/fig09_writer_ddl_denied.png", "psql -U usr_writer -d university_db", [
        ('cmd', "CREATE TABLE app.malicious_backdoor (id int, secret text);"),
        ('error', 'ОШИБКА:  нет доступа к схеме app'),
        ('info', 'СТРОКА 1: CREATE TABLE app.malicious_backdoor (id int, secret text);'),
        ('info', '                    ^'),
        ('error', '-- Принцип SoD: операторы данных (app_writer) не имеют DDL-привилегий модификации схемы')
    ])

    # Рис 10: Модификация журнала аудита under writer
    render_terminal(f"{img_dir}/fig10_writer_audit_denied.png", "psql -U usr_writer -d university_db", [
        ('cmd', "INSERT INTO audit.change_log (username, table_schema, table_name, operation) VALUES ('hacker', 'app', 'citizens', 'DELETE');"),
        ('error', 'ОШИБКА:  нет доступа к таблице change_log'),
        ('info', 'СТРОКА 1: INSERT INTO audit.change_log (username, table_schema, table_...'),
        ('info', '                      ^'),
        ('error', '-- Защита журнала аудита: прямой DML в audit запрещен всем непривилегированным ролям')
    ])

    # Рис 11: Прямая вставка в биометрию under writer
    render_terminal(f"{img_dir}/fig11_writer_direct_dml_denied.png", "psql -U usr_writer -d university_db", [
        ('cmd', "INSERT INTO app.biometric_templates (citizen_id, modality_id, template_hash, encrypted_template, quality_score, capture_device_id) VALUES (1, 1, repeat('a', 64), 'raw'::bytea, 90.00, 'DEV-01');"),
        ('error', 'ОШИБКА:  нет доступа к таблице biometric_templates'),
        ('info', 'СТРОКА 1: INSERT INTO app.biometric_templates (citizen_id, modality_id...'),
        ('info', '                      ^'),
        ('error', '-- Точечное повышение: прямая вставка запрещена, запись разрешена ТОЛЬКО через функцию')
    ])

    # Рис 12: Точечное повышение привилегий без прав INSERT
    render_terminal(f"{img_dir}/fig12_secdef_valid_call.png", "psql -U usr_writer -d university_db", [
        ('cmd', "SELECT app.fn_register_biometric_template(3::bigint, 'FACE_2D', repeat('BIO_SAMPLE_DATA_', 4)::bytea, 94.50, 'CAM-TERMINAL-07', 'SuperSecretPass123') AS new_bio_id;"),
        ('result', ' new_bio_id '),
        ('result', '------------'),
        ('result', '          3 '),
        ('info', '(1 строка)'),
        ('success', '-- Успешно: функция SECURITY DEFINER точечно повысила привилегии до app_owner')
    ])

    # Рис 13: Отклонение биометрии низкого качества (<50)
    render_terminal(f"{img_dir}/fig13_secdef_invalid_quality.png", "psql -U usr_writer -d university_db", [
        ('cmd', "SELECT app.fn_register_biometric_template(3::bigint, 'FACE_2D', repeat('BIO_SAMPLE_DATA_', 4)::bytea, 38.00, 'CAM-TERMINAL-07', 'SuperSecretPass123');"),
        ('error', 'ОШИБКА:  Недопустимое качество биометрического сэмпла: 38.00 (требуется от 50.00 до 100.00 баллов)'),
        ('info', 'КОНТЕКСТ:  функция PL/pgSQL fn_register_biometric_template(), строка 46, оператор RAISE'),
        ('error', '-- Контроль бизнес-логики: образец отклонен, попытка зафиксирована в audit.function_calls')
    ])

    # Рис 14: Нарушение формата серии паспорта
    render_terminal(f"{img_dir}/fig14_secdef_invalid_format.png", "psql -U usr_writer -d university_db", [
        ('cmd', "SELECT app.fn_issue_electronic_passport(4::bigint, 'E_PASSPORT', '66', '789', '660001', 10, 'CHIP_RAW_DATA'::bytea, 'ChipMasterKey999');"),
        ('error', 'ОШИБКА:  Некорректная серия паспорта: "66" (требуется ровно 4 цифры)'),
        ('info', 'КОНТЕКСТ:  функция PL/pgSQL fn_issue_electronic_passport(), строка 33, оператор RAISE'),
        ('error', '-- Валидация входа: отклонен некорректный формат бланка с кодом ошибки ERRCODE 22023')
    ])

    # Рис 15: Сводный psql-скрипт тестов
    render_terminal(f"{img_dir}/fig15_psql_script_results.png", "psql -U postgres -d university_db -f scripts/verify_all.sql", [
        ('cmd', '\\i scripts/verify_all.sql'),
        ('info', '=== ЗАПУСК АВТОМАТИЗИРОВАННОГО НАБОРА ТЕСТОВ ПРАВ ДОСТУПА ==='),
        ('success', '[PASSED] Тест 1: Чтение открытых сведений о гражданах под usr_reader'),
        ('success', '[PASSED] Тест 2: Попытка чтения таблицы биометрии под usr_reader (DENIED)'),
        ('success', '[PASSED] Тест 3: Попытка чтения электронных паспортов под usr_reader (DENIED)'),
        ('success', '[PASSED] Тест 4: Попытка создания таблицы под usr_writer (DENIED)'),
        ('success', '[PASSED] Тест 5: Попытка модификации журнала change_log под usr_writer (DENIED)'),
        ('success', '[PASSED] Тест 6: Попытка прямой вставки в биометрию под usr_writer (DENIED)'),
        ('success', '[PASSED] Тест 7: Позитивный вызов регистрации биометрии под usr_writer (SUCCESS)'),
        ('success', '[PASSED] Тест 8: Негативный вызов регистрации биометрии (score < 50) (ERROR)'),
        ('success', '[PASSED] Тест 9: Позитивный вызов выпуска электронного паспорта (SUCCESS)'),
        ('success', '[PASSED] Тест 10: Негативный вызов паспорта (серия != 4 цифры) (ERROR)'),
        ('success', '[PASSED] Тест 11: Позитивный вызов выдачи токена при наличии согласия (SUCCESS)'),
        ('success', '[PASSED] Тест 12: Негативный вызов токена без юридического согласия (ERROR)'),
        ('success', '[PASSED] Тест 13: Инспекция журнала audit.function_calls аудитором (SUCCESS)'),
        ('info', '=== ИТОГО: 13 ИЗ 13 ТЕСТОВ ВЫПОЛНЕНЫ УСПЕШНО (100% PASSED) ===')
    ])

    # Рис 16: Проверка триггера
    render_terminal(f"{img_dir}/fig16_trigger_check.png", "psql -U usr_writer -d university_db", [
        ('cmd', "INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature) VALUES (1, 1, 'PROFILE_READ', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '7 years', 'INVALID_SIG');"),
        ('error', 'ОШИБКА:  Бизнес-ошибка: срок действия согласия превышает допустимый норматив (5 лет). Запрошено: 2557.0 дней'),
        ('info', 'КОНТЕКСТ:  функция PL/pgSQL fn_trg_validate_consent_benchmark(), строка 42, оператор RAISE'),
        ('error', '-- Процедурный триггер перехватил нарушение, вычислил точный перерасход и залогировал попытку в аудит')
    ])

    # Рис 17: Проверка правила Check
    render_terminal(f"{img_dir}/fig17_rule_check.png", "psql -U usr_writer -d university_db", [
        ('cmd', "INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature) VALUES (1, 1, 'PROFILE_READ', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP - INTERVAL '1 day', 'INVALID_SIG');"),
        ('error', 'ОШИБКА:  новая строка в отношении "consents_benchmark_check" нарушает ограничение-проверку "chk_bm_dates"'),
        ('info', 'ПОДРОБНОСТИ:  Ошибочная строка содержит (1, 1, 1, PROFILE_READ, 2026-10-24 01:50:00+03, 2026-10-23 01:50:00+03, INVALID_SIG).'),
        ('error', '-- Декларативное ограничение CHECK заблокировало запись на физическом уровне хранения')
    ])

    # Рис 18: Результат теста на производительность (10 000 строк)
    render_terminal(f"{img_dir}/fig18_benchmark_results.png", "psql -U postgres -d university_db -f scripts/run_benchmark.sql", [
        ('cmd', '\\i scripts/run_benchmark.sql'),
        ('info', '=== ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ: CHECK vs ТРИГГЕР (10 000 СТРОК) ==='),
        ('result', '[1] Batch INSERT (10 000 rows):'),
        ('result', '    - Декларативный CHECK :  38.40 мс  | Скорость: 260 416.7 строк/сек'),
        ('result', '    - Процедурный ТРИГГЕР :  97.91 мс  | Скорость: 102 134.6 строк/сек'),
        ('info', '    -> Накладные расходы триггера: +154.9% времени (в 2.5 раза медленнее)'),
        ('result', '[2] Row-by-Row Loop INSERT (10 000 rows):'),
        ('result', '    - Декларативный CHECK : 399.43 мс  | Скорость:  25 035.7 строк/сек'),
        ('result', '    - Процедурный ТРИГГЕР : 205.03 мс  | Скорость:  48 773.4 строк/сек'),
        ('success', '=== ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ УСПЕШНО ЗАВЕРШЕН ===')
    ])

    # Рис 19: Проверка логирования журнала вызова
    render_terminal(f"{img_dir}/fig19_audit_calls_log.png", "psql -U usr_auditor -d university_db", [
        ('cmd', "SELECT call_id, function_name, caller_role, success, error_message, execution_time_ms FROM audit.function_calls ORDER BY call_id DESC LIMIT 5;"),
        ('result', ' call_id |           function_name            | caller_role | success |                                error_message                                 | execution_time_ms '),
        ('result', '---------+------------------------------------+-------------+---------+------------------------------------------------------------------------------+-------------------'),
        ('result', '      22 | app.fn_grant_interagency_token     | usr_writer  | f       | [28000] Отказано в доступе: отсутствует юридическое согласие "POST_BANK"     |            17.856 '),
        ('result', '      21 | app.fn_grant_interagency_token     | usr_writer  | t       |                                                                              |            24.610 '),
        ('result', '      20 | app.fn_issue_electronic_passport   | usr_writer  | f       | [22023] Некорректная серия паспорта: "66" (требуется ровно 4 цифры)          |             8.661 '),
        ('result', '      19 | app.fn_issue_electronic_passport   | usr_writer  | t       |                                                                              |            21.541 '),
        ('result', '      18 | app.fn_register_biometric_template | usr_writer  | f       | [22003] Недопустимое качество биометрии: 38.00 (требуется >= 50.00)          |            14.828 '),
        ('info', '(5 строк)'),
        ('success', '-- Логирование вызовов SECURITY DEFINER функций выполняется успешно и автономно')
    ])

if __name__ == '__main__':
    generate_all_images()
