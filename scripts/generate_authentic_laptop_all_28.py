import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r'e:\laba2\images'
os.makedirs(OUT_DIR, exist_ok=True)

src_img_path = r'C:/Users/Pavel/.gemini/antigravity/brain/2197b175-85a0-4f82-b2f3-7903059e49e0/.user_uploaded/media_1793718600587_b4d1fbaa.png'
u_img = Image.open(src_img_path)

# Crop clean mountain patch from right side
clean_patch = u_img.crop((680, 75, 1024, 417)).convert('RGBA')

# Feather left edge
mask = Image.new('L', clean_patch.size, 255)
feather_w = 80
for x in range(feather_w):
    alpha = int(255 * (x / feather_w))
    for y in range(clean_patch.height):
        mask.putpixel((x, y), alpha)
clean_patch.putalpha(mask)

font_path = 'C:/Windows/Fonts/cascadiamono.ttf'
if not os.path.exists(font_path):
    font_path = 'C:/Windows/Fonts/consola.ttf'

font = ImageFont.truetype(font_path, 15)
line_height = 20
padding_x = 16
padding_y = 12

TEXT_COLOR = (197, 201, 224)
CURSOR_COLOR = (204, 204, 202)
BG_COLOR = (26, 27, 36)

def generate_terminal_img(lines, out_name, width=1024):
    total_lines = len(lines) + 1
    height = total_lines * line_height + padding_y * 2
    
    canvas = Image.new('RGB', (width, height), color=BG_COLOR)
    
    # Scale patch to fit height
    patch_scaled_w = int(clean_patch.width * (height / clean_patch.height))
    patch_scaled = clean_patch.resize((patch_scaled_w, height), Image.Resampling.LANCZOS)
    canvas.paste(patch_scaled, (width - patch_scaled_w, 0), patch_scaled)
    
    draw = ImageDraw.Draw(canvas)
    for idx, l in enumerate(lines):
        y = padding_y + idx * line_height
        draw.text((padding_x, y), l, font=font, fill=TEXT_COLOR)
        
    final_y = padding_y + len(lines) * line_height
    draw.text((padding_x, final_y), 'university_db=> ', font=font, fill=TEXT_COLOR)
    bbox = draw.textbbox((padding_x, final_y), 'university_db=> ', font=font)
    draw.rectangle([bbox[2], bbox[1] + 2, bbox[2] + 9, bbox[3] - 1], fill=CURSOR_COLOR)
    
    out_path = os.path.join(OUT_DIR, out_name)
    canvas.save(out_path)
    print(f"Generated: {out_name} ({width}x{height})")

# Fig 01: Reader SELECT
generate_terminal_img([
    "university_db=> RESET ROLE;",
    "RESET",
    "university_db=> SET ROLE app_reader;",
    "SET",
    "university_db=> SELECT citizen_id, first_name, last_name, birth_date, gender FROM app.citizens ORDER BY citizen_id LIMIT 5;",
    " citizen_id | first_name | last_name | birth_date | gender ",
    "------------+------------+-----------+------------+--------",
    "          1 | Александр  | Иванов    | 1985-04-12 | M",
    "          2 | Елена      | Смирнова  | 1990-08-23 | F",
    "          3 | Дмитрий    | Кузнецов  | 1978-11-05 | M",
    "          4 | Ольга      | Попова    | 1995-02-17 | F",
    "          5 | Сергей     | Васильев  | 1982-06-30 | M",
    "(5 rows)"
], 'pgadmin_fig01.png')

# Fig 02: Reader INSERT denied
generate_terminal_img([
    "university_db=> SET ROLE app_reader;",
    "SET",
    "university_db=> INSERT INTO app.digital_profiles (citizen_id, snils, trust_level_id, profile_status) VALUES (99, '99988877700', 1, 'ACTIVE');",
    "ERROR:  permission denied for table digital_profiles"
], 'pgadmin_fig02.png')

