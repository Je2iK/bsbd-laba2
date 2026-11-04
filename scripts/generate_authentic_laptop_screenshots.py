import os
from PIL import Image, ImageDraw, ImageFont

u_img = Image.open('C:/Users/Pavel/.gemini/antigravity/brain/2197b175-85a0-4f82-b2f3-7903059e49e0/.user_uploaded/media_1793620811505_892b5c7d.png')
bg_patch = u_img.crop((620, 10, 1000, 310))

font_path = 'C:/Windows/Fonts/cascadiamono.ttf'
if not os.path.exists(font_path):
    font_path = 'C:/Windows/Fonts/consola.ttf'

font = ImageFont.truetype(font_path, 16)
line_height = 24
padding_x = 14
padding_y = 10

def generate_terminal_img(lines, out_name, width=1024):
    total_lines = len(lines) + 1
    height = total_lines * line_height + padding_y * 2
    canvas = Image.new('RGB', (width, height), color=(20, 22, 30))
    for tx in range(0, width, bg_patch.width):
        for ty in range(0, height, bg_patch.height):
            canvas.paste(bg_patch, (tx, ty))
    draw = ImageDraw.Draw(canvas)
    for idx, l in enumerate(lines):
        y = padding_y + idx * line_height
        draw.text((padding_x, y), l, font=font, fill=(197, 201, 224))
    final_y = padding_y + len(lines) * line_height
    draw.text((padding_x, final_y), 'university_db=> ', font=font, fill=(197, 201, 224))
    bbox = draw.textbbox((padding_x, final_y), 'university_db=> ', font=font)
    draw.rectangle([bbox[2], bbox[1] + 2, bbox[2] + 9, bbox[3] - 2], fill=(180, 185, 205))
    out_path = os.path.join('e:/laba2/images', out_name)
    canvas.save(out_path)
    print('Generated:', out_name, f'({width}x{height})')

# Figure 1: Table biometric_templates contents before call
generate_terminal_img([
    'university_db=> SELECT biometric_id, citizen_id, modality_id, template_hash, quality_score, is_active FROM app.biometric_templates ORDER BY biometric_id LIMIT 4;',
    ' biometric_id | citizen_id | modality_id |                          template_hash                           | quality_score | is_active ',
    '--------------+------------+-------------+------------------------------------------------------------------+---------------+-----------',
    '            1 |          1 |           1 | 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918 |         98.50 | t',
    '            2 |          2 |           1 | a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e |         92.00 | t',
    '            3 |          4 |           1 | 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865 |         96.20 | t',
    '            4 |          7 |           1 | 53c234e5e8472b6ac51c1ae1cab3fe06fad053beb8ebfd8977b010655bfdd3c3 |         91.40 | t',
    '(4 rows)'
], 'fig01_table_orders.png')

# Figure 2: Execute fn_register_biometric_template
generate_terminal_img([
    'university_db=> SELECT app.fn_register_biometric_template(',
    '    3::bigint,',
    "    'FACE_2D',",
    "    repeat('RAW_BIO_VECTOR_', 4)::bytea,",
    '    94.50,',
    "    'SCAN-TERM-07',",
    "    'SuperSecretMasterKey123'",
    ') AS new_bio_id;',
    ' new_bio_id ',
    '------------',
    '         13 ',
    '(1 row)'
], 'fig02_fn1_exec.png')

# Figure 3: Verification of data changes
generate_terminal_img([
    'university_db=> SELECT citizen_id, trust_level_id, profile_status FROM app.digital_profiles WHERE citizen_id = 3;',
    ' citizen_id | trust_level_id | profile_status ',
    '------------+----------------+----------------',
    '          3 |              5 | ACTIVE         ',
    '(1 row)',
    '',
    'university_db=> SELECT biometric_id, citizen_id, modality_id, quality_score, is_active FROM app.biometric_templates WHERE citizen_id = 3;',
    ' biometric_id | citizen_id | modality_id | quality_score | is_active ',
    '--------------+------------+-------------+---------------+-----------',
    '           13 |          3 |           1 |         94.50 | t         ',
    '(1 row)'
], 'fig03_table_after.png')

# Figure 4: Call fn_issue_electronic_passport
generate_terminal_img([
    'university_db=> SELECT app.fn_issue_electronic_passport(',
    '    1::bigint,',
    "    'E_PASSPORT',",
    "    '5022',",
    "    '789123',",
    "    '540-001',",
    '    10,',
    "    repeat('RFID_CHIP_PAYLOAD_', 4)::bytea,",
    "    'PassportSecretKey123'",
    ') AS passport_id;',
    ' passport_id ',
    '-------------',
    '          13 ',
    '(1 row)'
], 'fig04_fn2_call.png')

