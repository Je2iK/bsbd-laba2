import psycopg2

conn = psycopg2.connect(dbname='university_db', user='postgres', password='password', host='127.0.0.1', port=5433)
cur = conn.cursor()

print("--- Checking stg.consents_benchmark_check constraints ---")
cur.execute("SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid = 'stg.consents_benchmark_check'::regclass;")
for r in cur.fetchall():
    print(r)

print("\n--- Checking triggers on stg.consents_benchmark_trigger ---")
cur.execute("SELECT trigger_name, event_manipulation, action_statement FROM information_schema.triggers WHERE event_object_table = 'consents_benchmark_trigger';")
for r in cur.fetchall():
    print(r)

print("\n--- Checking function definition for stg.fn_trg_validate_consent_benchmark ---")
cur.execute("SELECT pg_get_functiondef(oid) FROM pg_proc WHERE proname = 'fn_trg_validate_consent_benchmark';")
r = cur.fetchone()
if r:
    print(r[0][:200] + "\n...\n" + r[0][-200:])
else:
    print("Function NOT FOUND")

conn.close()