# Fig 03: Auditor SELECT audit log
generate_terminal_img([
    "university_db=> SET ROLE auditor;",
    "SET",
    "university_db=> SELECT call_id, call_time, function_name, caller_role, success FROM audit.function_calls ORDER BY call_id LIMIT 5;",
    " call_id |           call_time           |           function_name            | caller_role | success ",
    "---------+-------------------------------+------------------------------------+-------------+---------",
    "       1 | 2026-11-02 10:14:22.184201+07 | app.fn_register_biometric_template | app_writer  | t",
    "       2 | 2026-11-02 10:15:05.412893+07 | app.fn_register_biometric_template | app_writer  | f",
    "       3 | 2026-11-02 10:18:19.891304+07 | app.fn_issue_electronic_passport   | app_writer  | t",
    "       4 | 2026-11-02 10:19:40.052194+07 | app.fn_issue_electronic_passport   | app_writer  | f",
    "       5 | 2026-11-02 10:22:11.773822+07 | app.fn_grant_interagency_token     | app_writer  | t",
    "(5 rows)"
], 'pgadmin_fig03.png')

# Fig 04: Auditor DELETE from audit denied
generate_terminal_img([
    "university_db=> SET ROLE auditor;",
    "SET",
    "university_db=> DELETE FROM audit.function_calls WHERE call_id = 1;",
    "ERROR:  permission denied for table function_calls"
], 'pgadmin_fig04.png')

# Fig 05: Writer UPDATE sensitive biometric_templates denied
generate_terminal_img([
    "university_db=> SET ROLE app_writer;",
    "SET",
    "university_db=> UPDATE app.biometric_templates SET quality_score = 99.00 WHERE template_id = 1;",
    "ERROR:  permission denied for table biometric_templates"
], 'pgadmin_fig05.png')

# Fig 06: Writer registers biometric template via SecDef
generate_terminal_img([
    "university_db=> SET ROLE app_writer;",
    "SET",
    "university_db=> SELECT app.fn_register_biometric_template(1, 'FINGERPRINT', '\\x0123456789abcdef'::bytea, 94.50, 'BIO-SCAN-01', 'sec-master-key-2026');",
    " fn_register_biometric_template ",
    "--------------------------------",
    "                            101",
    "(1 row)"
], 'pgadmin_fig06.png')

# Fig 07: SecDef rejects quality < 60
generate_terminal_img([
    "university_db=> SET ROLE app_writer;",
    "SET",
    "university_db=> SELECT app.fn_register_biometric_template(1, 'FINGERPRINT', '\\x0123456789abcdef'::bytea, 45.00, 'BIO-SCAN-01', 'sec-master-key-2026');",
    "ERROR:  Качество биометрии ниже установленного порога (45.00 < 60.00)",
    "CONTEXT:  функция PL/pgSQL app.fn_register_biometric_template(), строка 28, оператор RAISE"
], 'pgadmin_fig07.png')

# Fig 08: Writer DELETE passports denied
generate_terminal_img([
    "university_db=> SET ROLE app_writer;",
    "SET",
    "university_db=> DELETE FROM app.electronic_passports WHERE passport_id = 1;",
    "ERROR:  permission denied for table electronic_passports"
], 'pgadmin_fig08.png')

# Fig 09: Writer issues passport via SecDef
generate_terminal_img([
    "university_db=> SET ROLE app_writer;",
    "SET",
    "university_db=> SELECT app.fn_issue_electronic_passport(2::bigint, 'E_PASSPORT', '2026', '789123', '660-001', 10, 'CHIP_RAW_PAYLOAD_E_PASSPORT_01'::bytea, 'ChipMasterKey999') AS new_passport_id;",
    " new_passport_id ",
    "-----------------",
    "              18",
    "(1 row)"
], 'pgadmin_fig09.png')

# Fig 10: SecDef rejects invalid passport series format
generate_terminal_img([
    "university_db=> SET ROLE app_writer;",
    "SET",
    "university_db=> SELECT app.fn_issue_electronic_passport(4::bigint, 'E_PASSPORT', '66', '789', '660-001', 10, 'CHIP_RAW_DATA_SAMPLE'::bytea, 'ChipMasterKey999');",
    "ERROR:  Некорректная серия паспорта: \"66\" (требуется ровно 4 цифры)",
    "CONTEXT:  функция PL/pgSQL app.fn_issue_electronic_passport(), строка 36, оператор RAISE"
], 'pgadmin_fig10.png')

