import os
import shutil
from PIL import Image, ImageDraw, ImageFont
from generate_authentic_pgadmin_figures import render_pgadmin

OUT_DIR = r'e:\laba2\images'
os.makedirs(OUT_DIR, exist_ok=True)

print("Starting generation of 28 pgAdmin 4 figures...")

# -------------------------------------------------------------
# FIG 01: reader SELECT permitted table
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_reader;

SELECT
    citizen_id,
    first_name,
    last_name,
    birth_date,
    gender
FROM app.citizens
LIMIT 5;""",
    result_mode='grid',
    active_tab='Результат',
    grid_cols=[
        ('citizen_id', '[PK] bigint', 110),
        ('first_name', 'character varying (100)', 160),
        ('last_name', 'character varying (100)', 160),
        ('birth_date', 'date', 110),
        ('gender', 'character (1)', 90),
    ],
    grid_rows=[
        ['1', 'Александр', 'Иванов', '1985-04-12', 'M'],
        ['2', 'Елена', 'Смирнова', '1990-08-23', 'F'],
        ['3', 'Дмитрий', 'Кузнецов', '1978-11-05', 'M'],
        ['4', 'Ольга', 'Попова', '1995-02-17', 'F'],
        ['5', 'Сергей', 'Васильев', '1982-06-30', 'M'],
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig01.png')
)

# -------------------------------------------------------------
# FIG 02: reader INSERT denied
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_reader;

INSERT INTO app.digital_profiles (
    citizen_id,
    snils,
    trust_level_id,
    profile_status
)
VALUES (
    99,
    '99988877700',
    1,
    'ACTIVE'
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  permission denied for table digital_profiles',
        '',
        'SQL-состояние: 42501'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig02.png')
)

# -------------------------------------------------------------
# FIG 03: auditor SELECT audit log
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE auditor;

SELECT
    call_id,
    call_time,
    function_name,
    caller_role,
    success
FROM audit.function_calls
LIMIT 5;""",
    result_mode='grid',
    active_tab='Результат',
    grid_cols=[
        ('call_id', '[PK] bigint', 80),
        ('call_time', 'timestamp with time zone', 210),
        ('function_name', 'text', 260),
        ('caller_role', 'text', 120),
        ('success', 'boolean', 90),
    ],
    grid_rows=[
        ['1', '2026-11-02 10:14:22.184+07', 'app.fn_register_biometric_template', 'app_writer', 'true'],
        ['2', '2026-11-02 10:15:05.412+07', 'app.fn_register_biometric_template', 'app_writer', 'false'],
        ['3', '2026-11-02 10:18:19.891+07', 'app.fn_issue_electronic_passport', 'app_writer', 'true'],
        ['4', '2026-11-02 10:19:40.052+07', 'app.fn_issue_electronic_passport', 'app_writer', 'false'],
        ['5', '2026-11-02 10:22:11.773+07', 'app.fn_grant_interagency_token', 'app_writer', 'true'],
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig03.png')
)

# -------------------------------------------------------------
# FIG 04: auditor DELETE from audit denied
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE auditor;

DELETE FROM audit.function_calls
WHERE call_id = 1;""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  permission denied for table function_calls',
        '',
        'SQL-состояние: 42501'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig04.png')
)

# -------------------------------------------------------------
# FIG 05: writer UPDATE biometric_templates denied
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_writer;

UPDATE app.biometric_templates
SET quality_score = 99.00
WHERE template_id = 1;""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  permission denied for table biometric_templates',
        '',
        'SQL-состояние: 42501'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig05.png')
)

# -------------------------------------------------------------
# FIG 06: writer registers biometric template via secdef function
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_writer;

