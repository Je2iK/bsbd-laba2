import re
import pypdf
import subprocess

with open(r'e:\laba2\migrations\000008_security_definer_functions.up.sql', 'r', encoding='utf-8') as f:
    mig8 = f.read()
with open(r'e:\laba2\migrations\000009_check_vs_trigger_benchmarks.up.sql', 'r', encoding='utf-8') as f:
    mig9 = f.read()

fn1 = re.search(r'(CREATE OR REPLACE FUNCTION app\.fn_register_biometric_template.*?END;\s*\$\$;)', mig8, re.DOTALL).group(1).strip()
fn2 = re.search(r'(CREATE OR REPLACE FUNCTION app\.fn_issue_electronic_passport.*?END;\s*\$\$;)', mig8, re.DOTALL).group(1).strip()
fn3 = re.search(r'(CREATE OR REPLACE FUNCTION app\.fn_grant_interagency_token.*?END;\s*\$\$;)', mig8, re.DOTALL).group(1).strip()
check_table = re.search(r'(CREATE TABLE IF NOT EXISTS stg\.consents_benchmark_check.*?ALTER TABLE stg\.consents_benchmark_check OWNER TO app_owner;)', mig9, re.DOTALL).group(1).strip()
trg_func = re.search(r'(CREATE OR REPLACE FUNCTION stg\.fn_trg_validate_consent_benchmark.*?CREATE TRIGGER trg_validate_consent_benchmark.*?FOR EACH ROW EXECUTE FUNCTION stg\.fn_trg_validate_consent_benchmark\(\);)', mig9, re.DOTALL).group(1).strip()

fn1_lines = fn1.split('\n')
fn2_lines = fn2.split('\n')
fn3_lines = fn3.split('\n')

p18_code = '\n'.join(fn1_lines[:50])
p19_code = '\n'.join(fn1_lines[50:])
p20_code = '\n'.join(fn2_lines[:56])
p21_code = '\n'.join(fn2_lines[56:])
p22_code = '\n'.join(fn3_lines[:52])
p23_code = '\n'.join(fn3_lines[52:]) + '\n\n-- stg.consents_benchmark_check (DDL с ограничениями CHECK)\n' + check_table
p24_code = '-- Триггерная валидация бизнес-правил (BEFORE INSERT)\n' + trg_func

app_a = """// ============================================================================
// СТРАНИЦА 18: ПРИЛОЖЕНИЕ A (ЧАСТЬ 1)
// ============================================================================
#heading-section[Приложение A]

#set text(font: "Consolas", size: 8.5pt)
#set par(first-line-indent: 0cm, leading: 0.42em)

```sql
-- app.fn_register_biometric_template - Регистрация биометрии (SECURITY DEFINER)
""" + p18_code + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 19: ПРИЛОЖЕНИЕ A (ЧАСТЬ 2)
// ============================================================================
```sql
-- app.fn_register_biometric_template (окончание)
""" + p19_code + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 20: ПРИЛОЖЕНИЕ A (ЧАСТЬ 3)
// ============================================================================
```sql
-- app.fn_issue_electronic_passport - Выпуск паспорта (SECURITY DEFINER)
""" + p20_code + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 21: ПРИЛОЖЕНИЕ A (ЧАСТЬ 4)
// ============================================================================
```sql
-- app.fn_issue_electronic_passport (окончание)
""" + p21_code + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 22: ПРИЛОЖЕНИЕ A (ЧАСТЬ 5)
// ============================================================================
```sql
-- app.fn_grant_interagency_token - Межведомственный токен (SECURITY DEFINER)
""" + p22_code + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 23: ПРИЛОЖЕНИЕ A (ЧАСТЬ 6)
// ============================================================================
```sql
-- app.fn_grant_interagency_token (окончание)
""" + p23_code + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 24: ПРИЛОЖЕНИЕ A (ЧАСТЬ 7)
// ============================================================================
```sql
""" + p24_code + """
```
"""

with open(r'e:\laba2\report.typ', 'r', encoding='utf-8') as f:
    typ_text = f.read()

idx = typ_text.find('// СТРАНИЦА 18: ПРИЛОЖЕНИЕ A')
if idx == -1:
    idx = typ_text.find('#heading-section[Приложение A]')
    idx = typ_text.rfind('// ============================================================================', 0, idx)

typ_text_new = typ_text[:idx] + app_a
with open(r'e:\laba2\report.typ', 'w', encoding='utf-8') as f:
    f.write(typ_text_new)

print('Updated Appendix A in report.typ successfully')