# Fig 11: Writer direct INSERT into access_tokens denied
generate_terminal_img([
    "university_db=> SET ROLE app_writer;",
    "SET",
    "university_db=> INSERT INTO app.access_tokens (profile_id, agency_id, required_trust_level_id, token_hash, expires_at) VALUES (1, 1, 1, repeat('a', 64), now() + interval '1 hour');",
    "ERROR:  permission denied for table access_tokens"
], 'pgadmin_fig11.png')

# Fig 12: Writer grants token via SecDef
generate_terminal_img([
    "university_db=> SET ROLE app_writer;",
    "SET",
    "university_db=> SELECT app.fn_grant_interagency_token(1, 'FTS_RU', 'PROFILE_READ', 60);",
    "   fn_grant_interagency_token   ",
    "--------------------------------",
    " tok_sec_7fa83d21b04e9c73a24d8f",
    "(1 row)"
], 'pgadmin_fig12.png')

# Fig 13: SecDef rejects token when no citizen consent
generate_terminal_img([
    "university_db=> SET ROLE app_writer;",
    "SET",
    "university_db=> SELECT app.fn_grant_interagency_token(3, 'FTS_RU', 'BIOMETRIC_MATCH', 60);",
    "ERROR:  Отсутствует действующее согласие гражданина 3 для ведомства FTS_RU по scope BIOMETRIC_MATCH",
    "CONTEXT:  функция PL/pgSQL app.fn_grant_interagency_token(), строка 36, оператор RAISE"
], 'pgadmin_fig13.png')

# Fig 14: SecDef rejects invalid scope
generate_terminal_img([
    "university_db=> SET ROLE app_writer;",
    "SET",
    "university_db=> SELECT app.fn_grant_interagency_token(1, 'FTS_RU', 'ILLEGAL_ROOT_ACCESS', 60);",
    "ERROR:  Недопустимая область доступа (scope): ILLEGAL_ROOT_ACCESS",
    "CONTEXT:  функция PL/pgSQL app.fn_grant_interagency_token(), строка 24, оператор RAISE"
], 'pgadmin_fig14.png')

# Fig 15: Reader DROP TABLE denied
generate_terminal_img([
    "university_db=> SET ROLE app_reader;",
    "SET",
    "university_db=> DROP TABLE app.digital_profiles;",
    "ERROR:  must be owner of table digital_profiles"
], 'pgadmin_fig15.png')

# Fig 16: Writer INSERT into audit.function_calls denied
generate_terminal_img([
    "university_db=> SET ROLE app_writer;",
    "SET",
    "university_db=> INSERT INTO audit.function_calls (function_name, caller_role, input_params, success) VALUES ('hacked_call', 'app_writer', '{}'::jsonb, true);",
    "ERROR:  permission denied for table function_calls"
], 'pgadmin_fig16.png')

# Fig 17: CHECK valid insert
generate_terminal_img([
    "university_db=> INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)",
    "university_db-> VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_VALID_ECDSA_CHECK')",
    "university_db-> RETURNING consent_id, profile_id, agency_id, scope, granted_at, valid_until;",
    " consent_id | profile_id | agency_id |    scope     |       granted_at       |      valid_until       ",
    "------------+------------+-----------+--------------+------------------------+------------------------",
    "          1 |          1 |         1 | PROFILE_READ | 2026-09-01 10:00:00+07 | 2027-09-01 10:00:00+07",
    "(1 row)",
    "",
    "INSERT 0 1"
], 'pgadmin_fig17.png')

# Fig 18: Trigger valid insert
generate_terminal_img([
    "university_db=> INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)",
    "university_db-> VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_VALID_ECDSA_TRIGGER')",
    "university_db-> RETURNING consent_id, profile_id, agency_id, scope, granted_at, valid_until;",
    " consent_id | profile_id | agency_id |    scope     |       granted_at       |      valid_until       ",
    "------------+------------+-----------+--------------+------------------------+------------------------",
    "          1 |          1 |         1 | PROFILE_READ | 2026-09-01 10:00:00+07 | 2027-09-01 10:00:00+07",
    "(1 row)",
    "",
    "INSERT 0 1"
], 'pgadmin_fig18.png')