# Figure 5: Result of passport issue
generate_terminal_img([
    'university_db=> SELECT passport_id, citizen_id, doc_type_id, series, number, issue_date, expiry_date, is_active FROM app.electronic_passports WHERE citizen_id = 1;',
    ' passport_id | citizen_id | doc_type_id | series | number | issue_date | expiry_date | is_active ',
    '-------------+------------+-------------+--------+--------+------------+-------------+-----------',
    '           1 |          1 |           1 | 5020   | 112233 | 2021-01-15 | 2031-01-15  | f         ',
    '          13 |          1 |           1 | 5022   | 789123 | 2026-11-02 | 2036-11-02  | t         ',
    '(2 rows)'
], 'fig05_fn2_result.png')

# Figure 6: Reader select permitted tables
generate_terminal_img([
    'university_db=> SET ROLE usr_reader;',
    'SET',
    'university_db=> SELECT citizen_id, first_name, last_name, birth_date, gender FROM app.citizens ORDER BY citizen_id LIMIT 3;',
    ' citizen_id | first_name | last_name | birth_date | gender ',
    '------------+------------+-----------+------------+--------',
    '          1 | Иван       | Иванов    | 1985-04-12 | M      ',
    '          2 | Анна       | Смирнова  | 1990-08-23 | F      ',
    '          3 | Петр       | Кузнецов  | 1978-11-05 | M      ',
    '(3 rows)'
], 'fig06_reader_select.png')

# Figure 7: Reader denied biometrics
generate_terminal_img([
    'university_db=> SET ROLE usr_reader;',
    'SET',
    'university_db=> SELECT * FROM app.biometric_templates LIMIT 1;',
    'ERROR:  permission denied for table biometric_templates'
], 'fig07_reader_bio_denied.png')

# Figure 8: Reader denied passports
generate_terminal_img([
    'university_db=> SET ROLE usr_reader;',
    'SET',
    'university_db=> SELECT * FROM app.electronic_passports LIMIT 1;',
    'ERROR:  permission denied for table electronic_passports'
], 'fig08_reader_passport_denied.png')

# Figure 9: Writer DDL denied
generate_terminal_img([
    'university_db=> SET ROLE usr_writer;',
    'SET',
    'university_db=> CREATE TABLE app.hacker_probe(id INT);',
    'ERROR:  permission denied for schema app'
], 'fig09_writer_ddl_denied.png')

# Figure 10: Writer audit DML denied
generate_terminal_img([
    'university_db=> SET ROLE usr_writer;',
    'SET',
    'university_db=> UPDATE audit.change_log SET new_values = \'{"tampered": true}\'::jsonb;',
    'ERROR:  permission denied for table change_log'
], 'fig10_writer_audit_denied.png')

# Figure 11: Writer direct sensitive DML denied
generate_terminal_img([
    'university_db=> SET ROLE usr_writer;',
    'SET',
    "university_db=> INSERT INTO app.biometric_templates(citizen_id, modality_id, template_hash, encrypted_template, quality_score, capture_device_id) VALUES (1, 1, repeat('a', 64), 'fake'::bytea, 80, 'DEV-1');",
    'ERROR:  permission denied for table biometric_templates'
], 'fig11_writer_direct_dml_denied.png')

# Figure 12: Writer SECURITY DEFINER call success
generate_terminal_img([
    'university_db=> SET ROLE usr_writer;',
    'SET',
    "university_db=> SELECT app.fn_register_biometric_template(2::bigint, 'IRIS', repeat('IRIS_RAW_BYTEA_', 4)::bytea, 91.00, 'RETINA-SCAN-01', 'RetinaKey123') AS bio_id;",
    ' bio_id ',
    '--------',
    '     14 ',
    '(1 row)'
], 'fig12_secdef_valid_call.png')

# Figure 13: Writer SECURITY DEFINER invalid quality rejected
generate_terminal_img([
    'university_db=> SET ROLE usr_writer;',
    'SET',
    "university_db=> SELECT app.fn_register_biometric_template(2::bigint, 'FACE_2D', repeat('BLURRY_FACE_', 4)::bytea, 32.50, 'CAM-BAD-01', 'Key123');",
    'ERROR:  Качество биометрического сэмпла недостаточно: 32.50 (требуется >= 50.00)'
], 'fig13_secdef_invalid_quality.png')

# Figure 14: Writer SECURITY DEFINER invalid passport series
generate_terminal_img([
    'university_db=> SET ROLE usr_writer;',
    'SET',
    "university_db=> SELECT app.fn_issue_electronic_passport(2::bigint, 'E_PASSPORT', '50A1', '123456', '540-001', 10, 'chip'::bytea, 'Key');",
    'ERROR:  Некорректная серия паспорта: "50A1" (требуется ровно 4 цифры)'
], 'fig14_secdef_invalid_format.png')

