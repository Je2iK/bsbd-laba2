INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)
VALUES (1, 1, 'PROFILE_READ', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '7 years', 'INVALID_TRG_SIG');
