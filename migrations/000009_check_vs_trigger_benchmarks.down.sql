DROP TRIGGER IF EXISTS trg_validate_consent_benchmark ON stg.consents_benchmark_trigger;
DROP FUNCTION IF EXISTS stg.fn_trg_validate_consent_benchmark();
DROP TABLE IF EXISTS stg.consents_benchmark_trigger CASCADE;
DROP TABLE IF EXISTS stg.consents_benchmark_check CASCADE;
DROP TABLE IF EXISTS audit.validation_violations CASCADE;
