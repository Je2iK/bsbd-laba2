import re

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

p18_code = '-- app.fn_register_biometric_template - Регистрация биометрии (SECURITY DEFINER)\n' + '\n'.join(fn1_lines[:50])
p19_code = '-- app.fn_register_biometric_template (окончание)\n' + '\n'.join(fn1_lines[50:])
p20_code = '-- app.fn_issue_electronic_passport - Выпуск паспорта (SECURITY DEFINER)\n' + '\n'.join(fn2_lines[:56])
p21_code = '-- app.fn_issue_electronic_passport (окончание)\n' + '\n'.join(fn2_lines[56:])
p22_code = '-- app.fn_grant_interagency_token - Межведомственный токен (SECURITY DEFINER)\n' + '\n'.join(fn3_lines[:52])
p23_code = '-- app.fn_grant_interagency_token (окончание)\n' + '\n'.join(fn3_lines[52:]) + '\n\n-- stg.consents_benchmark_check (DDL с ограничениями CHECK)\n' + check_table
p24_code = '-- Триггерная валидация бизнес-правил (BEFORE INSERT)\n' + trg_func

with open(r'e:\laba2\scripts\build_chubreich_style_docx.py', 'r', encoding='utf-8') as f:
    docx_code = f.read()

idx = docx_code.find('add_heading(\'Приложение A\'')
if idx == -1:
    idx = docx_code.find('Приложение A')
idx = docx_code.rfind('# =========================================================================', 0, idx)

idx_end = docx_code.find('doc.save(')

docx_app_a = f'''# =========================================================================
    # Страница 18: Приложение A (часть 1)
    # =========================================================================
    add_heading('Приложение A', space_before=0, space_after=24)
    code_p18 = \"\"\"{p18_code}\"\"\"
    add_code_block(code_p18)
    doc.add_page_break()

    # =========================================================================
    # Страница 19: Приложение A (часть 2)
    # =========================================================================
    code_p19 = \"\"\"{p19_code}\"\"\"
    add_code_block(code_p19)
    doc.add_page_break()

    # =========================================================================
    # Страница 20: Приложение A (часть 3)
    # =========================================================================
    code_p20 = \"\"\"{p20_code}\"\"\"
    add_code_block(code_p20)
    doc.add_page_break()

    # =========================================================================
    # Страница 21: Приложение A (часть 4)
    # =========================================================================
    code_p21 = \"\"\"{p21_code}\"\"\"
    add_code_block(code_p21)
    doc.add_page_break()

    # =========================================================================
    # Страница 22: Приложение A (часть 5)
    # =========================================================================
    code_p22 = \"\"\"{p22_code}\"\"\"
    add_code_block(code_p22)
    doc.add_page_break()

    # =========================================================================
    # Страница 23: Приложение A (часть 6)
    # =========================================================================
    code_p23 = \"\"\"{p23_code}\"\"\"
    add_code_block(code_p23)
    doc.add_page_break()

    # =========================================================================
    # Страница 24: Приложение A (часть 7)
    # =========================================================================
    code_p24 = \"\"\"{p24_code}\"\"\"
    add_code_block(code_p24)

    '''

new_docx_code = docx_code[:idx] + docx_app_a + docx_code[idx_end:]
with open(r'e:\laba2\scripts\build_chubreich_style_docx.py', 'w', encoding='utf-8') as f:
    f.write(new_docx_code)

print('Updated build_chubreich_style_docx.py successfully')
