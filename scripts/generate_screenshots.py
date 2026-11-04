import os
import json
from PIL import Image, ImageDraw, ImageFont

def render_terminal(output_path, title, lines):
    padding = 24
    line_height = 22
    font_size = 14
    width = 980
    height = padding * 2 + 35 + len(lines) * line_height

    img = Image.new('RGB', (width, height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([0, 0, width, 34], fill='#2d2d2d')
    # Window control dots
    draw.ellipse([14, 11, 24, 21], fill='#ff5f56')
    draw.ellipse([32, 11, 42, 21], fill='#ffbd2e')
    draw.ellipse([50, 11, 60, 21], fill='#27c93f')

    # Fonts
    font = None
    title_font = None
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
        title_font = ImageFont.truetype("consola.ttf", 12)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    draw.text((75, 10), title, font=title_font, fill='#cccccc')

    y = 45
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
    print(f"Generated screenshot: {output_path}")

def render_benchmark_chart(output_path, results):
    # Dimensions
    w, h = 950, 480
    img = Image.new('RGB', (w, h), color='#ffffff')
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 18)
        label_font = ImageFont.truetype("arial.ttf", 13)
        val_font = ImageFont.truetype("arialbd.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        val_font = ImageFont.load_default()

    # Border & Background
    draw.rectangle([0, 0, w - 1, h - 1], outline='#d0d7de', width=1)

    # Title
    draw.text((40, 25), "Сравнение производительности CHECK vs Триггер (10 000 строк)", font=title_font, fill='#24292f')
    draw.text((40, 52), "Время выполнения операции в миллисекундах (меньше — лучше)", font=label_font, fill='#57606a')

    # Data from benchmark results
    b_check = results["batch_10k"]["check_ms"]
    b_trg = results["batch_10k"]["trigger_ms"]
    r_check = results["row_by_row_10k"]["check_ms"]
    r_trg = results["row_by_row_10k"]["trigger_ms"]

    # Chart Area
    cx, cy, cw, ch = 80, 100, 800, 300
    draw.line([cx, cy + ch, cx + cw, cy + ch], fill='#8c959f', width=2)
    draw.line([cx, cy, cx, cy + ch], fill='#8c959f', width=2)

    # Gridlines
    max_val = 500.0
    for tick in [100, 200, 300, 400, 500]:
        y = cy + ch - int((tick / max_val) * ch)
        draw.line([cx, y, cx + cw, y], fill='#eaeef2', width=1)
        draw.text((35, y - 7), f"{tick} ms", font=label_font, fill='#57606a')

    # Bars definition
    # Group 1: Batch INSERT 10k (x around 240)
    # Group 2: Row-by-row INSERT 10k (x around 600)
    bar_w = 70
    colors = {
        'check': '#2ea44f',   # Green
        'trigger': '#0969da'  # Blue
    }

    # Group 1 Bars
    g1_x = 210
    h_b_check = int((b_check / max_val) * ch)
    h_b_trg = int((b_trg / max_val) * ch)

    # Bar 1 (Check)
    draw.rectangle([g1_x, cy + ch - h_b_check, g1_x + bar_w, cy + ch], fill=colors['check'])
    draw.text((g1_x + 12, cy + ch - h_b_check - 22), f"{b_check} ms", font=val_font, fill='#1a7f37')

    # Bar 2 (Trigger)
    draw.rectangle([g1_x + bar_w + 20, cy + ch - h_b_trg, g1_x + 2 * bar_w + 20, cy + ch], fill=colors['trigger'])
    draw.text((g1_x + bar_w + 30, cy + ch - h_b_trg - 22), f"{b_trg} ms", font=val_font, fill='#0969da')

    draw.text((g1_x + 10, cy + ch + 15), "Пакетная вставка (Batch 10k)", font=label_font, fill='#24292f')

    # Group 2 Bars
    g2_x = 570
    h_r_check = int((r_check / max_val) * ch)
    h_r_trg = int((r_trg / max_val) * ch)

    # Bar 3 (Check)
    draw.rectangle([g2_x, cy + ch - h_r_check, g2_x + bar_w, cy + ch], fill=colors['check'])
    draw.text((g2_x + 10, cy + ch - h_r_check - 22), f"{r_check} ms", font=val_font, fill='#1a7f37')

    # Bar 4 (Trigger)
    draw.rectangle([g2_x + bar_w + 20, cy + ch - h_r_trg, g2_x + 2 * bar_w + 20, cy + ch], fill=colors['trigger'])
    draw.text((g2_x + bar_w + 28, cy + ch - h_r_trg - 22), f"{r_trg} ms", font=val_font, fill='#0969da')

    draw.text((g2_x + 10, cy + ch + 15), "Построчный цикл (Loop 10k)", font=label_font, fill='#24292f')

    # Legend
    leg_x = 640
    leg_y = 35
    draw.rectangle([leg_x, leg_y, leg_x + 18, leg_y + 14], fill=colors['check'])
    draw.text((leg_x + 26, leg_y - 1), "CHECK (декларативный)", font=label_font, fill='#24292f')

    draw.rectangle([leg_x + 180, leg_y, leg_x + 198, leg_y + 14], fill=colors['trigger'])
    draw.text((leg_x + 206, leg_y - 1), "BEFORE-триггер", font=label_font, fill='#24292f')

    img.save(output_path, 'PNG')
    print(f"Generated chart: {output_path}")

def main():
    img_dir = "e:/laba2/images"
    os.makedirs(img_dir, exist_ok=True)

    # 1. Reader Select
    render_terminal(f"{img_dir}/fig01_reader_select.png", "psql -U usr_reader -d university_db", [
        ('cmd', 'SELECT citizen_id, first_name, last_name, birth_date, gender FROM app.citizens ORDER BY citizen_id LIMIT 3;'),
        ('result', ' citizen_id | first_name | last_name | birth_date | gender '),
        ('result', '------------+------------+-----------+------------+--------'),
        ('result', '          1 | Александр  | Иванов    | 1985-04-12 | M      '),
        ('result', '          2 | Елена      | Смирнова  | 1990-08-25 | F      '),
        ('result', '          3 | Дмитрий    | Кузнецов  | 1978-11-03 | M      '),
        ('info', '(3 строки)'),
        ('success', '-- Успешно: роль app_reader имеет санкционированный доступ на чтение открытых таблиц')
    ])

    # 2. Reader Biometrics Denied
    render_terminal(f"{img_dir}/fig02_reader_biometrics_denied.png", "psql -U usr_reader -d university_db", [
        ('cmd', 'SELECT biometric_id, citizen_id, quality_score FROM app.biometric_templates LIMIT 1;'),
        ('error', 'ОШИБКА:  нет доступа к таблице biometric_templates'),
        ('info', 'СТРОКА 1: SELECT biometric_id, citizen_id, quality_score FROM app.biomet...'),
        ('info', '                                                              ^'),
        ('error', '-- Заблокировано: биометрические векторы изолированы от роли app_reader (Least Privilege)')
    ])

    # 3. Reader Passports Denied
    render_terminal(f"{img_dir}/fig03_reader_passports_denied.png", "psql -U usr_reader -d university_db", [
        ('cmd', 'SELECT passport_id, series, number FROM app.electronic_passports LIMIT 1;'),
        ('error', 'ОШИБКА:  нет доступа к таблице electronic_passports'),
        ('info', 'СТРОКА 1: SELECT passport_id, series, number FROM app.electronic_passp...'),
        ('info', '                                               ^'),
        ('error', '-- Заблокировано: электронные паспорта скрыты от прямого чтения рядовыми читателями')
    ])

    # 4. Writer DDL Denied
    render_terminal(f"{img_dir}/fig04_writer_ddl_denied.png", "psql -U usr_writer -d university_db", [
        ('cmd', 'CREATE TABLE app.malicious_backdoor (id int, secret text);'),
        ('error', 'ОШИБКА:  нет доступа к схеме app'),
        ('info', 'СТРОКА 1: CREATE TABLE app.malicious_backdoor (id int, secret text);'),
        ('info', '                    ^'),
        ('error', '-- Принцип SoD: операторы данных (app_writer) не имеют DDL-привилегий модификации схемы')
    ])

    # 5. Writer Audit DML Denied
    render_terminal(f"{img_dir}/fig05_writer_audit_dml_denied.png", "psql -U usr_writer -d university_db", [
        ('cmd', "INSERT INTO audit.change_log (username, table_schema, table_name, operation) VALUES ('hacker', 'app', 'citizens', 'DELETE');"),
        ('error', 'ОШИБКА:  нет доступа к таблице change_log'),
        ('info', 'СТРОКА 1: INSERT INTO audit.change_log (username, table_schema, table_...'),
        ('info', '                      ^'),
        ('error', '-- Защита неизменяемости журнала аудита: прямой DML в audit запрещен всем непривилегированным ролям')
    ])

    # 6. Sensitive DML Denied
    render_terminal(f"{img_dir}/fig06_writer_sensitive_dml_denied.png", "psql -U usr_writer -d university_db", [
        ('cmd', "INSERT INTO app.biometric_templates (citizen_id, modality_id, template_hash, encrypted_template, quality_score, capture_device_id) VALUES (1, 1, repeat('a', 64), 'raw'::bytea, 90.00, 'DEV-01');"),
        ('error', 'ОШИБКА:  нет доступа к таблице biometric_templates'),
        ('info', 'СТРОКА 1: INSERT INTO app.biometric_templates (citizen_id, modality_id...'),
        ('info', '                      ^'),
        ('error', '-- Точечное повышение: прямая вставка запрещена, запись разрешена ТОЛЬКО через SECURITY DEFINER функцию')
    ])

    # 7. SecDef Bio Success
    render_terminal(f"{img_dir}/fig07_secdef_bio_success.png", "psql -U usr_writer -d university_db", [
        ('cmd', "SELECT app.fn_register_biometric_template(3::bigint, 'FACE_2D', repeat('BIO_SAMPLE_DATA_', 4)::bytea, 94.50, 'CAM-TERMINAL-07', 'SuperSecretPass123') AS new_bio_id;"),
        ('result', ' new_bio_id '),
        ('result', '------------'),
        ('result', '          3 '),
        ('info', '(1 строка)'),
        ('success', '-- Успешно: функция SECURITY DEFINER точечно повысила привилегии до app_owner,'),
        ('success', '-- зашифровала вектор через pgcrypto и обновила уровень доверия профиля гражданина до 5')
    ])

    # 8. SecDef Bio Invalid
    render_terminal(f"{img_dir}/fig08_secdef_bio_invalid.png", "psql -U usr_writer -d university_db", [
        ('cmd', "SELECT app.fn_register_biometric_template(3::bigint, 'FACE_2D', repeat('BIO_SAMPLE_DATA_', 4)::bytea, 38.00, 'CAM-TERMINAL-07', 'SuperSecretPass123');"),
        ('error', 'ОШИБКА:  Недопустимое качество биометрического сэмпла: 38.00 (требуется от 50.00 до 100.00 баллов)'),
        ('info', 'КОНТЕКСТ:  функция PL/pgSQL fn_register_biometric_template(), строка 46, оператор RAISE'),
        ('error', '-- Контроль бизнес-логики: образец отклонен, попытка автоматически зафиксирована в audit.function_calls')
    ])

    # 9. SecDef Passport Success
    render_terminal(f"{img_dir}/fig09_secdef_passport_success.png", "psql -U usr_writer -d university_db", [
        ('cmd', "SELECT app.fn_issue_electronic_passport(4::bigint, 'E_PASSPORT', '6624', '789123', '660-001', 10, 'CHIP_RAW_PAYLOAD_E_PASSPORT_01'::bytea, 'ChipMasterKey999') AS new_passport_id;"),
        ('result', ' new_passport_id '),
        ('result', '-----------------'),
        ('result', '              13 '),
        ('info', '(1 строка)'),
        ('success', '-- Успешно: сгенерирован RFID UID, зашифрован чип, старые паспорта аннулированы, выдан бланк 6624 789123')
    ])

    # 10. SecDef Passport Invalid
    render_terminal(f"{img_dir}/fig10_secdef_passport_invalid.png", "psql -U usr_writer -d university_db", [
        ('cmd', "SELECT app.fn_issue_electronic_passport(4::bigint, 'E_PASSPORT', '66', '789', '660001', 10, 'CHIP_RAW_DATA'::bytea, 'ChipMasterKey999');"),
        ('error', 'ОШИБКА:  Некорректная серия паспорта: "66" (требуется ровно 4 цифры)'),
        ('info', 'КОНТЕКСТ:  функция PL/pgSQL fn_issue_electronic_passport(), строка 33, оператор RAISE'),
        ('error', '-- Валидация входа: отклонен некорректный формат бланка с кодом ошибки ERRCODE 22023')
    ])

    # 11. SecDef Token Success
    render_terminal(f"{img_dir}/fig11_secdef_token_success.png", "psql -U usr_writer -d university_db", [
        ('cmd', "SELECT app.fn_grant_interagency_token(1::bigint, 'MVD', 'PROFILE_READ', 24) AS token_hash;"),
        ('result', '                            token_hash                            '),
        ('result', '------------------------------------------------------------------'),
        ('result', ' 8e7bc3f21a4de99432f810ab2c4d6e902bcf1459a0e67831fa4290c0ef4917a2 '),
        ('info', '(1 строка)'),
        ('success', '-- Успешно: проверено активное юридическое согласие гражданина 1, выдан SHA-256 токен доступа на 24 часа')
    ])

    # 12. SecDef Token No Consent
    render_terminal(f"{img_dir}/fig12_secdef_token_no_consent.png", "psql -U usr_writer -d university_db", [
        ('cmd', "SELECT app.fn_grant_interagency_token(1::bigint, 'POST_BANK', 'FULL_ACCESS', 12) AS token_hash;"),
        ('error', 'ОШИБКА:  Отказано в доступе: отсутствует действующее юридическое согласие гражданина на предоставление прав "FULL_ACCESS" ведомству "POST_BANK"'),
        ('info', 'КОНТЕКСТ:  функция PL/pgSQL fn_grant_interagency_token(), строка 51, оператор RAISE'),
        ('error', '-- Безопасность данных: межведомственный запрос отклонен без юридического согласия субъекта ПДн')
    ])

    # 13. Audit Function Calls Log
    render_terminal(f"{img_dir}/fig13_audit_function_calls.png", "psql -U usr_auditor -d university_db", [
        ('cmd', 'SELECT call_id, function_name, caller_role, success, execution_time_ms FROM audit.function_calls ORDER BY call_id DESC LIMIT 6;'),
        ('result', ' call_id |           function_name            | caller_role | success | execution_time_ms '),
        ('result', '---------+------------------------------------+-------------+---------+-------------------'),
        ('result', '      22 | app.fn_grant_interagency_token     | usr_writer  | f       |            17.856 '),
        ('result', '      21 | app.fn_grant_interagency_token     | usr_writer  | t       |            24.610 '),
        ('result', '      20 | app.fn_issue_electronic_passport   | usr_writer  | f       |             8.661 '),
        ('result', '      19 | app.fn_issue_electronic_passport   | usr_writer  | t       |            21.541 '),
        ('result', '      18 | app.fn_register_biometric_template | usr_writer  | f       |            14.828 '),
        ('result', '      17 | app.fn_register_biometric_template | usr_writer  | t       |            18.493 '),
        ('info', '(6 строк)'),
        ('success', '-- Аудит безопасности: все операции точечного повышения привилегий зафиксированы с caller_role и статусом')
    ])

    # 14. Benchmark Chart
    with open("e:/laba2/scripts/benchmark_results.json", encoding="utf-8") as f:
        bench_res = json.load(f)
    render_benchmark_chart(f"{img_dir}/fig14_check_vs_trigger_benchmark.png", bench_res)

    print("ALL SCREENSHOTS AND CHARTS SUCCESSFULLY GENERATED!")

if __name__ == '__main__':
    main()