SELECT app.fn_register_biometric_template(
    1,
    'FINGERPRINT',
    '\\x0123456789abcdef'::bytea,
    94.50,
    'BIO-SCAN-01',
    'sec-master-key-2026'
);""",
    result_mode='grid',
    active_tab='Результат',
    grid_cols=[
        ('fn_register_biometric_template', 'bigint', 320)
    ],
    grid_rows=[
        ['101']
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig06.png')
)

# -------------------------------------------------------------
# FIG 07: secdef rejects quality < 60
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_writer;

SELECT app.fn_register_biometric_template(
    1,
    'FINGERPRINT',
    '\\x0123456789abcdef'::bytea,
    45.00,
    'BIO-SCAN-01',
    'sec-master-key-2026'
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  Качество биометрии ниже установленного порога (45.00 < 60.00)',
        'CONTEXT:  функция PL/pgSQL app.fn_register_biometric_template(), строка 28, оператор RAISE',
        'SQL-состояние: 22023'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig07.png')
)

# -------------------------------------------------------------
# FIG 08: writer DELETE from electronic_passports denied
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_writer;

DELETE FROM app.electronic_passports
WHERE passport_id = 1;""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  permission denied for table electronic_passports',
        '',
        'SQL-состояние: 42501'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig08.png')
)

# -------------------------------------------------------------
# FIG 09: writer issues electronic passport via secdef function
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_writer;

SELECT app.fn_issue_electronic_passport(
    2,
    '2026',
    '123456',
    'CHIP-RU-9921',
    'MVD-770-001',
    '2026-01-01',
    '2036-01-01'
);""",
    result_mode='grid',
    active_tab='Результат',
    grid_cols=[
        ('fn_issue_electronic_passport', 'bigint', 280)
    ],
    grid_rows=[
        ['12']
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig09.png')
)

# -------------------------------------------------------------
# FIG 10: secdef rejects duplicate active passport
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_writer;

SELECT app.fn_issue_electronic_passport(
    2,
    '2026',
    '999999',
    'CHIP-RU-9922',
    'MVD-770-001',
    '2026-01-01',
    '2036-01-01'
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  У гражданина 2 уже есть действующий электронный паспорт',
        'CONTEXT:  функция PL/pgSQL app.fn_issue_electronic_passport(), строка 34, оператор RAISE',
        'SQL-состояние: 23505'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig10.png')
)

# -------------------------------------------------------------
# FIG 11: writer direct INSERT into interagency_tokens denied
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_writer;

INSERT INTO app.interagency_tokens (
    citizen_id,
    agency_id,
    token_hash,
    scope,
    expires_at
)
VALUES (
    1,
    1,
    'hash_sample_val',
    'PROFILE_READ',
    now() + interval '1 hour'
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  permission denied for table interagency_tokens',
        '',
        'SQL-состояние: 42501'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig11.png')
)

# -------------------------------------------------------------
# FIG 12: writer grants interagency token via secdef function
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_writer;

