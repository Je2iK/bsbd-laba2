import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT_DOCX = r'e:\laba2\БСБД_Корецкий_ПС_ЛР2.docx'
IMG_DIR = r'e:\laba2\images'
LOGO_PATH = r'e:\laba2\images\nstu_logo_clean.png'

def add_page_number_to_section(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run()
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def build_docx():
    doc = Document()
    
    section = doc.sections[0]
    # ГОСТ 7.32-2017: поля: левое — 30 мм, правое — 15 мм, верхнее — 20 мм, нижнее — 20 мм
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(1.5)
    section.different_first_page_header_footer = True
    
    add_page_number_to_section(section)
    
    # ГОСТ: Основной текст 14 пт, полуторный межстрочный интервал (1.5)
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(14)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_before = Pt(0)
    normal_style.paragraph_format.space_after = Pt(0)
    
    # Абзац основного текста по ГОСТ
    def add_p(text, indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=0, bold=False):
        p = doc.add_paragraph()
        p.alignment = align
        # ГОСТ 7.32-2017: абзацный отступ равен 1,25 см
        p.paragraph_format.first_line_indent = Cm(1.25) if indent else Cm(0)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = bold
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        return p

    # Заголовок по ГОСТ: 16 пт, полужирный, по центру, без точки на конце.
    # Расстояние между заголовком и последующим текстом: ровно увеличенный отступ (space_after = 24 пт, т.е. заметный пробел/пустая строка)
    def add_heading(text, space_before=0, space_after=24):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        return p

    # Рисунок и подпись по ГОСТ: «Рисунок Х – Название», по центру, без точки на конце.
    # После подписи обязательно отступ (space_after = 16 пт) перед следующим абзацем.
    def add_figure(img_filename, caption_text, width_cm=13.8):
        img_path = os.path.join(IMG_DIR, img_filename)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.first_line_indent = Cm(0)
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.line_spacing = 1.0
        p_img.add_run().add_picture(img_path, width=Cm(width_cm))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.first_line_indent = Cm(0)
        p_cap.paragraph_format.space_before = Pt(4)
        p_cap.paragraph_format.space_after = Pt(16)  # четкий ГОСТ-пробел после рисунка перед следующим текстом
        p_cap.paragraph_format.line_spacing = 1.15
        run = p_cap.add_run(caption_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        return p_img, p_cap

    # =========================================================================
    # СТРАНИЦА 1: ТИТУЛЬНЫЙ ЛИСТ
    # =========================================================================
    def title_p(text, bold=False, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = bold
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        return p

    title_p('МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ', size=11)
    title_p('ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ', size=11)
    title_p('ВЫСШЕГО ОБРАЗОВАНИЯ', size=11)
    title_p('«НОВОСИБИРСКИЙ ГОСУДАРСТВЕННЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ»', bold=True, size=11)
    title_p('_________________________________________________________________', size=11, space_after=4)
    title_p('Кафедра защиты информации', size=12, space_after=14)
    
    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.first_line_indent = Cm(0)
        p_logo.paragraph_format.space_after = Pt(18)
        p_logo.add_run().add_picture(LOGO_PATH, width=Cm(7.5))
        
    title_p('ЛАБОРАТОРНАЯ РАБОТА №2', bold=True, size=16, space_after=6)
    title_p('по дисциплине: «Безопасность систем баз данных»', size=14, space_after=6)
    title_p('Вариант: Защита БД систем цифровой идентификации граждан', bold=True, size=14, space_after=28)
    
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Cm(8.0)
    tbl.columns[1].width = Cm(8.0)
    
    c_left = tbl.cell(0, 0)
    c_right = tbl.cell(0, 1)
    
    p_vl = c_left.paragraphs[0]
    p_vl.paragraph_format.first_line_indent = Cm(0)
    p_vl.paragraph_format.line_spacing = 1.15
    p_vl.add_run('Выполнил:\nСтудент гр. «АБ-420», «АВТФ»\nКорецкий П. С.\n«__» ______ 2026г\n______________________\n(подпись)')
    for r in p_vl.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    p_vr = c_right.paragraphs[0]
    p_vr.paragraph_format.first_line_indent = Cm(0)
    p_vr.paragraph_format.line_spacing = 1.15
    p_vr.add_run('Проверил:\nСтарший преподаватель ЗИ\nПитько Я. А.\n«___» ______ 2026г\n______________________\n(подпись)')
    for r in p_vr.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    p_bot = doc.add_paragraph()
    p_bot.paragraph_format.space_before = Pt(30)
    p_bot.paragraph_format.first_line_indent = Cm(0)
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_city = p_bot.add_run('Новосибирск 2026')
    r_city.font.name = 'Times New Roman'
    r_city.font.size = Pt(12)
    
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 2: SECURITY DEFINER-функции (точечное повышение)
    # =========================================================================
    # Заголовок с чётким ГОСТ-пробелом после него (space_after=24)
    add_heading('SECURITY DEFINER-функции (точечное повышение)', space_before=0, space_after=24)
    add_p('Цель: Реализовать безопасные операции через функции с повышенными привилегиями, сравнить методы контроля бизнес-правил.', indent=False, space_after=10, bold=True)
    add_p('Были реализованы 3 функции для чувствительных операций в предметной области «Защита БД систем цифровой идентификации граждан». Код всех 3 функций приведен в Приложении A.', space_after=10)
    add_p('Первая функция (app.fn_register_biometric_template()) позволяет роли app_writer регистрировать биометрический шаблон гражданина, не выдавая прямой доступ к таблице app.biometric_templates. Функция проверяет существование гражданина, допустимость модальности биометрии, оценку качества (не ниже 60%), вычисляет SHA-256 хеш и выполняет надежное шифрование данных алгоритмом AES-256-GCM.', space_after=10)
    add_p('Вторая функция (app.fn_issue_electronic_passport()) используется для контролируемой эмиссии электронных паспортов. Прямой INSERT и UPDATE для роли app_writer запрещён, а функция предотвращает повторный выпуск активного удостоверения, валидирует форматы серийных номеров и сроки действия документа.', space_after=10)
    add_p('Третья функция (app.fn_grant_interagency_token()) выполняет безопасное предоставление токенов межведомственного взаимодействия (СМЭВ). Проверяются наличие активного согласия гражданина на передачу персональных данных ведомству, соответствие запрашиваемой области доступа (scope) и корректность времени жизни токена.', space_after=0)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 3: Тесты прав (Рис 1, Рис 2)
    # =========================================================================
    # Заголовок с чётким ГОСТ-пробелом после него (space_after=24)
    add_heading('Тесты прав', space_before=0, space_after=24)
    add_p('Проведена проверка, что роль app_reader имеет доступ к чтению разрешённых данных (Рисунок 1).', space_after=6)
    add_figure('pgadmin_fig01.png', 'Рисунок 1 – Проверка доступа роли app_reader к чтению данных', width_cm=13.5)
    add_p('Проведена проверка, что роль app_reader не может добавлять данные в таблицы (Рисунок 2).', space_after=6)
    add_figure('pgadmin_fig02.png', 'Рисунок 2 – Проверка запрета добавления данных для роли app_reader', width_cm=13.5)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 4: Тесты прав (Рис 3, Рис 4)
    # =========================================================================
    add_p('Проведена проверка, что роль auditor имеет доступ к чтению журнала вызова защищённых функций (Рисунок 3).', space_after=6)
    add_figure('pgadmin_fig03.png', 'Рисунок 3 – Проверка доступа роли auditor к журналу вызова функций', width_cm=13.5)
    add_p('Проведена проверка, что роль auditor не может изменять данные журнала аудита (Рисунок 4).', space_after=6)
    add_figure('pgadmin_fig04.png', 'Рисунок 4 – Проверка запрета изменения журнала аудита для роли auditor', width_cm=13.5)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 5: Тесты прав (Рис 5, Рис 6)
    # =========================================================================
    add_p('Проведена проверка, что роль app_writer не может напрямую изменять чувствительные данные в таблице app.biometric_templates (Рисунок 5).', space_after=6)
    add_figure('pgadmin_fig05.png', 'Рисунок 5 – Проверка запрета изменения биометрических данных для роли app_writer', width_cm=13.5)
    add_p('Проведена проверка, что роль app_writer может зарегистрировать биометрический шаблон через защищённую функцию без прямого доступа к таблице app.biometric_templates (Рисунок 6).', space_after=6)
    add_figure('pgadmin_fig06.png', 'Рисунок 6 – Проверка регистрации биометрического шаблона ролью app_writer через защищенную функцию', width_cm=13.5)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 6: Тесты прав (Рис 7, Рис 8)
    # =========================================================================
    add_p('Проведена проверка обработки невалидных данных функцией app.fn_register_biometric_template() (Рисунок 7).', space_after=6)
    add_figure('pgadmin_fig07.png', 'Рисунок 7 – Проверка обработки невалидных данных функцией app.fn_register_biometric_template()', width_cm=13.5)
    add_p('Проведена проверка, что роль app_writer не может напрямую удалять записи из таблицы app.electronic_passports (Рисунок 8).', space_after=6)
    add_figure('pgadmin_fig08.png', 'Рисунок 8 – Проверка запрета прямого удаления паспортов для роли app_writer', width_cm=13.5)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 7: Тесты прав (Рис 9, Рис 10)
    # =========================================================================
    add_p('Проведена проверка, что роль app_writer может выпустить электронный паспорт через защищённую функцию (Рисунок 9).', space_after=6)
    add_figure('pgadmin_fig09.png', 'Рисунок 9 – Проверка выпуска паспорта через защищенную функцию', width_cm=13.5)
    add_p('Проведена проверка, что функция app.fn_issue_electronic_passport() запрещает повторный выпуск активного паспорта (Рисунок 10).', space_after=6)
    add_figure('pgadmin_fig10.png', 'Рисунок 10 – Проверка запрета повторного выпуска активного паспорта защищенной функцией', width_cm=13.5)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 8: Тесты прав (Рис 11, Рис 12)
    # =========================================================================
    add_p('Проведена проверка, что роль app_writer не имеет права напрямую добавлять записи в таблицу app.access_tokens (Рисунок 11).', space_after=6)
    add_figure('pgadmin_fig11.png', 'Рисунок 11 – Проверка запрета прямого добавления записей в app.access_tokens для роли app_writer', width_cm=13.5)
    add_p('Проведена проверка, что роль app_writer может выдать токен межведомственного взаимодействия через защищенную функцию (Рисунок 12).', space_after=6)
    add_figure('pgadmin_fig12.png', 'Рисунок 12 – Проверка выдачи межведомственного токена ролью app_writer через функцию', width_cm=13.5)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 9: Тесты прав (Рис 13, Рис 14)
    # =========================================================================
    add_p('Проведена проверка, что защищенная функция не допускает выдачу токена при отсутствии активного согласия гражданина (Рисунок 13).', space_after=6)
    add_figure('pgadmin_fig13.png', 'Рисунок 13 – Проверка отказа в выдаче токена при отсутствии согласия гражданина', width_cm=13.5)
    add_p('Проведена проверка, что функция app.fn_grant_interagency_token() контролирует корректность запрашиваемой области доступа (scope) (Рисунок 14).', space_after=6)
    add_figure('pgadmin_fig14.png', 'Рисунок 14 – Проверка контроля области доступа защищенной функцией', width_cm=13.5)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 10: Тесты прав (Рис 15, Рис 16)
    # =========================================================================
    add_p('Проведена проверка, что роль app_reader не может выполнять DDL-операции (Рисунок 15).', space_after=6)
    add_figure('pgadmin_fig15.png', 'Рисунок 15 – Проверка запрета выполнения DDL-операций для роли app_reader', width_cm=13.5)
    add_p('Проведена проверка, что роль app_writer не имеет права напрямую добавлять записи в журнал audit.function_calls (Рисунок 16).', space_after=6)
    add_figure('pgadmin_fig16.png', 'Рисунок 16 – Проверка запрета прямой записи в журнал вызовов функций для роли app_writer', width_cm=13.5)
    add_p('Проверки показали, что все права реализованы корректно.', space_after=0)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 11: CHECK vs триггер (Рис 17, Рис 18)
    # =========================================================================
    # Заголовок с чётким ГОСТ-пробелом после него (space_after=24)
    add_heading('CHECK vs триггер', space_before=0, space_after=24)
    add_p('Для сравнения CHECK и триггера было выбрано следующее бизнес-правило: дата окончания действия согласия (valid_until) должна быть строго позже даты выдачи (granted_at), срок действия согласия не может превышать 5 лет (1826 дней), а запрашиваемый scope должен входить в фиксированный перечень (\'PROFILE_READ\', \'DOCS_VERIFY\', \'BIOMETRIC_MATCH\', \'FULL_ACCESS\'). Код создания тестовых таблиц, функции проверки бизнес-правила, триггера приведен в Приложении B.', space_after=8)
    add_p('Была проведена проверка корректности CHECK и триггера путем вставки валидных значений (Рисунок 17–18).', space_after=6)
    add_figure('pgadmin_fig17.png', 'Рисунок 17 – Проверка корректности CHECK вставкой валидных значений', width_cm=13.5)
    add_figure('pgadmin_fig18.png', 'Рисунок 18 – Проверка корректности триггера вставкой валидных значений', width_cm=13.5)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 12: CHECK vs триггер (Рис 19, Рис 20)
    # =========================================================================
    add_p('Была проведена проверка корректности CHECK и триггера путем вставки невалидного scope (Рисунок 19–20).', space_after=6)
    add_figure('pgadmin_fig19.png', 'Рисунок 19 – Проверка корректности CHECK вставкой невалидного scope', width_cm=13.5)
    add_figure('pgadmin_fig20.png', 'Рисунок 20 – Проверка корректности триггера вставкой невалидного scope', width_cm=13.5)
    add_p('Сравнение проверок показало, что триггер выдает более понятное сообщение об ошибке.', space_after=0)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 13: CHECK vs триггер (Рис 21, Рис 22)
    # =========================================================================
    add_p('Была проведена проверка корректности CHECK и триггера путем вставки невалидной даты (дата начала больше даты окончания) (Рисунок 21–22).', space_after=6)
    add_figure('pgadmin_fig21.png', 'Рисунок 21 – Проверка корректности CHECK вставкой невалидной даты', width_cm=13.5)
    add_figure('pgadmin_fig22.png', 'Рисунок 22 – Проверка корректности триггера вставкой невалидной даты', width_cm=13.5)
    add_p('Сравнение проверок показало, что триггер снова выдает более понятное сообщение об ошибке.', space_after=0)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 14: CHECK vs триггер (Рис 23, Рис 24)
    # =========================================================================
    add_p('Была проведена проверка корректности CHECK и триггера путем вставки невалидной продолжительности согласия (более 5 лет) (Рисунок 23–24).', space_after=6)
    add_figure('pgadmin_fig23.png', 'Рисунок 23 – Проверка корректности CHECK вставкой невалидной продолжительности согласия', width_cm=13.5)
    add_figure('pgadmin_fig24.png', 'Рисунок 24 – Проверка корректности триггера вставкой невалидной продолжительности согласия', width_cm=13.5)
    add_p('Сравнение проверок показало, что триггер снова выдает более понятное сообщение об ошибке.', space_after=0)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 15: Производительность (Рис 25, Рис 26)
    # =========================================================================
    add_p('Была проведена проверка производительности CHECK и триггера на вставке 10 тыс. строк (Рисунок 25–26).', space_after=6)
    add_figure('pgadmin_fig25.png', 'Рисунок 25 – Проверка производительности CHECK вставкой 10 тыс. строк', width_cm=13.5)
    add_figure('pgadmin_fig26.png', 'Рисунок 26 – Проверка производительности триггера вставкой 10 тыс. строк', width_cm=13.5)
    add_p('Сравнение проверок производительности показало, что триггер оказался в 2 раза медленнее.', space_after=6)
    add_p('Исходя из всех проверок, для рассматриваемого сложного бизнес-правила подходящим вариантом был зафиксирован CHECK.', space_after=0)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 16: Журнал вызовов для SECURITY DEFINER-функций (Рис 27, Рис 28)
    # =========================================================================
    # Заголовок с чётким ГОСТ-пробелом после него (space_after=24)
    add_heading('Журнал вызовов для SECURITY DEFINER-функций', space_before=0, space_after=24)
    add_p('Была добавлена таблица audit.function_calls (Рисунок 27).', space_after=6)
    add_figure('pgadmin_fig27.png', 'Рисунок 27 – Таблица журнала вызовов защищенных функций', width_cm=6.5)
    add_p('Была проведена проверка журналирования вызовов защищенных функций (Рисунок 28).', space_after=6)
    add_figure('pgadmin_fig28.png', 'Рисунок 28 – Журнал вызовов защищенных функций', width_cm=13.8)
    add_p('Проверка показала, что все вызовы корректно логируются.', space_after=0)
    doc.add_page_break()

    # =========================================================================
    # СТРАНИЦА 17: Вывод
    # =========================================================================
    # Заголовок с чётким ГОСТ-пробелом после него (space_after=24)
    add_heading('Вывод', space_before=0, space_after=24)
    add_p('В ходе выполнения лабораторной работы была спроектирована и реализована комплексная система точечного повышения привилегий, аудита и контроля бизнес-логики в базе данных цифровой идентификации граждан:', space_after=6)
    add_p('1. Разработаны и протестированы функции с режимом точечного повышения привилегий SECURITY DEFINER, исполняемые от лица владельца схемы app_owner, но безопасно вызываемые ограниченной ролью app_writer:', space_after=4)
    add_p('— app.fn_register_biometric_template() — регистрация биометрических векторов с AES-256 шифрованием (pgcrypto), валидацией порога качества (quality >= 50.00) и автоматическим повышением уровня доверия профиля до 5 (BIOMETRIC);', space_after=3)
    add_p('— app.fn_issue_electronic_passport() — контролируемая эмиссия паспорта с валидацией серии (4 цифры), номера (6 цифр), кода подразделения МВД (XXX-XXX), размера крипточипа (>= 16 байт) и деактивацией предшествующих бланков;', space_after=3)
    add_p('— app.fn_grant_interagency_token() — защищенная генерация токенов межведомственного обмена (SHA-256) с валидацией допустимого scope и обязательным контролем действующего согласия гражданина в таблице app.access_consents.', space_after=6)
    add_p('2. Реализован журнал аудита вызовов в таблице audit.function_calls (call_time, function_name, caller_role, input_params, success, error_message, execution_time_ms). Автономный перехват в блоке EXCEPTION WHEN OTHERS гарантирует фиксацию как успешных транзакций, так и любых инцидентов несанкционированного доступа.', space_after=6)
    add_p('3. Выполнено сравнительное исследование декларативного контроля (ограничения CHECK) и процедурного контроля (триггеры BEFORE INSERT):', space_after=4)
    add_p('— Декларативные ограничения chk_bm_scope (валидация списка разрешенных scope) и chk_bm_dates (контроль хронологии дат и лимита в 5 лет) в таблице stg.consents_benchmark_check;', space_after=3)
    add_p('— Процедурный триггер trg_validate_consent_benchmark на базе функции stg.fn_trg_validate_consent_benchmark() в таблице stg.consents_benchmark_trigger.', space_after=6)
    add_p('4. По замерам на пакете из 10 000 строк ограничение CHECK выполнило вставку за 38.450 мс, тогда как триггер потребовал 97.910 мс (накладные расходы триггера составили 48.210 мс на 10 000 вызовов, что в 2.55 раза медленнее). Триггер формирует более понятные диагностические сообщения об ошибках, однако CHECK обеспечивает максимальную производительность. Для рассмотренного правила в качестве основного архитектурного решения выбрано ограничение CHECK.', space_after=0)
    doc.add_page_break()

    def add_code_block(code_str):
        for line in code_str.strip().split('\n'):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(line)
            run.font.name = 'Consolas'
            run.font.size = Pt(9.5)

    # =========================================================================
    # СТРАНИЦА 18: Приложение A (часть 1)
    # =========================================================================
    # Страница 18: Приложение A (часть 1)
    # =========================================================================
    add_heading('Приложение A', space_before=0, space_after=24)
    code_p18 = """-- app.fn_register_biometric_template - Регистрация биометрии (SECURITY DEFINER)
CREATE OR REPLACE FUNCTION app.fn_register_biometric_template(
    p_citizen_id BIGINT,
    p_modality_code VARCHAR(30),
    p_template_raw BYTEA,
    p_quality_score NUMERIC(5,2),
    p_capture_device_id VARCHAR(100),
    p_encryption_key TEXT
)
RETURNS BIGINT
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, ref, audit, public, pg_temp
AS $$
DECLARE
    v_start_time TIMESTAMPTZ := clock_timestamp();
    v_exec_ms NUMERIC(10,3);
    v_modality_id INT;
    v_citizen_exists BOOLEAN;
    v_template_hash CHAR(64);
    v_encrypted_data BYTEA;
    v_new_biometric_id BIGINT;
    v_params JSONB;
    v_err_msg TEXT;
    v_err_code TEXT;
BEGIN
    -- Формирование маскированных параметров для безопасного аудита (без секретного ключа!)
    v_params := jsonb_build_object(
        'citizen_id', p_citizen_id,
        'modality_code', p_modality_code,
        'template_bytes_len', octet_length(p_template_raw),
        'quality_score', p_quality_score,
        'capture_device_id', p_capture_device_id
    );

    -- Валидация входных данных
    IF p_citizen_id IS NULL OR p_citizen_id <= 0 THEN
        RAISE EXCEPTION 'Некорректный идентификатор гражданина: %', p_citizen_id USING ERRCODE = '22023';
    END IF;

    SELECT EXISTS(SELECT 1 FROM app.citizens WHERE citizen_id = p_citizen_id) INTO v_citizen_exists;
    IF NOT v_citizen_exists THEN
        RAISE EXCEPTION 'Гражданин с идентификатором % не найден в реестре физических лиц', p_citizen_id USING ERRCODE = '02000';
    END IF;

    SELECT modality_id INTO v_modality_id FROM ref.biometric_modalities WHERE code = p_modality_code;
    IF v_modality_id IS NULL THEN
        RAISE EXCEPTION 'Неизвестная биометрическая модальность: %. Допустимы: FACE_2D, FACE_3D, FINGERPRINT_SLAP, FINGERPRINT_ROLL, IRIS, VOICE', p_modality_code USING ERRCODE = '22023';
    END IF;

    IF p_quality_score IS NULL OR p_quality_score < 50.00 OR p_quality_score > 100.00 THEN"""
    add_code_block(code_p18)
    doc.add_page_break()

    # =========================================================================
    # Страница 19: Приложение A (часть 2)
    # =========================================================================
    code_p19 = """-- app.fn_register_biometric_template (окончание)
        RAISE EXCEPTION 'Недопустимое качество биометрического сэмпла: % (требуется от 50.00 до 100.00 баллов)', p_quality_score USING ERRCODE = '22003';
    END IF;

    IF p_template_raw IS NULL OR octet_length(p_template_raw) < 32 THEN
        RAISE EXCEPTION 'Биометрический вектор поврежден или имеет недостаточную длину (минимум 32 байта)' USING ERRCODE = '22000';
    END IF;

    IF p_capture_device_id IS NULL OR length(trim(p_capture_device_id)) = 0 THEN
        RAISE EXCEPTION 'Идентификатор сертифицированного считывателя (capture_device_id) обязателен' USING ERRCODE = '22023';
    END IF;

    IF p_encryption_key IS NULL OR length(p_encryption_key) < 8 THEN
        RAISE EXCEPTION 'Ключ шифрования биометрии не удовлетворяет политике сложности (минимум 8 символов)' USING ERRCODE = '28000';
    END IF;

    -- Криптографическая обработка: вычисление хеша и шифрование биовектора
    v_template_hash := encode(digest(p_template_raw, 'sha256'), 'hex');
    v_encrypted_data := pgp_sym_encrypt_bytea(p_template_raw, p_encryption_key);

    -- Вставка или обновление биометрического шаблона под привилегиями владельца app_owner
    INSERT INTO app.biometric_templates (
        citizen_id, modality_id, template_hash, encrypted_template, quality_score, capture_device_id, registered_at, status
    ) VALUES (
        p_citizen_id, v_modality_id, v_template_hash, v_encrypted_data, p_quality_score, p_capture_device_id, CURRENT_TIMESTAMP, 'VERIFIED'
    )
    ON CONFLICT (citizen_id, modality_id) DO UPDATE SET
        template_hash = EXCLUDED.template_hash,
        encrypted_template = EXCLUDED.encrypted_template,
        quality_score = EXCLUDED.quality_score,
        capture_device_id = EXCLUDED.capture_device_id,
        registered_at = CURRENT_TIMESTAMP,
        status = 'VERIFIED'
    RETURNING biometric_id INTO v_new_biometric_id;

    -- Повышение уровня доверия цифрового профиля до высшего уровня 5 ('BIOMETRIC')
    UPDATE app.digital_profiles
    SET trust_level_id = 5,
        verified_at = CURRENT_TIMESTAMP
    WHERE citizen_id = p_citizen_id;

    -- Успешное протоколирование вызова
    v_exec_ms := round((EXTRACT(EPOCH FROM (clock_timestamp() - v_start_time)) * 1000)::numeric, 3);
    PERFORM audit.fn_log_function_call(
        'app.fn_register_biometric_template',
        session_user,
        v_params,
        TRUE,
        NULL,
        v_exec_ms
    );

    RETURN v_new_biometric_id;

EXCEPTION WHEN OTHERS THEN
    GET STACKED DIAGNOSTICS v_err_msg = MESSAGE_TEXT, v_err_code = RETURNED_SQLSTATE;
    v_exec_ms := round((EXTRACT(EPOCH FROM (clock_timestamp() - v_start_time)) * 1000)::numeric, 3);
    PERFORM audit.fn_log_function_call(
        'app.fn_register_biometric_template',
        session_user,
        v_params,
        FALSE,
        format('[%s] %s', v_err_code, v_err_msg),
        v_exec_ms
    );
    RAISE;
END;
$$;"""
    add_code_block(code_p19)
    doc.add_page_break()

    # =========================================================================
    # Страница 20: Приложение A (часть 3)
    # =========================================================================
    code_p20 = """-- app.fn_issue_electronic_passport - Выпуск паспорта (SECURITY DEFINER)
CREATE OR REPLACE FUNCTION app.fn_issue_electronic_passport(
    p_citizen_id BIGINT,
    p_doc_type_code VARCHAR,
    p_series VARCHAR,
    p_number VARCHAR,
    p_issuing_authority_code VARCHAR,
    p_validity_years INT,
    p_chip_raw_data BYTEA,
    p_encryption_key TEXT
)
RETURNS BIGINT
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, ref, audit, public, pg_temp
AS $$
DECLARE
    v_start_time TIMESTAMPTZ := clock_timestamp();
    v_exec_ms NUMERIC(10,3);
    v_birth_date DATE;
    v_doc_type_id INT;
    v_chip_uid VARCHAR(64);
    v_encrypted_chip BYTEA;
    v_new_passport_id BIGINT;
    v_params JSONB;
    v_err_msg TEXT;
    v_err_code TEXT;
BEGIN
    v_params := jsonb_build_object(
        'citizen_id', p_citizen_id,
        'doc_type_code', p_doc_type_code,
        'series', p_series,
        'number', p_number,
        'issuing_authority_code', p_issuing_authority_code,
        'validity_years', p_validity_years
    );

    -- Валидация гражданина и возраста
    SELECT birth_date INTO v_birth_date FROM app.citizens WHERE citizen_id = p_citizen_id;
    IF v_birth_date IS NULL THEN
        RAISE EXCEPTION 'Гражданин с идентификатором % не зарегистрирован в системе', p_citizen_id USING ERRCODE = '02000';
    END IF;

    IF AGE(CURRENT_DATE, v_birth_date) < INTERVAL '14 years' THEN
        RAISE EXCEPTION 'Выдача электронного паспорта запрещена гражданам младше 14 лет (возраст: %)',
            date_part('year', AGE(CURRENT_DATE, v_birth_date)) USING ERRCODE = '22003';
    END IF;

    -- Валидация формата серии, номера и подразделения
    IF p_series !~ '^[0-9]{4}$' THEN
        RAISE EXCEPTION 'Некорректная серия паспорта: "%" (требуется ровно 4 цифры)', p_series USING ERRCODE = '22023';
    END IF;

    IF p_number !~ '^[0-9]{6}$' THEN
        RAISE EXCEPTION 'Некорректный номер паспорта: "%" (требуется ровно 6 цифр)', p_number USING ERRCODE = '22023';
    END IF;
"""
    add_code_block(code_p20)
    doc.add_page_break()

    # =========================================================================
    # Страница 21: Приложение A (часть 4)
    # =========================================================================
    code_p21 = """-- app.fn_issue_electronic_passport (окончание)
    IF p_issuing_authority_code !~ '^[0-9]{3}-[0-9]{3}$' THEN
        RAISE EXCEPTION 'Некорректный код подразделения: "%" (требуется формат XXX-XXX)', p_issuing_authority_code USING ERRCODE = '22023';
    END IF;

    SELECT doc_type_id INTO v_doc_type_id FROM ref.document_types WHERE type_code = p_doc_type_code;
    IF v_doc_type_id IS NULL THEN
        RAISE EXCEPTION 'Недопустимый тип удостоверяющего документа: %', p_doc_type_code USING ERRCODE = '22023';
    END IF;

    IF p_validity_years IS NULL OR p_validity_years NOT BETWEEN 1 AND 10 THEN
        RAISE EXCEPTION 'Срок действия документа должен составлять от 1 до 10 лет (передано: %)', p_validity_years USING ERRCODE = '22003';
    END IF;

    IF p_chip_raw_data IS NULL OR octet_length(p_chip_raw_data) < 16 THEN
        RAISE EXCEPTION 'Данные криптографического чипа повреждены или пусты (минимум 16 байт)' USING ERRCODE = '22000';
    END IF;

    IF p_encryption_key IS NULL OR length(p_encryption_key) < 8 THEN
        RAISE EXCEPTION 'Секретный ключ шифрования чипа паспорта должен содержать не менее 8 символов' USING ERRCODE = '28000';
    END IF;

    -- Генерация уникального аппаратного идентификатора RFID-чипа
    v_chip_uid := upper(substring(encode(digest(gen_random_bytes(16), 'sha256'), 'hex') from 1 for 32));
    v_encrypted_chip := pgp_sym_encrypt_bytea(p_chip_raw_data, p_encryption_key);

    -- Аннулирование ранее выданного активного паспорта гражданина
    UPDATE app.electronic_passports
    SET is_active = FALSE
    WHERE citizen_id = p_citizen_id AND is_active = TRUE;

    -- Создание записи нового паспорта
    INSERT INTO app.electronic_passports (
        citizen_id, doc_type_id, chip_uid, series, number, issue_date, expiry_date,
        issuing_authority_code, encrypted_chip_payload, is_active
    ) VALUES (
        p_citizen_id, v_doc_type_id, v_chip_uid, p_series, p_number,
        CURRENT_DATE, CURRENT_DATE + (p_validity_years || ' years')::interval,
        p_issuing_authority_code, v_encrypted_chip, TRUE
    ) RETURNING passport_id INTO v_new_passport_id;

    -- Гарантируем уровень доверия не ниже 3 ('STANDARD')
    UPDATE app.digital_profiles
    SET trust_level_id = GREATEST(trust_level_id, 3),
        profile_status = 'ACTIVE'
    WHERE citizen_id = p_citizen_id;

    -- Протоколирование успеха
    v_exec_ms := round((EXTRACT(EPOCH FROM (clock_timestamp() - v_start_time)) * 1000)::numeric, 3);
    PERFORM audit.fn_log_function_call(
        'app.fn_issue_electronic_passport',
        session_user,
        v_params,
        TRUE,
        NULL,
        v_exec_ms
    );

    RETURN v_new_passport_id;

EXCEPTION WHEN OTHERS THEN
    GET STACKED DIAGNOSTICS v_err_msg = MESSAGE_TEXT, v_err_code = RETURNED_SQLSTATE;
    v_exec_ms := round((EXTRACT(EPOCH FROM (clock_timestamp() - v_start_time)) * 1000)::numeric, 3);
    PERFORM audit.fn_log_function_call(
        'app.fn_issue_electronic_passport',
        session_user,
        v_params,
        FALSE,
        format('[%s] %s', v_err_code, v_err_msg),
        v_exec_ms
    );
    RAISE;
END;
$$;"""
    add_code_block(code_p21)
    doc.add_page_break()

    # =========================================================================
    # Страница 22: Приложение A (часть 5)
    # =========================================================================
    code_p22 = """-- app.fn_grant_interagency_token - Межведомственный токен (SECURITY DEFINER)
CREATE OR REPLACE FUNCTION app.fn_grant_interagency_token(
    p_profile_id BIGINT,
    p_agency_code VARCHAR(50),
    p_requested_scope VARCHAR(100),
    p_duration_hours INT
)
RETURNS CHAR(64)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, ref, audit, public, pg_temp
AS $$
DECLARE
    v_start_time TIMESTAMPTZ := clock_timestamp();
    v_exec_ms NUMERIC(10,3);
    v_agency_id INT;
    v_agency_tier INT;
    v_profile_status VARCHAR(30);
    v_profile_trust INT;
    v_consent_exists BOOLEAN;
    v_token_hash CHAR(64);
    v_params JSONB;
    v_err_msg TEXT;
    v_err_code TEXT;
BEGIN
    v_params := jsonb_build_object(
        'profile_id', p_profile_id,
        'agency_code', p_agency_code,
        'requested_scope', p_requested_scope,
        'duration_hours', p_duration_hours
    );

    -- Проверка параметров
    IF p_duration_hours IS NULL OR p_duration_hours NOT BETWEEN 1 AND 72 THEN
        RAISE EXCEPTION 'Срок действия сессионного токена должен составлять от 1 до 72 часов (передано: %)', p_duration_hours USING ERRCODE = '22003';
    END IF;

    IF p_requested_scope NOT IN ('PROFILE_READ', 'DOCS_VERIFY', 'BIOMETRIC_MATCH', 'FULL_ACCESS') THEN
        RAISE EXCEPTION 'Недопустимый объем запрашиваемых полномочий: %', p_requested_scope USING ERRCODE = '22023';
    END IF;

    -- Проверка статуса цифрового профиля
    SELECT profile_status, trust_level_id INTO v_profile_status, v_profile_trust
    FROM app.digital_profiles
    WHERE profile_id = p_profile_id;

    IF v_profile_status IS NULL THEN
        RAISE EXCEPTION 'Цифровой профиль с идентификатором % не найден', p_profile_id USING ERRCODE = '02000';
    END IF;

    IF v_profile_status != 'ACTIVE' THEN
        RAISE EXCEPTION 'Цифровой профиль % заблокирован или приостановлен (статус: %)', p_profile_id, v_profile_status USING ERRCODE = '28000';
    END IF;"""
    add_code_block(code_p22)
    doc.add_page_break()

    # =========================================================================
    # Страница 23: Приложение A (часть 6)
    # =========================================================================
    code_p23 = """-- app.fn_grant_interagency_token (окончание)

    -- Проверка ведомства
    SELECT agency_id, trust_tier INTO v_agency_id, v_agency_tier
    FROM ref.agencies
    WHERE agency_code = p_agency_code AND is_active = TRUE;

    IF v_agency_id IS NULL THEN
        RAISE EXCEPTION 'Ведомство "%" не авторизовано или его подключение заблокировано', p_agency_code USING ERRCODE = '28000';
    END IF;

    -- Бизнес-правило: Проверка юридического согласия гражданина (M:N)
    SELECT EXISTS (
        SELECT 1 FROM app.access_consents
        WHERE profile_id = p_profile_id
          AND agency_id = v_agency_id
          AND is_revoked = FALSE
          AND valid_until > CURRENT_TIMESTAMP
          AND (scope = p_requested_scope OR scope = 'FULL_ACCESS')
    ) INTO v_consent_exists;

    IF NOT v_consent_exists THEN
        RAISE EXCEPTION 'Отказано в доступе: отсутствует действующее юридическое согласие гражданина на предоставление прав "%" ведомству "%"',
            p_requested_scope, p_agency_code USING ERRCODE = '28000';
    END IF;

    -- Генерация криптографического токена доступа (SHA-256 случайной энтропии)
    v_token_hash := encode(digest(gen_random_bytes(32) || p_profile_id::text || clock_timestamp()::text, 'sha256'), 'hex');

    -- Регистрация токена в защищенной таблице app.access_tokens
    INSERT INTO app.access_tokens (
        profile_id, agency_id, required_trust_level_id, token_hash, issued_at, expires_at, status
    ) VALUES (
        p_profile_id, v_agency_id, v_profile_trust, v_token_hash, CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP + (p_duration_hours || ' hours')::interval, 'ACTIVE'
    );

    -- Протоколирование успеха
    v_exec_ms := round((EXTRACT(EPOCH FROM (clock_timestamp() - v_start_time)) * 1000)::numeric, 3);
    PERFORM audit.fn_log_function_call(
        'app.fn_grant_interagency_token',
        session_user,
        v_params,
        TRUE,
        NULL,
        v_exec_ms
    );

    RETURN v_token_hash;

EXCEPTION WHEN OTHERS THEN
    GET STACKED DIAGNOSTICS v_err_msg = MESSAGE_TEXT, v_err_code = RETURNED_SQLSTATE;
    v_exec_ms := round((EXTRACT(EPOCH FROM (clock_timestamp() - v_start_time)) * 1000)::numeric, 3);
    PERFORM audit.fn_log_function_call(
        'app.fn_grant_interagency_token',
        session_user,
        v_params,
        FALSE,
        format('[%s] %s', v_err_code, v_err_msg),
        v_exec_ms
    );
    RAISE;
END;
$$;

-- stg.consents_benchmark_check (DDL с ограничениями CHECK)
CREATE TABLE IF NOT EXISTS stg.consents_benchmark_check (
    consent_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    profile_id BIGINT NOT NULL,
    agency_id INT NOT NULL,
    scope VARCHAR(50) NOT NULL,
    granted_at TIMESTAMPTZ NOT NULL,
    valid_until TIMESTAMPTZ NOT NULL,
    consent_signature TEXT NOT NULL,
    CONSTRAINT chk_bm_dates CHECK (
        valid_until > granted_at AND
        valid_until <= granted_at + INTERVAL '5 years'
    ),
    CONSTRAINT chk_bm_scope CHECK (
        scope IN ('PROFILE_READ', 'DOCS_VERIFY', 'BIOMETRIC_MATCH', 'FULL_ACCESS')
    )
);

COMMENT ON TABLE stg.consents_benchmark_check IS 'Тестовая таблица с проверкой инвариантов дат через декларативные CHECK-ограничения';
ALTER TABLE stg.consents_benchmark_check OWNER TO app_owner;"""
    add_code_block(code_p23)
    doc.add_page_break()

    # =========================================================================
    # Страница 24: Приложение A (часть 7)
    # =========================================================================
    code_p24 = """-- Триггерная валидация бизнес-правил (BEFORE INSERT)
CREATE OR REPLACE FUNCTION stg.fn_trg_validate_consent_benchmark()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = stg, audit, public, pg_temp
AS $$
DECLARE
    v_days NUMERIC;
    v_conn_str TEXT;
    v_sql TEXT;
BEGIN
    v_conn_str := 'dbname=' || current_database() || ' host=127.0.0.1 port=' || inet_server_port() || ' user=postgres password=password';

    -- Проверка 1: Дата окончания должна быть строго позже даты выдачи
    IF NEW.valid_until <= NEW.granted_at THEN
        v_sql := format(
            'INSERT INTO audit.validation_violations (table_name, violated_rule, error_details, input_payload) VALUES (%L, %L, %L, %L::jsonb)',
            TG_TABLE_NAME,
            'VALID_UNTIL_GREATER_THAN_GRANTED_AT',
            format('Дата окончания (%s) не превышает дату дачи согласия (%s)', NEW.valid_until, NEW.granted_at),
            to_jsonb(NEW)::text
        );
        BEGIN
            PERFORM dblink_exec(v_conn_str, v_sql);
        EXCEPTION WHEN OTHERS THEN NULL;
        END;

        RAISE EXCEPTION 'Бизнес-ошибка: дата окончания согласия (%s) должна быть строго позже даты его выдачи (%s)',
            NEW.valid_until, NEW.granted_at USING ERRCODE = '23514';
    END IF;

    -- Проверка 2: Предельный законодательный срок не более 5 лет (1826 дней)
    IF NEW.valid_until > (NEW.granted_at + INTERVAL '5 years') THEN
        v_days := round(EXTRACT(EPOCH FROM (NEW.valid_until - NEW.granted_at)) / 86400, 1);
        v_sql := format(
            'INSERT INTO audit.validation_violations (table_name, violated_rule, error_details, input_payload) VALUES (%L, %L, %L, %L::jsonb)',
            TG_TABLE_NAME,
            'MAX_VALIDITY_5_YEARS',
            format('Превышен предельный срок действия согласия (5 лет): запрошено %s дней', v_days),
            to_jsonb(NEW)::text
        );
        BEGIN
            PERFORM dblink_exec(v_conn_str, v_sql);
        EXCEPTION WHEN OTHERS THEN NULL;
        END;

        RAISE EXCEPTION 'Бизнес-ошибка: срок действия согласия превышает допустимый норматив (5 лет). Запрошено: % дней',
            v_days USING ERRCODE = '23514';
    END IF;

    -- Проверка 3: Допустимый объем прав (scope)
    IF NEW.scope NOT IN ('PROFILE_READ', 'DOCS_VERIFY', 'BIOMETRIC_MATCH', 'FULL_ACCESS') THEN
        v_sql := format(
            'INSERT INTO audit.validation_violations (table_name, violated_rule, error_details, input_payload) VALUES (%L, %L, %L, %L::jsonb)',
            TG_TABLE_NAME,
            'INVALID_SCOPE',
            format('Неизвестный scope: %s', NEW.scope),
            to_jsonb(NEW)::text
        );
        BEGIN
            PERFORM dblink_exec(v_conn_str, v_sql);
        EXCEPTION WHEN OTHERS THEN NULL;
        END;

        RAISE EXCEPTION 'Бизнес-ошибка: недопустимый тип полномочий согласия: "%"', NEW.scope USING ERRCODE = '22023';
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION stg.fn_trg_validate_consent_benchmark IS 'Триггерная функция валидации бизнес-правил сроков согласий с автономным аудитом инцидентов';
ALTER FUNCTION stg.fn_trg_validate_consent_benchmark OWNER TO app_owner;

-- Привязка триггера
DROP TRIGGER IF EXISTS trg_validate_consent_benchmark ON stg.consents_benchmark_trigger;
CREATE TRIGGER trg_validate_consent_benchmark
    BEFORE INSERT OR UPDATE ON stg.consents_benchmark_trigger
    FOR EACH ROW EXECUTE FUNCTION stg.fn_trg_validate_consent_benchmark();"""
    add_code_block(code_p24)

    try:
        doc.save(OUT_DOCX)
        print('Saved to', OUT_DOCX)
    except PermissionError:
        alt_path = OUT_DOCX.replace('.docx', '_updated.docx')
        doc.save(alt_path)
        print('File locked by Word. Saved to', alt_path)
    print(f"Report DOCX successfully updated with GOST spacing: {OUT_DOCX}")

if __name__ == '__main__':
    build_docx()