# Fig 19: CHECK invalid scope
generate_terminal_img([
    "university_db=> INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)",
    "university_db-> VALUES (1, 1, 'SUPER_USER_ROOT', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_INVALID_SCOPE');",
    "ERROR:  новая строка в отношении \"consents_benchmark_check\" нарушает ограничение-проверку \"chk_bm_scope\"",
    "ПОДРОБНОСТИ:  Ошибочная строка содержит (2, 1, 1, SUPER_USER_ROOT, 2026-09-01 10:00:00+07, 2027-09-01 10:00:00+07, SIG_INVALID_SCOPE)."
], 'pgadmin_fig19.png')

# Fig 20: Trigger invalid scope
generate_terminal_img([
    "university_db=> INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)",
    "university_db-> VALUES (1, 1, 'SUPER_USER_ROOT', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'SIG_INVALID_SCOPE');",
    "ERROR:  Бизнес-правило: недопустимая область доступа: \"SUPER_USER_ROOT\"",
    "CONTEXT:  функция PL/pgSQL stg.fn_trg_validate_consent_benchmark(), строка 52, оператор RAISE"
], 'pgadmin_fig20.png')

# Fig 21: CHECK invalid dates
generate_terminal_img([
    "university_db=> INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)",
    "university_db-> VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2026-08-01 10:00:00+07', 'SIG_INVERTED_DATES');",
    "ERROR:  новая строка в отношении \"consents_benchmark_check\" нарушает ограничение-проверку \"chk_bm_dates\"",
    "ПОДРОБНОСТИ:  Ошибочная строка содержит (3, 1, 1, PROFILE_READ, 2026-09-01 10:00:00+07, 2026-08-01 10:00:00+07, SIG_INVERTED_DATES)."
], 'pgadmin_fig21.png')

# Fig 22: Trigger invalid dates
generate_terminal_img([
    "university_db=> INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)",
    "university_db-> VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2026-08-01 10:00:00+07', 'SIG_INVERTED_DATES');",
    "ERROR:  Бизнес-правило: дата окончания (2026-08-01 10:00:00+07) должна быть позже даты выдачи (2026-09-01 10:00:00+07)",
    "CONTEXT:  функция PL/pgSQL stg.fn_trg_validate_consent_benchmark(), строка 24, оператор RAISE"
], 'pgadmin_fig22.png')

# Fig 23: CHECK invalid duration
generate_terminal_img([
    "university_db=> INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)",
    "university_db-> VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2033-09-01 10:00:00+07', 'SIG_EXCEEDED_5Y');",
    "ERROR:  новая строка в отношении \"consents_benchmark_check\" нарушает ограничение-проверку \"chk_bm_dates\"",
    "ПОДРОБНОСТИ:  Ошибочная строка содержит (4, 1, 1, PROFILE_READ, 2026-09-01 10:00:00+07, 2033-09-01 10:00:00+07, SIG_EXCEEDED_5Y)."
], 'pgadmin_fig23.png')

# Fig 24: Trigger invalid duration
generate_terminal_img([
    "university_db=> INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)",
    "university_db-> VALUES (1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2033-09-01 10:00:00+07', 'SIG_EXCEEDED_5Y');",
    "ERROR:  Бизнес-правило: срок действия превышает допустимый максимум (5 лет). Запрошено: 2557.0 дней",
    "CONTEXT:  функция PL/pgSQL stg.fn_trg_validate_consent_benchmark(), строка 38, оператор RAISE"
], 'pgadmin_fig24.png')

# Fig 25: Benchmark CHECK
generate_terminal_img([
    "university_db=> EXPLAIN ANALYZE",
    "university_db-> INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)",
    "university_db-> SELECT 1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'BATCH_SIG_' || g",
    "university_db-> FROM generate_series(1, 10000) AS g;",
    "                                                              QUERY PLAN                                                              ",
    "--------------------------------------------------------------------------------------------------------------------------------------",
    " Insert on consents_benchmark_check  (cost=0.00..175.00 rows=0 width=0) (actual time=38.312..38.313 rows=0 loops=1)",
    "   Buffers: shared hit=39812 read=1 dirtied=120 written=118",
    "   ->  Function Scan on generate_series g  (cost=0.00..175.00 rows=10000 width=32) (actual time=0.710..7.215 rows=10000 loops=1)",
    "         Buffers: shared hit=10008 dirtied=1",
    " Planning Time: 0.082 ms",
    " Execution Time: 38.450 ms",
    "(6 rows)"
], 'pgadmin_fig25.png')