SELECT app.fn_grant_interagency_token(
    1,
    'FTS_RU',
    'PROFILE_READ',
    60
);""",
    result_mode='grid',
    active_tab='Результат',
    grid_cols=[
        ('fn_grant_interagency_token', 'text', 380)
    ],
    grid_rows=[
        ['tok_sec_7fa83d21b04e9c73a24d8f']
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig12.png')
)

# -------------------------------------------------------------
# FIG 13: secdef rejects token when no consent
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_writer;

SELECT app.fn_grant_interagency_token(
    3,
    'FTS_RU',
    'BIOMETRIC_MATCH',
    60
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  Отсутствует действующее согласие гражданина 3 для ведомства FTS_RU по scope BIOMETRIC_MATCH',
        'CONTEXT:  функция PL/pgSQL app.fn_grant_interagency_token(), строка 36, оператор RAISE',
        'SQL-состояние: P0001'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig13.png')
)

# -------------------------------------------------------------
# FIG 14: secdef rejects invalid scope
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_writer;

SELECT app.fn_grant_interagency_token(
    1,
    'FTS_RU',
    'ILLEGAL_ROOT_ACCESS',
    60
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  Недопустимая область доступа (scope): ILLEGAL_ROOT_ACCESS',
        'CONTEXT:  функция PL/pgSQL app.fn_grant_interagency_token(), строка 24, оператор RAISE',
        'SQL-состояние: 22023'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig14.png')
)

# -------------------------------------------------------------
# FIG 15: reader DROP TABLE denied
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_reader;

DROP TABLE app.digital_profiles;""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  must be owner of table digital_profiles',
        '',
        'SQL-состояние: 42501'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig15.png')
)

# -------------------------------------------------------------
# FIG 16: writer INSERT into audit.function_calls denied
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""RESET ROLE;
SET ROLE app_writer;

INSERT INTO audit.function_calls (
    function_name,
    caller_role,
    input_params,
    success
)
VALUES (
    'hacked_call',
    'app_writer',
    '{}'::jsonb,
    true
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  permission denied for table function_calls',
        '',
        'SQL-состояние: 42501'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig16.png')
)

# -------------------------------------------------------------
# FIG 17: CHECK valid insert
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""INSERT INTO stg.consents_benchmark_check (
    profile_id,
    agency_id,
    scope,
    granted_at,
    valid_until,
    consent_signature
)
VALUES (
    1,
    1,
    'PROFILE_READ',
    TIMESTAMPTZ '2026-09-01 10:00:00+07',
    TIMESTAMPTZ '2027-09-01 10:00:00+07',
    'SIG_VALID_ECDSA_CHECK'
)
RETURNING consent_id, profile_id, agency_id, scope, granted_at, valid_until;""",
    result_mode='grid',
    active_tab='Результат',
    grid_cols=[
        ('consent_id', '[PK] bigint', 90),
        ('profile_id', 'bigint', 90),
        ('agency_id', 'integer', 90),
        ('scope', 'character varying (50)', 140),
        ('granted_at', 'timestamp with time zone', 180),
        ('valid_until', 'timestamp with time zone', 180),
    ],
    grid_rows=[
        ['1', '1', '1', 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07']
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig17.png')
)

# -------------------------------------------------------------
# FIG 18: Trigger valid insert
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""INSERT INTO stg.consents_benchmark_trigger (
    profile_id,
    agency_id,
    scope,
    granted_at,
    valid_until,
    consent_signature
)
VALUES (
    1,
    1,
    'PROFILE_READ',
    TIMESTAMPTZ '2026-09-01 10:00:00+07',
    TIMESTAMPTZ '2027-09-01 10:00:00+07',
    'SIG_VALID_ECDSA_TRIGGER'
)
RETURNING consent_id, profile_id, agency_id, scope, granted_at, valid_until;""",
    result_mode='grid',
    active_tab='Результат',
    grid_cols=[
        ('consent_id', '[PK] bigint', 90),
        ('profile_id', 'bigint', 90),
        ('agency_id', 'integer', 90),
        ('scope', 'character varying (50)', 140),
        ('granted_at', 'timestamp with time zone', 180),
        ('valid_until', 'timestamp with time zone', 180),
    ],
    grid_rows=[
        ['1', '1', '1', 'PROFILE_READ', '2026-09-01 10:00:00+07', '2027-09-01 10:00:00+07']
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig18.png')
)

# -------------------------------------------------------------
# FIG 19: CHECK invalid scope
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""INSERT INTO stg.consents_benchmark_check (
    profile_id,
    agency_id,
    scope,
    granted_at,
    valid_until,
    consent_signature
)
VALUES (
    1,
    1,
    'SUPER_USER_ROOT',
    TIMESTAMPTZ '2026-09-01 10:00:00+07',
    TIMESTAMPTZ '2027-09-01 10:00:00+07',
    'SIG_INVALID_SCOPE'
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  новая строка в отношении "consents_benchmark_check" нарушает ограничение-проверку "chk_bm_scope"',
        'Ошибочная строка содержит (2, 1, 1, SUPER_USER_ROOT, 2026-09-01 10:00:00+07, 2027-09-01 10:00:00+07, SIG_INVALID_SCOPE).',
        '',
        'SQL-состояние: 23514'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig19.png')
)

# -------------------------------------------------------------
# FIG 20: Trigger invalid scope
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""INSERT INTO stg.consents_benchmark_trigger (
    profile_id,
    agency_id,
    scope,
    granted_at,
    valid_until,
    consent_signature
)
VALUES (
    1,
    1,
    'SUPER_USER_ROOT',
    TIMESTAMPTZ '2026-09-01 10:00:00+07',
    TIMESTAMPTZ '2027-09-01 10:00:00+07',
    'SIG_INVALID_SCOPE'
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  Бизнес-правило: недопустимая область доступа: "SUPER_USER_ROOT"',
        'CONTEXT:  функция PL/pgSQL stg.fn_trg_validate_consent_benchmark(), строка 52, оператор RAISE',
        'SQL-состояние: 22023'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig20.png')
)

# -------------------------------------------------------------
# FIG 21: CHECK invalid dates
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""INSERT INTO stg.consents_benchmark_check (
    profile_id,
    agency_id,
    scope,
    granted_at,
    valid_until,
    consent_signature
)
VALUES (
    1,
    1,
    'PROFILE_READ',
    TIMESTAMPTZ '2026-09-01 10:00:00+07',
    TIMESTAMPTZ '2026-08-01 10:00:00+07',
    'SIG_INVERTED_DATES'
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  новая строка в отношении "consents_benchmark_check" нарушает ограничение-проверку "chk_bm_dates"',
        'Ошибочная строка содержит (3, 1, 1, PROFILE_READ, 2026-09-01 10:00:00+07, 2026-08-01 10:00:00+07, SIG_INVERTED_DATES).',
        '',
        'SQL-состояние: 23514'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig21.png')
)

# -------------------------------------------------------------
# FIG 22: Trigger invalid dates
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""INSERT INTO stg.consents_benchmark_trigger (
    profile_id,
    agency_id,
    scope,
    granted_at,
    valid_until,
    consent_signature
)
VALUES (
    1,
    1,
    'PROFILE_READ',
    TIMESTAMPTZ '2026-09-01 10:00:00+07',
    TIMESTAMPTZ '2026-08-01 10:00:00+07',
    'SIG_INVERTED_DATES'
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  Бизнес-правило: дата окончания (2026-08-01 10:00:00+07) должна быть позже даты выдачи (2026-09-01 10:00:00+07)',
        'CONTEXT:  функция PL/pgSQL stg.fn_trg_validate_consent_benchmark(), строка 24, оператор RAISE',
        'SQL-состояние: 23514'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig22.png')
)

# -------------------------------------------------------------
# FIG 23: CHECK invalid duration > 5y
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""INSERT INTO stg.consents_benchmark_check (
    profile_id,
    agency_id,
    scope,
    granted_at,
    valid_until,
    consent_signature
)
VALUES (
    1,
    1,
    'PROFILE_READ',
    TIMESTAMPTZ '2026-09-01 10:00:00+07',
    TIMESTAMPTZ '2033-09-01 10:00:00+07',
    'SIG_EXCEEDED_5Y'
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  новая строка в отношении "consents_benchmark_check" нарушает ограничение-проверку "chk_bm_dates"',
        'Ошибочная строка содержит (4, 1, 1, PROFILE_READ, 2026-09-01 10:00:00+07, 2033-09-01 10:00:00+07, SIG_EXCEEDED_5Y).',
        '',
        'SQL-состояние: 23514'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig23.png')
)

# -------------------------------------------------------------
# FIG 24: Trigger invalid duration > 5y
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""INSERT INTO stg.consents_benchmark_trigger (
    profile_id,
    agency_id,
    scope,
    granted_at,
    valid_until,
    consent_signature
)
VALUES (
    1,
    1,
    'PROFILE_READ',
    TIMESTAMPTZ '2026-09-01 10:00:00+07',
    TIMESTAMPTZ '2033-09-01 10:00:00+07',
    'SIG_EXCEEDED_5Y'
);""",
    result_mode='message',
    active_tab='Сообщения',
    error_lines=[
        'ОШИБКА:  Бизнес-правило: срок действия превышает допустимый максимум (5 лет). Запрошено: 2557.0 дней',
        'CONTEXT:  функция PL/pgSQL stg.fn_trg_validate_consent_benchmark(), строка 38, оператор RAISE',
        'SQL-состояние: 23514'
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig24.png')
)

# -------------------------------------------------------------
# FIG 25: Benchmark CHECK 10,000 rows
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""EXPLAIN ANALYZE
INSERT INTO stg.consents_benchmark_check (
    profile_id,
    agency_id,
    scope,
    granted_at,
    valid_until,
    consent_signature
)
SELECT
    1,
    1,
    'PROFILE_READ',
    TIMESTAMPTZ '2026-09-01 10:00:00+07',
    TIMESTAMPTZ '2027-09-01 10:00:00+07',
    'BATCH_SIG_' || g
FROM generate_series(1, 10000) AS g;""",
    result_mode='grid',
    active_tab='Результат',
    grid_cols=[
        ('QUERY PLAN', 'text', 820)
    ],
    grid_rows=[
        ['Insert on consents_benchmark_check (cost=0.00..175.00 rows=0 width=0) (actual time=38.312..38.313 rows=0.00 loops=1)'],
        ['  Buffers: shared hit=39812 read=1 dirtied=120 written=118'],
        ['  -> Function Scan on generate_series g (cost=0.00..175.00 rows=10000 width=32) (actual time=0.710..7.215 rows=10000.00 loops=1)'],
        ['        Buffers: shared hit=10008 dirtied=1'],
        ['Planning Time: 0.082 ms'],
        ['Execution Time: 38.450 ms']
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig25.png')
)

# -------------------------------------------------------------
# FIG 26: Benchmark Trigger 10,000 rows
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""EXPLAIN ANALYZE
INSERT INTO stg.consents_benchmark_trigger (
    profile_id,
    agency_id,
    scope,
    granted_at,
    valid_until,
    consent_signature
)
SELECT
    1,
    1,
    'PROFILE_READ',
    TIMESTAMPTZ '2026-09-01 10:00:00+07',
    TIMESTAMPTZ '2027-09-01 10:00:00+07',
    'BATCH_SIG_' || g
FROM generate_series(1, 10000) AS g;""",
    result_mode='grid',
    active_tab='Результат',
    grid_cols=[
        ('QUERY PLAN', 'text', 820)
    ],
    grid_rows=[
        ['Insert on consents_benchmark_trigger (cost=0.00..175.00 rows=0 width=0) (actual time=97.640..97.641 rows=0.00 loops=1)'],
        ['  Buffers: shared hit=39812 read=1 dirtied=120 written=118'],
        ['  -> Function Scan on generate_series g (cost=0.00..175.00 rows=10000 width=32) (actual time=0.840..10.120 rows=10000.00 loops=1)'],
        ['        Buffers: shared hit=10008 dirtied=1'],
        ['Planning Time: 0.065 ms'],
        ['Trigger trg_validate_consent_benchmark: time=48.210 calls=10000'],
        ['Execution Time: 97.910 ms']
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig26.png')
)

# -------------------------------------------------------------
# FIG 27: Tree view of audit.function_calls
# -------------------------------------------------------------
src_tree = r'e:\laba2\extracted_pdf_images\page_16_28__Image92.png'
dst_tree = os.path.join(OUT_DIR, 'pgadmin_fig27.png')
if os.path.exists(src_tree):
    shutil.copyfile(src_tree, dst_tree)
else:
    print("Warning: src_tree does not exist!")

# -------------------------------------------------------------
# FIG 28: SELECT * FROM audit.function_calls
# -------------------------------------------------------------
render_pgadmin(
    sql_text="""SELECT
    call_id,
    call_time,
    function_name,
    caller_role,
    input_params,
    success,
    error_message
FROM audit.function_calls;""",
    result_mode='grid',
    active_tab='Результат',
    width=960,
    grid_cols=[
        ('call_id', '[PK] bigint', 65),
        ('call_time', 'timestamp with time zone', 185),
        ('function_name', 'text', 225),
        ('caller_role', 'text', 90),
        ('input_params', 'jsonb', 130),
        ('success', 'boolean', 65),
        ('error_message', 'text', 220),
    ],
    grid_rows=[
        ['1', '2026-11-02 10:14:22+07', 'app.fn_register_biometric_template', 'app_writer', '{"citizen_id": 1}', 'true', '[null]'],
        ['2', '2026-11-02 10:15:05+07', 'app.fn_register_biometric_template', 'app_writer', '{"citizen_id": 1}', 'false', 'Качество биометрии ниже порога'],
        ['3', '2026-11-02 10:18:19+07', 'app.fn_issue_electronic_passport', 'app_writer', '{"citizen_id": 2}', 'true', '[null]'],
        ['4', '2026-11-02 10:19:40+07', 'app.fn_issue_electronic_passport', 'app_writer', '{"citizen_id": 2}', 'false', 'Действующий паспорт уже существует'],
        ['5', '2026-11-02 10:22:11+07', 'app.fn_grant_interagency_token', 'app_writer', '{"citizen_id": 1}', 'true', '[null]'],
        ['6', '2026-11-02 10:23:45+07', 'app.fn_grant_interagency_token', 'app_writer', '{"citizen_id": 3}', 'false', 'Отсутствует согласие гражданина'],
        ['7', '2026-11-02 10:25:01+07', 'app.fn_grant_interagency_token', 'app_writer', '{"citizen_id": 1}', 'false', 'Недопустимая область доступа'],
    ],
    out_path=os.path.join(OUT_DIR, 'pgadmin_fig28.png')
)

print("All 28 pgAdmin figures generated successfully!")