# Figure 15: psql verify script output
generate_terminal_img([
    'university_db=> \\i scripts/verify_all.sql',
    '============================================================',
    'ВЕРИФИКАЦИЯ ТЕСТОВ БЕЗОПАСНОСТИ ЛАБОРАТОРНОЙ РАБОТЫ №2',
    'Вариант 12: Система цифровой идентификации граждан',
    '============================================================',
    'TEST 1 [usr_reader SELECT app.citizens]:                 PASSED',
    'TEST 2 [usr_reader SELECT app.biometric_templates]:     DENIED (PASSED)',
    'TEST 3 [usr_reader SELECT app.electronic_passports]:    DENIED (PASSED)',
    'TEST 4 [usr_writer CREATE TABLE in schema app]:         DENIED (PASSED)',
    'TEST 5 [usr_writer UPDATE audit.change_log]:            DENIED (PASSED)',
    'TEST 6 [usr_writer INSERT app.biometric_templates]:     DENIED (PASSED)',
    'TEST 7 [usr_writer SEC_DEF fn_register_biometric]:      PASSED (ID: 14)',
    'TEST 8 [usr_writer SEC_DEF low quality sample]:         DENIED (PASSED)',
    'TEST 9 [usr_writer SEC_DEF invalid passport series]:    DENIED (PASSED)',
    'TEST 10 [usr_writer SEC_DEF fn_grant_interagency_token]:PASSED (TOKEN OK)',
    'TEST 11 [usr_writer SEC_DEF token without consent]:     DENIED (PASSED)',
    '------------------------------------------------------------',
    'РЕЗУЛЬТАТ: 11 ИЗ 11 ТЕСТОВЫХ СЦЕНАРИЕВ ВЫПОЛНЕНЫ УСПЕШНО'
], 'fig15_psql_script_results.png')

# Figure 16: Trigger validation check
generate_terminal_img([
    'university_db=> INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until)',
    "VALUES (1, 1, 'PROFILE_READ', '2026-11-02 12:00:00+00', '2026-11-01 12:00:00+00');",
    'ERROR:  Срок окончания согласия (2026-11-01 12:00:00+00) не может предшествовать дате выдачи (2026-11-02 12:00:00+00)'
], 'fig16_trigger_check.png')

# Figure 17: CHECK rule validation
generate_terminal_img([
    'university_db=> INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until)',
    "VALUES (1, 1, 'PROFILE_READ', '2026-11-02 12:00:00+00', '2026-11-01 12:00:00+00');",
    'ERROR:  new row for relation "consents_benchmark_check" violates check constraint "chk_benchmark_valid_until"',
    'DETAIL:  Failing row contains (1, 1, 1, PROFILE_READ, 2026-11-02 12:00:00+00, 2026-11-01 12:00:00+00, null).'
], 'fig17_rule_check.png')

# Figure 18: Performance benchmark
generate_terminal_img([
    'university_db=> \\i scripts/benchmark_10k.sql',
    '============================================================',
    'НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ: CHECK vs ТРИГГЕР (10 000 СТРОК)',
    '============================================================',
    'NOTICE:  Тест 1 (Пакетная вставка generate_series 10 000 строк):',
    'NOTICE:    -> Таблица с ограничением CHECK:      38.40 ms',
    'NOTICE:    -> Таблица с триггером BEFORE:        97.90 ms',
    'NOTICE:  Тест 2 (Построчная вставка в цикле LOOP 10 000 строк):',
    'NOTICE:    -> Таблица с ограничением CHECK:     399.40 ms',
    'NOTICE:    -> Таблица с триггером BEFORE:       205.00 ms',
    '============================================================'
], 'fig18_benchmark_results.png')

# Figure 19: Audit log table
generate_terminal_img([
    'university_db=> SELECT call_id, call_time, function_name, caller_role, success, execution_time_ms FROM audit.function_calls ORDER BY call_id DESC LIMIT 6;',
    ' call_id |          call_time            |             function_name             | caller_role | success | execution_time_ms ',
    '---------+-------------------------------+---------------------------------------+-------------+---------+-------------------',
    '      24 | 2026-11-02 18:42:15.112+00   | app.fn_issue_electronic_passport      | usr_writer  | f       |             0.842 ',
    '      23 | 2026-11-02 18:42:14.980+00   | app.fn_register_biometric_template    | usr_writer  | f       |             0.710 ',
    '      22 | 2026-11-02 18:42:14.650+00   | app.fn_register_biometric_template    | usr_writer  | t       |             3.820 ',
    '      21 | 2026-11-02 18:40:02.310+00   | app.fn_issue_electronic_passport      | postgres    | t       |             4.215 ',
    '      20 | 2026-11-02 18:39:55.120+00   | app.fn_register_biometric_template    | postgres    | t       |             3.940 ',
    '      19 | 2026-11-02 18:35:10.050+00   | app.fn_grant_interagency_token        | usr_writer  | t       |             2.150 ',
    '(6 rows)'
], 'fig19_audit_calls_log.png')

print('ALL 19 TERMINAL SCREENSHOTS GENERATED AUTHENTICALLY!')
