-- ============================================================================
-- Миграция 000007: Таблица и подсистема аудита вызовов SECURITY DEFINER функций
-- Вариант 12: Защита БД систем цифровой идентификации граждан
-- ============================================================================

-- Подключение dblink для автономного протоколирования (сохранение журнала даже при откате внешней транзакции)
CREATE EXTENSION IF NOT EXISTS dblink;

-- Таблица журнала вызовов функций повышенных привилегий
CREATE TABLE IF NOT EXISTS audit.function_calls (
    call_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    call_time TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    function_name TEXT NOT NULL,
    caller_role TEXT NOT NULL DEFAULT session_user,
    input_params JSONB NOT NULL,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    execution_time_ms NUMERIC(10,3)
);

COMMENT ON TABLE audit.function_calls IS 'Журнал регистрации вызовов функций с точечным повышением привилегий (SECURITY DEFINER)';
COMMENT ON COLUMN audit.function_calls.call_id IS 'Уникальный номер записи вызова';
COMMENT ON COLUMN audit.function_calls.call_time IS 'Точное время запуска функции (по системному таймеру clock_timestamp)';
COMMENT ON COLUMN audit.function_calls.function_name IS 'Полное имя вызванной функции (с указанием схемы)';
COMMENT ON COLUMN audit.function_calls.caller_role IS 'Роль реального пользователя сессии (session_user)';
COMMENT ON COLUMN audit.function_calls.input_params IS 'JSONB образ переданных входных параметров';
COMMENT ON COLUMN audit.function_calls.success IS 'Флаг успешного завершения операции (TRUE - успех, FALSE - ошибка)';
COMMENT ON COLUMN audit.function_calls.error_message IS 'Текст диагностического сообщения об ошибке при сбое';
COMMENT ON COLUMN audit.function_calls.execution_time_ms IS 'Время выполнения тела функции в миллисекундах';

-- Индексы для быстрого поиска по журналу
CREATE INDEX IF NOT EXISTS idx_func_calls_time ON audit.function_calls(call_time DESC);
CREATE INDEX IF NOT EXISTS idx_func_calls_name ON audit.function_calls(function_name);
CREATE INDEX IF NOT EXISTS idx_func_calls_caller ON audit.function_calls(caller_role);
CREATE INDEX IF NOT EXISTS idx_func_calls_success ON audit.function_calls(success);

-- Передача владения и строгие права доступа (Least Privilege)
ALTER TABLE audit.function_calls OWNER TO app_owner;

-- Запрет любых прямых изменений таблицы аудита для непривилегированных ролей
REVOKE ALL ON audit.function_calls FROM PUBLIC;
REVOKE ALL ON audit.function_calls FROM app_reader, app_writer;
GRANT SELECT ON audit.function_calls TO auditor, app_owner;

-- Служебная функция протоколирования вызова с поддержкой автономных транзакций
CREATE OR REPLACE FUNCTION audit.fn_log_function_call(
    p_function_name TEXT,
    p_caller_role TEXT,
    p_input_params JSONB,
    p_success BOOLEAN,
    p_error_message TEXT DEFAULT NULL,
    p_execution_time_ms NUMERIC DEFAULT NULL
)
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = audit, public, pg_temp
AS $$
DECLARE
    v_conn_str TEXT;
    v_sql TEXT;
BEGIN
    -- Попытка автономной фиксации через dblink (гарантия сохранности журнала при сбоях)
    BEGIN
        v_conn_str := 'dbname=' || current_database() || ' host=127.0.0.1 port=' || inet_server_port() || ' user=postgres password=password';
        v_sql := format(
            'INSERT INTO audit.function_calls (call_time, function_name, caller_role, input_params, success, error_message, execution_time_ms) VALUES (%L, %L, %L, %L::jsonb, %L, %L, %L)',
            clock_timestamp(), p_function_name, p_caller_role, p_input_params::text, p_success, p_error_message, p_execution_time_ms
        );
        PERFORM dblink_exec(v_conn_str, v_sql);
    EXCEPTION WHEN OTHERS THEN
        -- Фолбек на прямую вставку в рамках текущей транзакции
        INSERT INTO audit.function_calls (
            call_time, function_name, caller_role, input_params, success, error_message, execution_time_ms
        ) VALUES (
            clock_timestamp(), p_function_name, p_caller_role, p_input_params, p_success, p_error_message, p_execution_time_ms
        );
    END;
END;
$$;

COMMENT ON FUNCTION audit.fn_log_function_call IS 'Служебная процедура фиксации событий вызова функций в журнал audit.function_calls';
ALTER FUNCTION audit.fn_log_function_call OWNER TO app_owner;
REVOKE ALL ON FUNCTION audit.fn_log_function_call FROM PUBLIC;
GRANT EXECUTE ON FUNCTION audit.fn_log_function_call TO app_owner;
