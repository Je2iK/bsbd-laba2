import os
import subprocess
import json

PSQL = r"C:\Program Files\PostgreSQL\18\bin\psql.exe"
ENV = os.environ.copy()
ENV['PGPASSWORD'] = 'password'

def run_sql(sql):
    res = subprocess.run(
        [PSQL, '-U', 'postgres', '-p', '5433', '-h', '127.0.0.1', '-d', 'university_db', '-w', '-tAc', sql],
        capture_output=True, env=ENV, text=True, encoding='cp1251', errors='replace'
    )
    return res.stdout.strip(), res.stderr.strip(), res.returncode

def main():
    print("=== STARTING CHECK vs TRIGGER BENCHMARK (10,000 ROWS) ===")

    # Clear previous benchmark data
    run_sql("TRUNCATE TABLE stg.consents_benchmark_check, stg.consents_benchmark_trigger, audit.validation_violations;")

    # 1. Batch INSERT 10,000 rows - CHECK
    batch_check_sql = """
    DO $$
    DECLARE
        t1 TIMESTAMPTZ := clock_timestamp();
        t2 TIMESTAMPTZ;
        ms NUMERIC;
    BEGIN
        INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
        SELECT
            (i % 12) + 1,
            (i % 10) + 1,
            'PROFILE_READ',
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP + INTERVAL '1 year',
            'SIG_BATCH_CHECK_' || i
        FROM generate_series(1, 10000) AS i;
        t2 := clock_timestamp();
        ms := round((EXTRACT(EPOCH FROM (t2 - t1)) * 1000)::numeric, 2);
        RAISE NOTICE 'BATCH_CHECK_MS:%', ms;
    END $$;
    """
    _, err, _ = run_sql(batch_check_sql)
    batch_check_ms = float(err.split("BATCH_CHECK_MS:")[1].split()[0]) if "BATCH_CHECK_MS:" in err else 0.0

    # 2. Batch INSERT 10,000 rows - TRIGGER
    batch_trg_sql = """
    DO $$
    DECLARE
        t1 TIMESTAMPTZ := clock_timestamp();
        t2 TIMESTAMPTZ;
        ms NUMERIC;
    BEGIN
        INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
        SELECT
            (i % 12) + 1,
            (i % 10) + 1,
            'PROFILE_READ',
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP + INTERVAL '1 year',
            'SIG_BATCH_TRG_' || i
        FROM generate_series(1, 10000) AS i;
        t2 := clock_timestamp();
        ms := round((EXTRACT(EPOCH FROM (t2 - t1)) * 1000)::numeric, 2);
        RAISE NOTICE 'BATCH_TRG_MS:%', ms;
    END $$;
    """
    _, err, _ = run_sql(batch_trg_sql)
    batch_trg_ms = float(err.split("BATCH_TRG_MS:")[1].split()[0]) if "BATCH_TRG_MS:" in err else 0.0

    # Clear tables for row-by-row benchmark
    run_sql("TRUNCATE TABLE stg.consents_benchmark_check, stg.consents_benchmark_trigger;")

    # 3. Row-by-row INSERT 10,000 rows - CHECK
    row_check_sql = """
    DO $$
    DECLARE
        t1 TIMESTAMPTZ := clock_timestamp();
        t2 TIMESTAMPTZ;
        ms NUMERIC;
    BEGIN
        FOR i IN 1..10000 LOOP
            INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
            VALUES (
                (i % 12) + 1,
                (i % 10) + 1,
                'DOCS_VERIFY',
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP + INTERVAL '2 years',
                'SIG_ROW_CHECK_' || i
            );
        END LOOP;
        t2 := clock_timestamp();
        ms := round((EXTRACT(EPOCH FROM (t2 - t1)) * 1000)::numeric, 2);
        RAISE NOTICE 'ROW_CHECK_MS:%', ms;
    END $$;
    """
    _, err, _ = run_sql(row_check_sql)
    row_check_ms = float(err.split("ROW_CHECK_MS:")[1].split()[0]) if "ROW_CHECK_MS:" in err else 0.0

    # 4. Row-by-row INSERT 10,000 rows - TRIGGER
    row_trg_sql = """
    DO $$
    DECLARE
        t1 TIMESTAMPTZ := clock_timestamp();
        t2 TIMESTAMPTZ;
        ms NUMERIC;
    BEGIN
        FOR i IN 1..10000 LOOP
            INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
            VALUES (
                (i % 12) + 1,
                (i % 10) + 1,
                'DOCS_VERIFY',
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP + INTERVAL '2 years',
                'SIG_ROW_TRG_' || i
            );
        END LOOP;
        t2 := clock_timestamp();
        ms := round((EXTRACT(EPOCH FROM (t2 - t1)) * 1000)::numeric, 2);
        RAISE NOTICE 'ROW_TRG_MS:%', ms;
    END $$;
    """
    _, err, _ = run_sql(row_trg_sql)
    row_trg_ms = float(err.split("ROW_TRG_MS:")[1].split()[0]) if "ROW_TRG_MS:" in err else 0.0

    # 5. Test Violation & Audit Logging
    invalid_check_sql = """
    INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
    VALUES (1, 1, 'PROFILE_READ', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP - INTERVAL '1 day', 'INVALID_CHECK_SIG');
    """
    _, err_check, code_check = run_sql(invalid_check_sql)

    invalid_trg_sql = """
    INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
    VALUES (1, 1, 'PROFILE_READ', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '7 years', 'INVALID_TRG_SIG');
    """
    _, err_trg, code_trg = run_sql(invalid_trg_sql)

    # Count violations logged in audit table
    violations_count, _, _ = run_sql("SELECT count(*) FROM audit.validation_violations;")
    violations_details, _, _ = run_sql("SELECT json_agg(t) FROM (SELECT violation_id, violated_rule, error_details FROM audit.validation_violations) t;")

    results = {
        "batch_10k": {
            "check_ms": batch_check_ms,
            "check_tps": round(10000 / (batch_check_ms / 1000.0), 1) if batch_check_ms > 0 else 0,
            "trigger_ms": batch_trg_ms,
            "trigger_tps": round(10000 / (batch_trg_ms / 1000.0), 1) if batch_trg_ms > 0 else 0,
            "overhead_pct": round(((batch_trg_ms - batch_check_ms) / batch_check_ms) * 100, 1) if batch_check_ms > 0 else 0
        },
        "row_by_row_10k": {
            "check_ms": row_check_ms,
            "check_tps": round(10000 / (row_check_ms / 1000.0), 1) if row_check_ms > 0 else 0,
            "trigger_ms": row_trg_ms,
            "trigger_tps": round(10000 / (row_trg_ms / 1000.0), 1) if row_trg_ms > 0 else 0,
            "overhead_pct": round(((row_trg_ms - row_check_ms) / row_check_ms) * 100, 1) if row_check_ms > 0 else 0
        },
        "negative_tests": {
            "check_error": err_check,
            "trigger_error": err_trg,
            "violations_logged": int(violations_count) if violations_count.isdigit() else 0,
            "violations_details": violations_details
        }
    }

    with open("e:/laba2/scripts/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("BENCHMARK COMPLETED SUCCESSFULLY!")
    print(f"Batch Check MS: {batch_check_ms}, Trigger MS: {batch_trg_ms}")
    print(f"Row Check MS: {row_check_ms}, Trigger MS: {row_trg_ms}")
    print(f"Violations Logged: {violations_count}")

if __name__ == '__main__':
    main()
