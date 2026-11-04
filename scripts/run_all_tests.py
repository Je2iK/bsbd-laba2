import os
import subprocess
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
PSQL = r"C:\Program Files\PostgreSQL\18\bin\psql.exe"

def run_test_case(user, password, sql):
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    res = subprocess.run(
        [PSQL, '-U', user, '-p', '5433', '-h', '127.0.0.1', '-d', 'university_db', '-w', '-c', sql],
        capture_output=True, env=env, text=True, encoding='utf-8', errors='replace'
    )
    return res.stdout.strip(), res.stderr.strip(), res.returncode

def main():
    # Cleanup previous test runs to ensure complete idempotency
    run_test_case('postgres', 'password', "DELETE FROM app.electronic_passports WHERE series = '6624' AND number = '789123';")

    test_results = []

    # -------------------------------------------------------------------------
    # CASE 1: Чтение разрешенных таблиц (usr_reader)
    # -------------------------------------------------------------------------
    c1_sql = "SELECT citizen_id, first_name, last_name, birth_date, gender FROM app.citizens ORDER BY citizen_id LIMIT 3;"
    out, err, code = run_test_case('usr_reader', 'ReaderPass123!', c1_sql)
    test_results.append({
        "id": 1,
        "title": "Чтение общедоступных таблиц схемы app пользователем usr_reader",
        "user": "usr_reader",
        "sql": c1_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "SUCCESS",
        "status": "PASSED" if code == 0 and "Александр" in out else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 2: Попытка чтения закрытой таблицы биометрии (usr_reader)
    # -------------------------------------------------------------------------
    c2_sql = "SELECT biometric_id, citizen_id, quality_score FROM app.biometric_templates LIMIT 1;"
    out, err, code = run_test_case('usr_reader', 'ReaderPass123!', c2_sql)
    test_results.append({
        "id": 2,
        "title": "Попытка несанкционированного чтения биометрических данных (usr_reader)",
        "user": "usr_reader",
        "sql": c2_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "ERROR (Permission Denied for table biometric_templates)",
        "status": "PASSED" if code != 0 and ("нет доступа к таблице" in err.lower() or "permission denied" in err.lower()) else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 3: Попытка чтения электронных паспортов (usr_reader)
    # -------------------------------------------------------------------------
    c3_sql = "SELECT passport_id, series, number FROM app.electronic_passports LIMIT 1;"
    out, err, code = run_test_case('usr_reader', 'ReaderPass123!', c3_sql)
    test_results.append({
        "id": 3,
        "title": "Попытка несанкционированного чтения электронных паспортов (usr_reader)",
        "user": "usr_reader",
        "sql": c3_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "ERROR (Permission Denied for table electronic_passports)",
        "status": "PASSED" if code != 0 and ("нет доступа к таблице" in err.lower() or "permission denied" in err.lower()) else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 4: Попытка выполнения DDL неадминистратором (usr_writer)
    # -------------------------------------------------------------------------
    c4_sql = "CREATE TABLE app.malicious_backdoor (id int, secret text);"
    out, err, code = run_test_case('usr_writer', 'WriterPass123!', c4_sql)
    test_results.append({
        "id": 4,
        "title": "Попытка выполнения DDL (создание таблицы) оператором usr_writer",
        "user": "usr_writer",
        "sql": c4_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "ERROR (Permission Denied for schema app)",
        "status": "PASSED" if code != 0 and ("нет доступа к схеме" in err.lower() or "permission denied" in err.lower()) else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 5: Попытка прямой модификации (DML) таблицы аудита (usr_writer)
    # -------------------------------------------------------------------------
    c5_sql = "INSERT INTO audit.change_log (username, table_schema, table_name, operation) VALUES ('hacker', 'app', 'citizens', 'DELETE');"
    out, err, code = run_test_case('usr_writer', 'WriterPass123!', c5_sql)
    test_results.append({
        "id": 5,
        "title": "Попытка прямой модификации журнала change_log оператором usr_writer",
        "user": "usr_writer",
        "sql": c5_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "ERROR (Permission Denied for table change_log)",
        "status": "PASSED" if code != 0 and ("нет доступа к таблице" in err.lower() or "permission denied" in err.lower()) else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 6: Попытка прямого DML к закрытой таблице app.biometric_templates (usr_writer)
    # -------------------------------------------------------------------------
    c6_sql = "INSERT INTO app.biometric_templates (citizen_id, modality_id, template_hash, encrypted_template, quality_score, capture_device_id) VALUES (1, 1, repeat('a', 64), 'raw'::bytea, 90.00, 'DEV-01');"
    out, err, code = run_test_case('usr_writer', 'WriterPass123!', c6_sql)
    test_results.append({
        "id": 6,
        "title": "Попытка прямой вставки в защищенную таблицу биометрии в обход функций (usr_writer)",
        "user": "usr_writer",
        "sql": c6_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "ERROR (Permission Denied for table biometric_templates)",
        "status": "PASSED" if code != 0 and ("нет доступа к таблице" in err.lower() or "permission denied" in err.lower()) else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 7: Успешный вызов SECURITY DEFINER функции регистрации биометрии (usr_writer)
    # -------------------------------------------------------------------------
    c7_sql = "SELECT app.fn_register_biometric_template(3::bigint, 'FACE_2D', repeat('BIO_SAMPLE_DATA_', 4)::bytea, 94.50, 'CAM-TERMINAL-07', 'SuperSecretPass123') AS new_bio_id;"
    out, err, code = run_test_case('usr_writer', 'WriterPass123!', c7_sql)
    test_results.append({
        "id": 7,
        "title": "Позитивный вызов SECURITY DEFINER регистрации биометрии (usr_writer)",
        "user": "usr_writer",
        "sql": c7_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "SUCCESS (new_bio_id returned, trust level upgraded to 5)",
        "status": "PASSED" if code == 0 and "new_bio_id" in out else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 8: Негативный вызов SECURITY DEFINER биометрии (качество < 50.00) (usr_writer)
    # -------------------------------------------------------------------------
    c8_sql = "SELECT app.fn_register_biometric_template(3::bigint, 'FACE_2D', repeat('BIO_SAMPLE_DATA_', 4)::bytea, 38.00, 'CAM-TERMINAL-07', 'SuperSecretPass123');"
    out, err, code = run_test_case('usr_writer', 'WriterPass123!', c8_sql)
    test_results.append({
        "id": 8,
        "title": "Негативный вызов регистрации биометрии: отклонение сэмпла низкого качества (usr_writer)",
        "user": "usr_writer",
        "sql": c8_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "ERROR (Недопустимое качество биометрического сэмпла: 38.00)",
        "status": "PASSED" if code != 0 and "недопустимое качество" in err.lower() else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 9: Успешный вызов SECURITY DEFINER выдачи электронного паспорта (usr_writer)
    # -------------------------------------------------------------------------
    c9_sql = "SELECT app.fn_issue_electronic_passport(4::bigint, 'E_PASSPORT', '6624', '789123', '660-001', 10, 'CHIP_RAW_PAYLOAD_E_PASSPORT_01'::bytea, 'ChipMasterKey999') AS new_passport_id;"
    out, err, code = run_test_case('usr_writer', 'WriterPass123!', c9_sql)
    test_results.append({
        "id": 9,
        "title": "Позитивный вызов SECURITY DEFINER выпуска электронного паспорта (usr_writer)",
        "user": "usr_writer",
        "sql": c9_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "SUCCESS (new_passport_id returned, old passports deactivated)",
        "status": "PASSED" if code == 0 and "new_passport_id" in out else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 10: Негативный вызов выдачи паспорта: неверный формат серии/номера (usr_writer)
    # -------------------------------------------------------------------------
    c10_sql = "SELECT app.fn_issue_electronic_passport(4::bigint, 'E_PASSPORT', '66', '789', '660001', 10, 'CHIP_RAW_DATA'::bytea, 'ChipMasterKey999');"
    out, err, code = run_test_case('usr_writer', 'WriterPass123!', c10_sql)
    test_results.append({
        "id": 10,
        "title": "Негативный вызов выпуска паспорта: нарушение формата бланка (usr_writer)",
        "user": "usr_writer",
        "sql": c10_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "ERROR (Некорректная серия паспорта: 66)",
        "status": "PASSED" if code != 0 and "некорректная серия" in err.lower() else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 11: Успешный вызов выдачи межведомственного токена при согласии (usr_writer)
    # -------------------------------------------------------------------------
    c11_sql = "SELECT app.fn_grant_interagency_token(1::bigint, 'MVD', 'PROFILE_READ', 24) AS token_hash;"
    out, err, code = run_test_case('usr_writer', 'WriterPass123!', c11_sql)
    test_results.append({
        "id": 11,
        "title": "Позитивный вызов выдачи межведомственного токена при активном согласии (usr_writer)",
        "user": "usr_writer",
        "sql": c11_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "SUCCESS (token_hash generated and registered)",
        "status": "PASSED" if code == 0 and "token_hash" in out else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 12: Негативный вызов выдачи токена: отсутствие согласия гражданина (usr_writer)
    # -------------------------------------------------------------------------
    c12_sql = "SELECT app.fn_grant_interagency_token(1::bigint, 'POST_BANK', 'FULL_ACCESS', 12) AS token_hash;"
    out, err, code = run_test_case('usr_writer', 'WriterPass123!', c12_sql)
    test_results.append({
        "id": 12,
        "title": "Негативный вызов выдачи токена: отказ из-за отсутствия согласия (usr_writer)",
        "user": "usr_writer",
        "sql": c12_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "ERROR (Отсутствует действующее юридическое согласие)",
        "status": "PASSED" if code != 0 and "согласие" in err.lower() else "FAILED"
    })

    # -------------------------------------------------------------------------
    # CASE 13: Инспекция журнала аудита audit.function_calls (usr_auditor)
    # -------------------------------------------------------------------------
    c13_sql = "SELECT call_id, function_name, caller_role, success, error_message, execution_time_ms FROM audit.function_calls ORDER BY call_id DESC LIMIT 6;"
    out, err, code = run_test_case('usr_auditor', 'AuditorPass123!', c13_sql)
    test_results.append({
        "id": 13,
        "title": "Аудит и контроль: инспекция журнала audit.function_calls аудитором (usr_auditor)",
        "user": "usr_auditor",
        "sql": c13_sql,
        "stdout": out,
        "stderr": err,
        "exit_code": code,
        "expected": "SUCCESS (returns recorded successful and failed calls)",
        "status": "PASSED" if code == 0 and "function_name" in out else "FAILED"
    })

    with open("e:/laba2/scripts/test_results.json", "w", encoding="utf-8") as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)

    print("ALL TESTS RUN FINISHED!")
    passed = sum(1 for t in test_results if t['status'] == 'PASSED')
    print(f"Total: {len(test_results)}, Passed: {passed}, Failed: {len(test_results) - passed}")
    for t in test_results:
        print(f"[{t['status']}] Case {t['id']}: {t['title']}")

if __name__ == '__main__':
    main()
