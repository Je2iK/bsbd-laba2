import re
import pypdf

with open(r'e:\laba2\migrations\000008_security_definer_functions.up.sql', 'r', encoding='utf-8') as f:
    mig8 = f.read()
with open(r'e:\laba2\migrations\000009_check_vs_trigger_benchmarks.up.sql', 'r', encoding='utf-8') as f:
    mig9 = f.read()

fn1 = re.search(r'(CREATE OR REPLACE FUNCTION app\.fn_register_biometric_template.*?END;\s*\$\$;)', mig8, re.DOTALL).group(1).strip()
fn2 = re.search(r'(CREATE OR REPLACE FUNCTION app\.fn_issue_electronic_passport.*?END;\s*\$\$;)', mig8, re.DOTALL).group(1).strip()
fn3 = re.search(r'(CREATE OR REPLACE FUNCTION app\.fn_grant_interagency_token.*?END;\s*\$\$;)', mig8, re.DOTALL).group(1).strip()

check_table = re.search(r'(CREATE TABLE IF NOT EXISTS stg\.consents_benchmark_check.*?ALTER TABLE stg\.consents_benchmark_check OWNER TO app_owner;)', mig9, re.DOTALL).group(1).strip()
trg_table = re.search(r'(CREATE TABLE IF NOT EXISTS stg\.consents_benchmark_trigger.*?ALTER TABLE stg\.consents_benchmark_trigger OWNER TO app_owner;)', mig9, re.DOTALL).group(1).strip()
trg_func = re.search(r'(CREATE OR REPLACE FUNCTION stg\.fn_trg_validate_consent_benchmark.*?CREATE TRIGGER trg_validate_consent_benchmark.*?FOR EACH ROW EXECUTE FUNCTION stg\.fn_trg_validate_consent_benchmark\(\);)', mig9, re.DOTALL).group(1).strip()

fn1_lines = fn1.split('\n')
fn2_lines = fn2.split('\n')
fn3_lines = fn3.split('\n')
trg_lines = trg_func.split('\n')

all_app_a_lines = (
    ['-- app.fn_register_biometric_template - Регистрация биометрии (SECURITY DEFINER)'] + fn1_lines +
    ['', '-- app.fn_issue_electronic_passport - Выпуск паспорта (SECURITY DEFINER)'] + fn2_lines +
    ['', '-- app.fn_grant_interagency_token - Выдача межведомственного токена (SECURITY DEFINER)'] + fn3_lines
)

# Filter out empty comment dividers
cleaned_app_a = [l for l in all_app_a_lines if not l.strip().startswith('-- ==') and not l.strip().startswith('-- --')]

# Distribute 320 lines into 5 pages (18-22):
# Page 18: 52 lines (with heading)
# Page 19: 67 lines
# Page 20: 67 lines
# Page 21: 67 lines
# Page 22: remaining (~67 lines)
p18 = '\n'.join(cleaned_app_a[:52])
p19 = '\n'.join(cleaned_app_a[52:119])
p20 = '\n'.join(cleaned_app_a[119:186])
p21 = '\n'.join(cleaned_app_a[186:253])
p22 = '\n'.join(cleaned_app_a[253:])

# Appendix B:
all_app_b_lines = (
    ['-- Тестовые таблицы сравнения CHECK и триггера'] + check_table.split('\n') +
    ['', trg_table] +
    ['', '-- Функция BEFORE-триггера stg.fn_trg_validate_consent_benchmark'] + [l for l in trg_lines if not l.strip().startswith('-- ==')]
)

# Page 23: 55 lines (with heading)
# Page 24: remaining lines
p23 = '\n'.join(all_app_b_lines[:52])
p24 = '\n'.join(all_app_b_lines[52:])

app_content = """// ============================================================================
// СТРАНИЦА 18: ПРИЛОЖЕНИЕ A (ЧАСТЬ 1)
// ============================================================================
#heading-section[Приложение A]

#set text(font: "Consolas", size: 7.2pt)
#set par(first-line-indent: 0cm, leading: 0.32em)

```sql
""" + p18 + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 19: ПРИЛОЖЕНИЕ A (ЧАСТЬ 2)
// ============================================================================
#set text(font: "Consolas", size: 7.2pt)
#set par(first-line-indent: 0cm, leading: 0.32em)

```sql
""" + p19 + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 20: ПРИЛОЖЕНИЕ A (ЧАСТЬ 3)
// ============================================================================
#set text(font: "Consolas", size: 7.2pt)
#set par(first-line-indent: 0cm, leading: 0.32em)

```sql
""" + p20 + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 21: ПРИЛОЖЕНИЕ A (ЧАСТЬ 4)
// ============================================================================
#set text(font: "Consolas", size: 7.2pt)
#set par(first-line-indent: 0cm, leading: 0.32em)

```sql
""" + p21 + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 22: ПРИЛОЖЕНИЕ A (ЧАСТЬ 5)
// ============================================================================
#set text(font: "Consolas", size: 7.2pt)
#set par(first-line-indent: 0cm, leading: 0.32em)

```sql
""" + p22 + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 23: ПРИЛОЖЕНИЕ Б (ЧАСТЬ 1)
// ============================================================================
#heading-section[Приложение Б]

#set text(font: "Consolas", size: 7.2pt)
#set par(first-line-indent: 0cm, leading: 0.32em)

```sql
""" + p23 + """
```

#pagebreak()

// ============================================================================
// СТРАНИЦА 24: ПРИЛОЖЕНИЕ Б (ЧАСТЬ 2)
// ============================================================================
#set text(font: "Consolas", size: 7.2pt)
#set par(first-line-indent: 0cm, leading: 0.32em)

```sql
""" + p24 + """
```
"""

with open(r'e:\laba2\report.typ', 'r', encoding='utf-8') as f:
    typ_text = f.read()

idx = typ_text.find('// СТРАНИЦА 18: ПРИЛОЖЕНИЕ A')
if idx == -1:
    idx = typ_text.find('#heading-section[Приложение A]')
    idx = typ_text.rfind('// ============================================================================', 0, idx)

typ_text_new = typ_text[:idx] + app_content
with open(r'e:\laba2\report.typ', 'w', encoding='utf-8') as f:
    f.write(typ_text_new)

print('Updated report.typ with Appendix A and B cleanly')
