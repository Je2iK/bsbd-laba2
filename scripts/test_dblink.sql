DO $$
DECLARE
    v_conn_str TEXT;
    v_sql TEXT;
BEGIN
    v_conn_str := 'dbname=' || current_database() || ' host=127.0.0.1 port=' || inet_server_port() || ' user=postgres password=password';
    v_sql := format('INSERT INTO audit.validation_violations (table_name, violated_rule, error_details, input_payload) VALUES (%L, %L, %L, %L::jsonb)',
        'test_tab', 'RULE_1', 'details', '{"foo": 1}');
    PERFORM dblink_exec(v_conn_str, v_sql);
END $$;
