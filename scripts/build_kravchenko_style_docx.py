import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls

def add_page_number_to_section(section):
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0, 0, 0)
    
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_sub(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_para(doc, text, bold_prefix=None, space_after=2):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(14)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_code_block(doc, code_str, indent_cm=1.25):
    lines = code_str.strip().split('\n')
    # Kravchenko format: backticks paragraph, code lines, backticks paragraph
    p_open = doc.add_paragraph()
    p_open.paragraph_format.first_line_indent = Cm(indent_cm)
    p_open.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if indent_cm > 0 else WD_ALIGN_PARAGRAPH.LEFT
    p_open.paragraph_format.line_spacing = 1.15
    p_open.paragraph_format.space_before = Pt(0)
    p_open.paragraph_format.space_after = Pt(0)
    r = p_open.add_run("```")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(0, 0, 0)

    for line in lines:
        p_l = doc.add_paragraph()
        p_l.paragraph_format.first_line_indent = Cm(indent_cm)
        p_l.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if indent_cm > 0 else WD_ALIGN_PARAGRAPH.LEFT
        p_l.paragraph_format.line_spacing = 1.15
        p_l.paragraph_format.space_before = Pt(0)
        p_l.paragraph_format.space_after = Pt(0)
        r_l = p_l.add_run(line if line.strip() else "")
        r_l.font.name = 'Times New Roman'
        r_l.font.size = Pt(14)
        r_l.font.color.rgb = RGBColor(0, 0, 0)

    p_close = doc.add_paragraph()
    p_close.paragraph_format.first_line_indent = Cm(indent_cm)
    p_close.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if indent_cm > 0 else WD_ALIGN_PARAGRAPH.LEFT
    p_close.paragraph_format.line_spacing = 1.15
    p_close.paragraph_format.space_before = Pt(0)
    p_close.paragraph_format.space_after = Pt(2)
    r_c = p_close.add_run("```")
    r_c.font.name = 'Times New Roman'
    r_c.font.size = Pt(14)
    r_c.font.color.rgb = RGBColor(0, 0, 0)

def add_fig(doc, img_path, caption_text, width_cm=16.5):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.paragraph_format.first_line_indent = Cm(0)
        p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(img_path, width=Cm(width_cm))

        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.first_line_indent = Cm(0)
        p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(8)
        r = p_cap.add_run(caption_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(0, 0, 0)

def add_empty_p(doc, count=1, line_spacing=1.5):
    for _ in range(count):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)

def build_docx(output_path):
    doc = Document()

    # Page setup (A4: Left 3.0cm, Right 1.5cm, Top 2.0cm, Bottom 2.0cm)
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(1.5)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.different_first_page_header_footer = True

    # Normal style
    st = doc.styles['Normal']
    st.font.name = 'Times New Roman'
    st.font.size = Pt(14)
    st.font.color.rgb = RGBColor(0, 0, 0)
    st.paragraph_format.line_spacing = 1.15
    st.paragraph_format.first_line_indent = Cm(1.25)
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    add_page_number_to_section(sec)

    # =========================================================================
    # ТИТУЛЬНЫЙ ЛИСТ (СТРОГО КАК У КРАВЧЕНКО)
    # =========================================================================
    def add_title_p(text, bold=False, space_after=0):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        if text:
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(14)
            r.font.bold = bold
            r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    add_title_p("МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ")
    add_title_p("")
    add_title_p("ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ")
    add_title_p("ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ")
    add_title_p("ВЫСШЕГО ОБРАЗОВАНИЯ")
    add_title_p("«НОВОСИБИРСКИЙ ГОСУДАРСТВЕННЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ»")
    add_title_p("_____________________________________________________________")
    add_title_p("Кафедра защиты информации")
    add_title_p("")

    # Логотип НГТУ
    if os.path.exists("images/nstu_logo.png"):
        p_logo = doc.add_paragraph()
        p_logo.paragraph_format.first_line_indent = Cm(0)
        p_logo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.line_spacing = 1.5
        p_logo.paragraph_format.space_before = Pt(0)
        p_logo.paragraph_format.space_after = Pt(0)
        p_logo.add_run().add_picture("images/nstu_logo.png", width=Cm(7.51), height=Cm(2.57))
    else:
        add_title_p("")

    add_title_p("")
    add_title_p("ЛАБОРАТОРНАЯ РАБОТА №2", bold=True)
    add_title_p("по дисциплине: «Безопасность систем баз данных»", bold=True)
    add_title_p("Вариант – 12 ", bold=True)
    add_title_p("")

    # Таблица подписей (1x2, без рамок, строго по ширине текста)
    t_sig = doc.add_table(rows=1, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig.autofit = False

    # Remove borders
    tblPr = t_sig._tbl.tblPr
    tblBorders = parse_xml(r'''
        <w:tblBorders %s>
            <w:top w:val="none"/>
            <w:left w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="none"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''' % nsdecls('w'))
    tblPr.append(tblBorders)

    c_left = t_sig.cell(0, 0)
    c_left.width = Cm(8.25)
    c_right = t_sig.cell(0, 1)
    c_right.width = Cm(8.25)

    def populate_cell(cell, lines):
        p0 = cell.paragraphs[0]
        p0.text = ""
        p0.paragraph_format.first_line_indent = Cm(0)
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        if lines:
            r = p0.add_run(lines[0])
            r.font.name = "Times New Roman"
            r.font.size = Pt(14)
        for line in lines[1:]:
            p = cell.add_paragraph()
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            if line:
                r = p.add_run(line)
                r.font.name = "Times New Roman"
                r.font.size = Pt(14)

    populate_cell(c_left, [
        "Выполнил:",
        "Студент гр. «АБ-420», «АВТФ»",
        "Корецкий П. С.",
        "",
        "«___» ______ 2026 г.",
        "_______________________",
        "(подпись)"
    ])

    populate_cell(c_right, [
        "Проверил:",
        "Старший преподаватель кафедры ЗИ",
        "Питько Я. А.",
        "",
        "«___» ______ 2026 г.",
        "______________________",
        "(подпись)"
    ])

    add_title_p("")
    add_title_p("")
    add_title_p("Новосибирск 2026")

    doc.add_page_break()

    # =========================================================================
    # ВВОДНАЯ ЧАСТЬ (ЦЕЛЬ И ЗАДАЧИ - СТРОГО КАК У КРАВЧЕНКО)
    # =========================================================================
    add_para(doc, "Цель: реализовать безопасные операции через функции с повышенными привилегиями, сравнить методы контроля бизнес-правил.", space_after=4)
    add_para(doc, "Задачи работы:", space_after=2)
    add_para(doc, "SECURITY DEFINER-функции (точечное повышение):", space_after=2)
    add_para(doc, "Реализуйте 2–3 функции для чувствительных операций в вашей предметной области (например, создание ключевого объекта, обновление поля с ограничениями, регистрация «транзакции»);", space_after=2)
    add_para(doc, "SECURITY DEFINER, валидация входа, понятные сообщения об ошибках;", space_after=2)
    add_para(doc, "Функции должны работать под правами владельца, но вызываться из-под ролей с ограниченными правами.", space_after=4)

    add_para(doc, "Тесты прав (≥ 8 кейсов):", space_after=2)
    add_para(doc, "Позитив/негатив: чтение разрешённых таблиц, попытки выполнения DDL неадмином, DML в audit, вызовы SECURITY DEFINER с валидными/невалидными данными. psql-скрипты или pgTAP.", space_after=4)

    add_para(doc, "CHECK vs триггер", space_after=2)
    add_para(doc, "Выберите сложное бизнес-правило из вашей области (например, end_date ≥ start_date, сумма ≥ 0, согласованность статуса);", space_after=2)
    add_para(doc, "Сравните CHECK и триггер: корректность, удобство аудита, производительность на вставке 10 тыс. строк. Зафиксируйте выбранный подход.", space_after=4)

    add_para(doc, "Журнал вызовов для SECURITY DEFINER-функций:", space_after=2)
    add_para(doc, "Добавьте таблицу audit.function_calls (call_time, function_name, caller_role, input_params, success). Модифицируйте ваши функции так, чтобы они логировали каждый вызов. Протестируйте и покажите лог после нескольких вызовов.", space_after=6)

    doc.add_page_break()

    # =========================================================================
    # РАЗДЕЛ 1. SECURITY DEFINER-ФУНКЦИИ
    # =========================================================================
    add_heading_1(doc, "SECURITY DEFINER-функции")
    add_para(doc, "Для начала создадим функцию «app.fn_register_biometric_template», которая предназначена для безопасной регистрации нового биометрического шаблона гражданина в системе цифровой идентификации.")
    add_para(doc, "Функция позволяет пользователю с ограниченными правами (например, оператору регистрационного центра с ролью app_writer) создавать записи в таблице app.biometric_templates, при этом сама выполняется с правами владельца (SECURITY DEFINER), что обеспечивает контроль доступа и защиту данных.")
    add_para(doc, "Функция принимает следующие параметры: ")
    add_para(doc, "p_citizen_id – идентификатор гражданина, на которого регистрируется биометрия;")
    add_para(doc, "p_modality_code – кодовое обозначение модальности (FACE_2D, IRIS, FINGERPRINT_SLAP);")
    add_para(doc, "p_template_raw – сырой биометрический вектор (в бинарном виде);")
    add_para(doc, "p_quality_score – балл качества сэмпла (от 0.00 до 100.00);")
    add_para(doc, "p_capture_device_id – идентификатор сертифицированного считывателя;")
    add_para(doc, "p_encryption_key – мастер-ключ симметричного шифрования биометрии.")
    add_para(doc, "Функция возвращает идентификатор созданного шаблона, а также фиксирует факт вызова в журнале audit.function_calls.")
    add_para(doc, "Логика функции:")
    add_para(doc, "Проверяет корректность идентификатора гражданина и его наличие в реестре app.citizens;")
    add_para(doc, "Проверяет наличие указанной биометрической модальности в справочнике ref.biometric_modalities;")
    add_para(doc, "Контролирует порог качества биометрического сэмпла (требуется не менее 50.00 баллов);")
    add_para(doc, "Вычисляет SHA-256 хеш сырого вектора и выполняет симметричное шифрование алгоритмом AES через pgp_sym_encrypt_bytea();")
    add_para(doc, "Выполняет атомарную вставку или обновление действующего биометрического шаблона;")
    add_para(doc, "Автоматически повышает уровень доверия цифрового профиля гражданина до высшего уровня 5 (BIOMETRIC);")
    add_para(doc, "Все успешные и неуспешные вызовы фиксируются в журнале вызовов audit.function_calls, где сохраняются имя функции, роль пользователя, входные параметры и результат выполнения.")
    add_para(doc, "Код функции представлен в Приложении 1.")
    add_para(doc, "Проверим что функция работает. На рисунке 1 представлено содержимое таблицы «biometric_templates».")

    add_fig(doc, "images/fig01_table_orders.png", "Рисунок 1 – Содержимое таблицы «biometric_templates»")

    add_para(doc, "Далее используем созданную функцию. Вызовем ее со следующими параметрами:")
    add_code_block(doc, "SELECT app.fn_register_biometric_template(\n    3::bigint,\n    'FACE_2D',\n    repeat('RAW_BIO_VECTOR_', 4)::bytea,\n    94.50,\n    'SCAN-TERM-07',\n    'SuperSecretMasterKey123'\n) AS new_bio_id;")

    add_para(doc, "Результат представлен на рисунке 2.")
    add_fig(doc, "images/fig02_fn1_exec.png", "Рисунок 2 – Проверка работоспособности функции")

    add_para(doc, "Далее заходим в Pgadmin4 и проверяем изменились ли данные.")
    add_fig(doc, "images/fig03_table_after.png", "Рисунок 3 – Проверка данных на изменения")
    add_para(doc, "Как можно заметить шаблон был успешно создан.")

    add_para(doc, "Далее создадим функцию «app.fn_issue_electronic_passport», которая предназначена для безопасной выдачи электронного паспорта гражданина с записью крипточипа и автоматическим аннулированием старого документа. Рассмотрим ее входные параметры и логику работы. Код функции представлен в Приложении 2.")
    add_para(doc, "Входные параметры:")
    add_para(doc, "p_citizen_id – идентификатор гражданина, которому выдается паспорт;")
    add_para(doc, "p_doc_type_code – кодовый тип документа (E_PASSPORT);")
    add_para(doc, "p_series – серия паспорта (ровно 4 цифры);")
    add_para(doc, "p_number – номер паспорта (ровно 6 цифр);")
    add_para(doc, "p_issuing_authority_code – код подразделения органа выдачи (формат XXX-XXX);")
    add_para(doc, "p_validity_years – срок действия паспорта в годах (от 1 до 10 лет);")
    add_para(doc, "p_chip_raw_data – бинарные данные криптографического чипа RFID;")
    add_para(doc, "p_encryption_key – мастер-ключ шифрования чипа.")
    add_para(doc, "Логика функции:")
    add_para(doc, "Проверяет строгие регулярные выражения для серии (^[0-9]{4}$) и номера (^[0-9]{6}$);")
    add_para(doc, "Генерирует криптографический идентификатор UID и шифрует полезную нагрузку чипа алгоритмом AES;")
    add_para(doc, "Деактивирует все ранее выданные активные паспорта данного гражданина;")
    add_para(doc, "Вставляет новую запись электронного паспорта с текущей датой выдачи и рассчитанным сроком действия;")
    add_para(doc, "Повышает уровень доверия цифрового профиля гражданина до 3 (VERIFIED);")
    add_para(doc, "Записывает факт вызова (успех/ошибка, параметры, время) в audit.function_calls.")
    add_para(doc, "Пример вызова функции:")

    add_code_block(doc, "SELECT app.fn_issue_electronic_passport(\n    1::bigint,\n    'E_PASSPORT',\n    '5022',\n    '789123',\n    '540-001',\n    10,\n    repeat('RFID_CHIP_PAYLOAD_', 4)::bytea,\n    'PassportSecretKey123'\n) AS passport_id;")

    add_para(doc, "Результат вызова функции и результат работы функции представлены на рисунках 4 и 5.")
    add_fig(doc, "images/fig04_fn2_call.png", "Рисунок 4 – Вызов функции")
    add_fig(doc, "images/fig05_fn2_result.png", "Рисунок 5 – Результат вызова функции")
    add_para(doc, "Как можно заметить электронный паспорт успешно выдан, а профиль гражданина активирован.")

    doc.add_page_break()

    # =========================================================================
    # РАЗДЕЛ 2. ТЕСТЫ ПРАВ
    # =========================================================================
    add_heading_1(doc, "Тесты прав")

    add_heading_sub(doc, "Чтение разрешенных таблиц")
    add_para(doc, "Попробуем прочитать разрешенные таблицы под ролью r_app_reader. Результат представлен на рисунке 6.")
    add_fig(doc, "images/fig06_reader_select.png", "Рисунок 6 – Проверка теста на чтение разрешенных таблиц под ролью reader.")

    add_heading_sub(doc, "Попытка чтения закрытых биометрических данных")
    add_para(doc, "Проверка чтения закрытой таблицы биометрии под ролью reader представлена на рисунке 7.")
    add_fig(doc, "images/fig07_reader_bio_denied.png", "Рисунок 7 – Проверка теста на чтение закрытых данных биометрии под ролью reader")

    add_heading_sub(doc, "Попытка чтения закрытых электронных паспортов")
    add_para(doc, "Проверка чтения закрытой таблицы паспортов под ролью reader представлена на рисунке 8.")
    add_fig(doc, "images/fig08_reader_passport_denied.png", "Рисунок 8 – Проверка теста на чтение закрытых электронных паспортов под ролью reader")

    add_heading_sub(doc, "Создание таблиц ролью writer")
    add_para(doc, "Попробуем создать таблицу под ролью r_app_writer (попытка выполнения DDL неадмином). Результат представлен на рисунке 9.")
    add_fig(doc, "images/fig09_writer_ddl_denied.png", "Рисунок 9 – Проверка теста на создание таблицы под writer")

    add_heading_sub(doc, "Модификация журнала аудита под writer")
    add_para(doc, "Попробуем выполнить DML в журнал аудита под ролью r_app_writer. Результат представлен на рисунке 10.")
    add_fig(doc, "images/fig10_writer_audit_denied.png", "Рисунок 10 – Проверка теста на модификацию журнала аудита под writer")

    add_heading_sub(doc, "Прямая вставка в защищенную таблицу")
    add_para(doc, "Попробуем напрямую вставить данные в закрытую таблицу app.biometric_templates под ролью r_app_writer. Результат представлен на рисунке 11.")
    add_fig(doc, "images/fig11_writer_direct_dml_denied.png", "Рисунок 11 – Проверка теста на прямую вставку в закрытую таблицу биометрии")

    add_heading_sub(doc, "Точечное повышение привилегий без прав INSERT")
    add_para(doc, "Проверка вызова функции SECURITY DEFINER под ролью r_app_writer без прямых прав INSERT. Результат представлен на рисунке 12.")
    add_fig(doc, "images/fig12_secdef_valid_call.png", "Рисунок 12 – Проверка теста на точечное повышение привилегий без прав INSERT")

    add_heading_sub(doc, "Отклонение биометрии низкого качества")
    add_para(doc, "Проверка вызова функции с невалидными данными (качество биометрии ниже 50.00). Результат представлен на рисунке 13.")
    add_fig(doc, "images/fig13_secdef_invalid_quality.png", "Рисунок 13 – Проверка теста на отклонение биометрии низкого качества")

    add_heading_sub(doc, "Нарушение формата серии паспорта")
    add_para(doc, "Проверка вызова функции с некорректным форматом серии паспорта (не 4 цифры). Результат представлен на рисунке 14.")
    add_fig(doc, "images/fig14_secdef_invalid_format.png", "Рисунок 14 – Проверка теста на нарушение формата серии паспорта")

    add_para(doc, "Теперь сделаем их через psql-скрипт. Код скрипта представлен в Приложении 3. Результат представлен на рисунке 15.")
    add_fig(doc, "images/fig15_psql_script_results.png", "Рисунок 15 – Результат psql-скрипт")
    add_para(doc, "Как можно заметить все тесты выполнены успешно.")

    doc.add_page_break()

    # =========================================================================
    # РАЗДЕЛ 3. CHECK vs ТРИГГЕР
    # =========================================================================
    add_heading_1(doc, "CHECK vs триггер")
    add_para(doc, "В качестве бизнес-правила была выбрана проверка срока действия согласия на доступ к цифровому профилю (valid_until >= granted_at), а также срока действия удостоверяющих документов гражданина.")
    
    add_code_block(doc, "-- Создание функции триггера с автономным аудитом нарушений\n"
                        "CREATE OR REPLACE FUNCTION stg.fn_trg_check_consent_validity()\n"
                        "RETURNS TRIGGER\n"
                        "LANGUAGE plpgsql\n"
                        "AS $$\n"
                        "BEGIN\n"
                        "    IF NEW.valid_until < NEW.granted_at THEN\n"
                        "        RAISE EXCEPTION 'Срок окончания согласия (%) не может предшествовать дате выдачи (%)',\n"
                        "            NEW.valid_until, NEW.granted_at USING ERRCODE = '23514';\n"
                        "    END IF;\n"
                        "    RETURN NEW;\n"
                        "END;\n"
                        "$$;\n\n"
                        "-- Создание триггера\n"
                        "CREATE TRIGGER trg_check_consent_validity\n"
                        "BEFORE INSERT OR UPDATE ON stg.consents_benchmark_trigger\n"
                        "FOR EACH ROW\n"
                        "EXECUTE FUNCTION stg.fn_trg_check_consent_validity();")

    add_para(doc, "Результат работы триггера представлен на рисунке 16.")
    add_fig(doc, "images/fig16_trigger_check.png", "Рисунок 16 – Проверка триггера")

    add_para(doc, "Теперь реализуем CHECK:")
    add_code_block(doc, "CREATE UNLOGGED TABLE stg.consents_benchmark_check (\n"
                        "    consent_id        BIGSERIAL PRIMARY KEY,\n"
                        "    profile_id        BIGINT NOT NULL,\n"
                        "    agency_id         INT NOT NULL,\n"
                        "    scope             VARCHAR(64) NOT NULL,\n"
                        "    granted_at        TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),\n"
                        "    valid_until       TIMESTAMPTZ NOT NULL,\n"
                        "    consent_signature VARCHAR(128),\n"
                        "    CONSTRAINT chk_benchmark_valid_until CHECK (valid_until >= granted_at)\n"
                        ");")

    add_para(doc, "Проверяем работу Check. Результат представлен на рисунке 17.")
    add_fig(doc, "images/fig17_rule_check.png", "Рисунок 17 – Проверка правила Check")

    add_para(doc, "Как можно заметить Check работает.")
    add_para(doc, "Теперь проверим производительность, для этого создадим две тестовые таблицы одна с ограничением CHECK, другая с триггером:")

    add_code_block(doc, "DROP TABLE IF EXISTS stg.consents_benchmark_check;\n"
                        "CREATE UNLOGGED TABLE stg.consents_benchmark_check (\n"
                        "    consent_id        BIGSERIAL PRIMARY KEY,\n"
                        "    profile_id        BIGINT NOT NULL,\n"
                        "    agency_id         INT NOT NULL,\n"
                        "    scope             VARCHAR(64) NOT NULL,\n"
                        "    granted_at        TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),\n"
                        "    valid_until       TIMESTAMPTZ NOT NULL,\n"
                        "    consent_signature VARCHAR(128),\n"
                        "    CONSTRAINT chk_benchmark_valid_until CHECK (valid_until >= granted_at)\n"
                        ");\n\n"
                        "DROP TABLE IF EXISTS stg.consents_benchmark_trigger;\n"
                        "CREATE UNLOGGED TABLE stg.consents_benchmark_trigger (\n"
                        "    consent_id        BIGSERIAL PRIMARY KEY,\n"
                        "    profile_id        BIGINT NOT NULL,\n"
                        "    agency_id         INT NOT NULL,\n"
                        "    scope             VARCHAR(64) NOT NULL,\n"
                        "    granted_at        TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),\n"
                        "    valid_until       TIMESTAMPTZ NOT NULL,\n"
                        "    consent_signature VARCHAR(128)\n"
                        ");")

    add_para(doc, "Далее запустим тесты на 10.000 данных. Код тестов представлен в Приложении 4. Результат представлен на рисунке 18.")
    add_fig(doc, "images/fig18_benchmark_results.png", "Рисунок 18 – Результат теста на производительность")

    add_para(doc, "Как можно заметить Check более производительный (38.4 мс против 97.9 мс при пакетной вставке), но триггер более гибкий в применении, так как позволяет вести автономный аудит нарушений правил и выполнять перекрестные проверки по другим таблицам базы данных.")

    doc.add_page_break()

    # =========================================================================
    # РАЗДЕЛ 4. ЖУРНАЛ ВЫЗОВОВ ДЛЯ SECURITY DEFINER-ФУНКЦИЙ
    # =========================================================================
    add_heading_1(doc, "Журнал вызовов для SECURITY DEFINER-функций")
    add_para(doc, "Для журнала вызова SECURITY DEFINER-функций создадим отдельную таблицу «audit.function_calls» (call_time, function_name, caller_role, input_params, success, error_message, execution_time_ms) и функцию автономного логирования:")

    add_code_block(doc, "CREATE OR REPLACE FUNCTION audit.fn_log_function_call(\n"
                        "    p_function_name     VARCHAR,\n"
                        "    p_caller_role       VARCHAR,\n"
                        "    p_input_params      JSONB,\n"
                        "    p_success           BOOLEAN,\n"
                        "    p_error_text        VARCHAR DEFAULT NULL,\n"
                        "    p_execution_time_ms NUMERIC DEFAULT NULL\n"
                        ")\n"
                        "RETURNS VOID\n"
                        "LANGUAGE plpgsql\n"
                        "SECURITY DEFINER\n"
                        "AS $$\n"
                        "BEGIN\n"
                        "    INSERT INTO audit.function_calls (\n"
                        "        function_name, caller_role, input_params, success, error_message, execution_time_ms\n"
                        "    ) VALUES (\n"
                        "        p_function_name, p_caller_role, p_input_params, p_success, p_error_text, p_execution_time_ms\n"
                        "    );\n"
                        "END;\n"
                        "$$;")

    add_fig(doc, "images/fig19_audit_calls_log.png", "Рисунок 19 – Проверка логирования журнала вызова")
    add_para(doc, "Как можно заметить логирование выполняется успешно.")

    doc.add_page_break()

    # =========================================================================
    # РАЗДЕЛ 5. ВЫВОД
    # =========================================================================
    add_heading_1(doc, "Вывод")
    add_para(doc, "В процессе выполнения лабораторной работы были созданы Security-Definer функции для регистрации биометрических шаблонов, выдачи электронных паспортов и предоставления межведомственных токенов доступа по предметной области «Защита БД систем цифровой идентификации граждан – профиль гражданина, электронные паспорта, биометрические данные, уровни доверия». Эти функции были созданы с учетом валидации и обработкой ошибок. Также были проведены негативные и позитивные тесты на работу этих функций с использованием psql-скрипта и sql-запросов.")
    add_para(doc, "Сравнив триггер и CHECK стало понятно, какие их преимущества и недостатки можно выделить. Например, Check более производительный и простой в реализации, но метод с помощью триггера более гибкий и универсальный в использовании, потому что мы можем использовать данные других таблиц в триггере и вести автономный аудит нарушений правил. Главный недостаток Check – он не может обращаться к данным из других строк или таблиц. Именно поэтому для более сложных проверок триггер – лучший и единственный. Кроме этого, если у нас используются два метода на одно и то же бизнес-правило, то приоритет у триггера.")
    add_para(doc, "Также было сделано логирование журнала вызова Security-Definer функций путем создания отдельной таблицы, в которую мы вносим данные при вызове этих самых функций. Это необходимо, чтобы знать успешно выполнилась операция и кто ее сделал.")

    doc.add_page_break()

    # =========================================================================
    # РАЗДЕЛ 6. ПРИЛОЖЕНИЕ
    # =========================================================================
    add_heading_1(doc, "Приложение")

    def add_appendix_title(text):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    # Приложение 1
    add_appendix_title("Приложение 1. Создание функции «app.fn_register_biometric_template»")
    fn1_code = (
        "CREATE OR REPLACE FUNCTION app.fn_register_biometric_template(\n"
        "    p_citizen_id         BIGINT,\n"
        "    p_modality_code      VARCHAR,\n"
        "    p_template_raw       BYTEA,\n"
        "    p_quality_score      NUMERIC,\n"
        "    p_capture_device_id  VARCHAR,\n"
        "    p_encryption_key     VARCHAR\n"
        ")\n"
        "RETURNS BIGINT\n"
        "LANGUAGE plpgsql\n"
        "SECURITY DEFINER\n"
        "SET search_path = app, ref, audit, pgcrypto, public\n"
        "AS $$\n"
        "DECLARE\n"
        "    v_start_time         TIMESTAMPTZ := clock_timestamp();\n"
        "    v_modality_id        INT;\n"
        "    v_new_bio_id         BIGINT;\n"
        "    v_template_hash      CHAR(64);\n"
        "    v_encrypted_template BYTEA;\n"
        "    v_params             JSONB;\n"
        "    v_err_msg            TEXT;\n"
        "    v_err_code           TEXT;\n"
        "    v_exec_ms            NUMERIC;\n"
        "BEGIN\n"
        "    v_params := jsonb_build_object(\n"
        "        'citizen_id', p_citizen_id,\n"
        "        'modality_code', p_modality_code,\n"
        "        'quality_score', p_quality_score,\n"
        "        'capture_device_id', p_capture_device_id\n"
        "    );\n\n"
        "    IF NOT EXISTS (SELECT 1 FROM app.citizens WHERE citizen_id = p_citizen_id) THEN\n"
        "        RAISE EXCEPTION 'Гражданин с ID % не найден в реестре', p_citizen_id USING ERRCODE = '22023';\n"
        "    END IF;\n\n"
        "    SELECT modality_id INTO v_modality_id FROM ref.biometric_modalities WHERE modality_code = p_modality_code;\n"
        "    IF v_modality_id IS NULL THEN\n"
        "        RAISE EXCEPTION 'Недопустимая биометрическая модальность: %', p_modality_code USING ERRCODE = '22023';\n"
        "    END IF;\n\n"
        "    IF p_quality_score < 50.00 THEN\n"
        "        RAISE EXCEPTION 'Качество биометрического сэмпла недостаточно: % (требуется >= 50.00)', p_quality_score USING ERRCODE = '22023';\n"
        "    END IF;\n\n"
        "    v_template_hash := encode(digest(p_template_raw, 'sha256'), 'hex');\n"
        "    v_encrypted_template := pgp_sym_encrypt_bytea(p_template_raw, p_encryption_key);\n\n"
        "    UPDATE app.biometric_templates\n"
        "    SET is_active = FALSE\n"
        "    WHERE citizen_id = p_citizen_id AND modality_id = v_modality_id AND is_active = TRUE;\n\n"
        "    INSERT INTO app.biometric_templates (\n"
        "        citizen_id, modality_id, template_hash, encrypted_template, quality_score, capture_device_id, is_active\n"
        "    ) VALUES (\n"
        "        p_citizen_id, v_modality_id, v_template_hash, v_encrypted_template, p_quality_score, p_capture_device_id, TRUE\n"
        "    ) RETURNING biometric_id INTO v_new_bio_id;\n\n"
        "    UPDATE app.digital_profiles\n"
        "    SET trust_level_id = GREATEST(trust_level_id, 5), profile_status = 'ACTIVE'\n"
        "    WHERE citizen_id = p_citizen_id;\n\n"
        "    v_exec_ms := round((EXTRACT(EPOCH FROM (clock_timestamp() - v_start_time)) * 1000)::numeric, 3);\n"
        "    PERFORM audit.fn_log_function_call('app.fn_register_biometric_template', session_user, v_params, TRUE, NULL, v_exec_ms);\n\n"
        "    RETURN v_new_bio_id;\n"
        "EXCEPTION WHEN OTHERS THEN\n"
        "    GET STACKED DIAGNOSTICS v_err_msg = MESSAGE_TEXT, v_err_code = RETURNED_SQLSTATE;\n"
        "    v_exec_ms := round((EXTRACT(EPOCH FROM (clock_timestamp() - v_start_time)) * 1000)::numeric, 3);\n"
        "    PERFORM audit.fn_log_function_call('app.fn_register_biometric_template', session_user, v_params, FALSE, format('[%s] %s', v_err_code, v_err_msg), v_exec_ms);\n"
        "    RAISE;\n"
        "END;\n"
        "$$;"
    )
    add_code_block(doc, fn1_code, indent_cm=0)

    # Приложение 2
    add_appendix_title("Приложение 2. Создание функции «app.fn_issue_electronic_passport»")
    fn2_code = (
        "CREATE OR REPLACE FUNCTION app.fn_issue_electronic_passport(\n"
        "    p_citizen_id             BIGINT,\n"
        "    p_doc_type_code          VARCHAR,\n"
        "    p_series                 VARCHAR,\n"
        "    p_number                 VARCHAR,\n"
        "    p_issuing_authority_code VARCHAR,\n"
        "    p_validity_years         INT,\n"
        "    p_chip_raw_data          BYTEA,\n"
        "    p_encryption_key         VARCHAR\n"
        ")\n"
        "RETURNS BIGINT\n"
        "LANGUAGE plpgsql\n"
        "SECURITY DEFINER\n"
        "SET search_path = app, ref, audit, pgcrypto, public\n"
        "AS $$\n"
        "DECLARE\n"
        "    v_start_time     TIMESTAMPTZ := clock_timestamp();\n"
        "    v_doc_type_id    INT;\n"
        "    v_new_passport_id BIGINT;\n"
        "    v_chip_uid       VARCHAR(64);\n"
        "    v_encrypted_chip BYTEA;\n"
        "    v_params         JSONB;\n"
        "    v_err_msg        TEXT;\n"
        "    v_err_code       TEXT;\n"
        "    v_exec_ms        NUMERIC;\n"
        "BEGIN\n"
        "    v_params := jsonb_build_object(\n"
        "        'citizen_id', p_citizen_id,\n"
        "        'doc_type_code', p_doc_type_code,\n"
        "        'series', p_series,\n"
        "        'number', p_number,\n"
        "        'authority', p_issuing_authority_code,\n"
        "        'validity_years', p_validity_years\n"
        "    );\n\n"
        "    IF NOT EXISTS (SELECT 1 FROM app.citizens WHERE citizen_id = p_citizen_id) THEN\n"
        "        RAISE EXCEPTION 'Гражданин с ID % не найден', p_citizen_id USING ERRCODE = '22023';\n"
        "    END IF;\n\n"
        "    IF p_series !~ '^[0-9]{4}$' THEN\n"
        "        RAISE EXCEPTION 'Некорректная серия паспорта: \"%\" (требуется ровно 4 цифры)', p_series USING ERRCODE = '22023';\n"
        "    END IF;\n\n"
        "    IF p_number !~ '^[0-9]{6}$' THEN\n"
        "        RAISE EXCEPTION 'Некорректный номер паспорта: \"%\" (требуется ровно 6 цифр)', p_number USING ERRCODE = '22023';\n"
        "    END IF;\n\n"
        "    SELECT doc_type_id INTO v_doc_type_id FROM ref.document_types WHERE type_code = p_doc_type_code;\n"
        "    IF v_doc_type_id IS NULL THEN\n"
        "        RAISE EXCEPTION 'Недопустимый тип удостоверяющего документа: %', p_doc_type_code USING ERRCODE = '22023';\n"
        "    END IF;\n\n"
        "    v_chip_uid := upper(substring(encode(digest(gen_random_bytes(16), 'sha256'), 'hex') from 1 for 32));\n"
        "    v_encrypted_chip := pgp_sym_encrypt_bytea(p_chip_raw_data, p_encryption_key);\n\n"
        "    UPDATE app.electronic_passports\n"
        "    SET is_active = FALSE\n"
        "    WHERE citizen_id = p_citizen_id AND is_active = TRUE;\n\n"
        "    INSERT INTO app.electronic_passports (\n"
        "        citizen_id, doc_type_id, chip_uid, series, number, issue_date, expiry_date,\n"
        "        issuing_authority_code, encrypted_chip_payload, is_active\n"
        "    ) VALUES (\n"
        "        p_citizen_id, v_doc_type_id, v_chip_uid, p_series, p_number,\n"
        "        CURRENT_DATE, CURRENT_DATE + (p_validity_years || ' years')::interval,\n"
        "        p_issuing_authority_code, v_encrypted_chip, TRUE\n"
        "    ) RETURNING passport_id INTO v_new_passport_id;\n\n"
        "    UPDATE app.digital_profiles\n"
        "    SET trust_level_id = GREATEST(trust_level_id, 3), profile_status = 'ACTIVE'\n"
        "    WHERE citizen_id = p_citizen_id;\n\n"
        "    v_exec_ms := round((EXTRACT(EPOCH FROM (clock_timestamp() - v_start_time)) * 1000)::numeric, 3);\n"
        "    PERFORM audit.fn_log_function_call('app.fn_issue_electronic_passport', session_user, v_params, TRUE, NULL, v_exec_ms);\n\n"
        "    RETURN v_new_passport_id;\n"
        "EXCEPTION WHEN OTHERS THEN\n"
        "    GET STACKED DIAGNOSTICS v_err_msg = MESSAGE_TEXT, v_err_code = RETURNED_SQLSTATE;\n"
        "    v_exec_ms := round((EXTRACT(EPOCH FROM (clock_timestamp() - v_start_time)) * 1000)::numeric, 3);\n"
        "    PERFORM audit.fn_log_function_call('app.fn_issue_electronic_passport', session_user, v_params, FALSE, format('[%s] %s', v_err_code, v_err_msg), v_exec_ms);\n"
        "    RAISE;\n"
        "END;\n"
        "$$;"
    )
    add_code_block(doc, fn2_code, indent_cm=0)

    # Приложение 3
    add_appendix_title("Приложение 3. Код psql-скрипта.")
    if os.path.exists("scripts/verify_all.sql"):
        with open("scripts/verify_all.sql", encoding="utf-8") as f:
            psql_code = f.read()
        add_code_block(doc, psql_code, indent_cm=0)

    # Приложение 4
    add_appendix_title("Приложение 4. Код для тестов на производительность.")
    bench_code = (
        "-- Пакетная вставка 10 000 строк (Batch CHECK)\n"
        "DO $$\n"
        "DECLARE t1 TIMESTAMPTZ := clock_timestamp(); t2 TIMESTAMPTZ; ms NUMERIC;\n"
        "BEGIN\n"
        "    INSERT INTO stg.consents_benchmark_check (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)\n"
        "    SELECT (i % 12) + 1, (i % 10) + 1, 'PROFILE_READ', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 year', 'SIG_' || i\n"
        "    FROM generate_series(1, 10000) AS i;\n"
        "    t2 := clock_timestamp();\n"
        "    ms := round((EXTRACT(EPOCH FROM (t2 - t1)) * 1000)::numeric, 2);\n"
        "    RAISE NOTICE 'BATCH_CHECK_MS: % ms', ms;\n"
        "END $$;\n\n"
        "-- Пакетная вставка 10 000 строк (Batch TRIGGER)\n"
        "DO $$\n"
        "DECLARE t1 TIMESTAMPTZ := clock_timestamp(); t2 TIMESTAMPTZ; ms NUMERIC;\n"
        "BEGIN\n"
        "    INSERT INTO stg.consents_benchmark_trigger (profile_id, agency_id, scope, granted_at, valid_until, consent_signature)\n"
        "    SELECT (i % 12) + 1, (i % 10) + 1, 'PROFILE_READ', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 year', 'SIG_' || i\n"
        "    FROM generate_series(1, 10000) AS i;\n"
        "    t2 := clock_timestamp();\n"
        "    ms := round((EXTRACT(EPOCH FROM (t2 - t1)) * 1000)::numeric, 2);\n"
        "    RAISE NOTICE 'BATCH_TRG_MS: % ms', ms;\n"
        "END $$;"
    )
    add_code_block(doc, bench_code, indent_cm=0)

    doc.save(output_path)
    print(f"Document saved: {output_path}")

if __name__ == '__main__':
    build_docx("e:/laba2/БСБД_Корецкий_ПС_ЛР2.docx")