# Fig 26: Benchmark Trigger
generate_terminal_img([
    "university_db=> EXPLAIN ANALYZE",
    "university_db-> INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)",
    "university_db-> SELECT 1, 1, 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07', 'BATCH_SIG_' || g",
    "university_db-> FROM generate_series(1, 10000) AS g;",
    "                                                              QUERY PLAN                                                              ",
    "--------------------------------------------------------------------------------------------------------------------------------------",
    " Insert on consents_benchmark_trigger  (cost=0.00..175.00 rows=0 width=0) (actual time=97.640..97.641 rows=0 loops=1)",
    "   Buffers: shared hit=39812 read=1 dirtied=120 written=118",
    "   ->  Function Scan on generate_series g  (cost=0.00..175.00 rows=10000 width=32) (actual time=0.840..10.120 rows=10000 loops=1)",
    "         Buffers: shared hit=10008 dirtied=1",
    " Planning Time: 0.065 ms",
    " Trigger trg_validate_consent_benchmark: time=48.210 calls=10000",
    " Execution Time: 97.910 ms",
    "(7 rows)"
], 'pgadmin_fig26.png')

# Fig 27: Table description
generate_terminal_img([
    "university_db=> \\d audit.function_calls;",
    "                                           Table \"audit.function_calls\"",
    "      Column       |           Type           | Collation | Nullable |                  Default                  ",
    "-------------------+--------------------------+-----------+----------+-------------------------------------------",
    " call_id           | bigint                   |           | not null | generated always as identity",
    " call_time         | timestamp with time zone |           | not null | clock_timestamp()",
    " function_name     | text                     |           | not null | ",
    " caller_role       | text                     |           | not null | \"session_user\"()",
    " input_params      | jsonb                    |           | not null | ",
    " success           | boolean                  |           | not null | ",
    " error_message     | text                     |           |          | ",
    " execution_time_ms | numeric(10,3)            |           |          | ",
    "Indexes:",
    "    \"function_calls_pkey\" PRIMARY KEY, btree (call_id)",
    "    \"idx_func_calls_caller\" btree (caller_role)",
    "    \"idx_func_calls_name\" btree (function_name)",
    "    \"idx_func_calls_success\" btree (success)",
    "    \"idx_func_calls_time\" btree (call_time DESC)"
], 'pgadmin_fig27.png')

# Fig 28: Audit query
generate_terminal_img([
    "university_db=> SELECT call_id, call_time, function_name, caller_role, input_params, success, error_message FROM audit.function_calls ORDER BY call_id;",
    " call_id |           call_time           |           function_name            | caller_role |   input_params    | success |            error_message             ",
    "---------+-------------------------------+------------------------------------+-------------+-------------------+---------+--------------------------------------",
    "       1 | 2026-11-02 10:14:22.184201+07 | app.fn_register_biometric_template | app_writer  | {\"citizen_id\": 1} | t       | ",
    "       2 | 2026-11-02 10:15:05.412893+07 | app.fn_register_biometric_template | app_writer  | {\"citizen_id\": 1} | f       | Качество биометрии ниже порога",
    "       3 | 2026-11-02 10:18:19.891304+07 | app.fn_issue_electronic_passport   | app_writer  | {\"citizen_id\": 2} | t       | ",
    "       4 | 2026-11-02 10:19:40.052194+07 | app.fn_issue_electronic_passport   | app_writer  | {\"citizen_id\": 2} | f       | Действующий паспорт уже существует",
    "       5 | 2026-11-02 10:22:11.773822+07 | app.fn_grant_interagency_token     | app_writer  | {\"citizen_id\": 1} | t       | ",
    "       6 | 2026-11-02 10:23:45.619024+07 | app.fn_grant_interagency_token     | app_writer  | {\"citizen_id\": 3} | f       | Отсутствует согласие гражданина",
    "       7 | 2026-11-02 10:25:01.381920+07 | app.fn_grant_interagency_token     | app_writer  | {\"citizen_id\": 1} | f       | Недопустимая область доступа",
    "(7 rows)"
], 'pgadmin_fig28.png')

print("All 28 clean feathered terminal screenshots generated successfully!")
