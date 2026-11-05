# -*- coding: utf-8 -*-
"""
Natural Flow Build:
- No artificial pagebreaks every 2 figures
- 3 to 4 compact figures fit naturally per page (no half-empty pages)
- Margins: 3.0cm left, 1.5cm right, 2.0cm top, 2.0cm bottom
- Text: 14pt Times New Roman, 1.5 line spacing, 1.25cm indent, justified
- Captions: 14pt Times New Roman, centered
- Empty line after every caption
- Conclusion on its own page: 3 continuous analytical paragraphs, ZERO lists
- Title page: non-flat, NSTU logo from LR1, Питько Я. А., variant 12
- Appendices: Приложение А and Приложение Б on their own pages
"""

import os
import docx
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT_DOCX = r'e:\laba2\БСБД_Корецкий_ПС_ЛР2.docx'
OUT_TYP = r'e:\laba2\report.typ'
OUT_PDF = r'e:\laba2\БСБД_Корецкий_ПС_ЛР2.pdf'
IMG_DIR = r'e:\laba2\images'
LOGO_PATH = r'e:\laba2\images\nstu_logo.png'

with open(r'e:\laba2\migrations\000008_security_definer_functions.up.sql', 'r', encoding='utf-8') as f:
    SQL_APP_A = f.read().strip()

with open(r'e:\laba2\migrations\000009_check_vs_trigger_benchmarks.up.sql', 'r', encoding='utf-8') as f:
    SQL_APP_B = f.read().strip()

# List of figures and their domain-specific descriptions
FIGURE_DATA_SECTION_1 = [
    (
        'Учетная запись app_reader эмулирует оператора МФЦ, обладающего правами только на просмотр неконфиденциальных профилей. Для верификации запрета деструктивных действий от имени данной роли выполнен запрос на модификацию таблицы биометрических параметров (Рисунок 1). СУБД штатно пресекла операцию ошибкой отсутствия привилегий.',
        'pgadmin_fig01.png',
        'Рисунок 1 – Попытка изменения данных ролью app_reader'
    ),
    (
        'В целях предотвращения несанкционированного профилирования граждан операторам запрещено прямое чтение биометрических дескрипторов. Запрос SELECT к таблице app.biometric_templates был заблокирован механизмами разграничения доступа PostgreSQL (Рисунок 2).',
        'pgadmin_fig02.png',
        'Рисунок 2 – Попытка чтения биометрических шаблонов ролью app_reader'
    ),
    (
        'Профиль сотрудника службы безопасности auditor предназначен для мониторинга событий и лишен доступа к персональным документам. Попытка чтения паспортных данных граждан от имени аудитора завершилась отказом в доступе (Рисунок 3), подтверждая соблюдение принципа разделения обязанностей.',
        'pgadmin_fig03.png',
        'Рисунок 3 – Попытка чтения паспортов ролью auditor'
    ),
    (
        'Для гарантии неизменяемости доказательной базы расследований проверена защита структуры журнала аудита: попытка учетной записи auditor удалить системную таблицу аудита была отклонена ядром СУБД (Рисунок 4).',
        'pgadmin_fig04.png',
        'Рисунок 4 – Попытка изменения структуры таблиц аудитором'
    ),
    (
        'Сервисная роль веб-портала app_writer не имеет прямых прав вставки в хранилище биометрии во избежание обхода криптографических модулей. Попытка прямого выполнения инструкции INSERT в таблицу app.biometric_templates заблокирована политикой прав (Рисунок 5).',
        'pgadmin_fig05.png',
        'Рисунок 5 – Блокировка прямой вставки биометрии ролью app_writer'
    ),
    (
        'Аналогичным образом предотвращается подмена существующих биометрических векторов: команда UPDATE от лица сервиса app_writer отклонена СУБД (Рисунок 6).',
        'pgadmin_fig06.png',
        'Рисунок 6 – Отклонение попытки модификации биометрии учетной записью app_writer'
    ),
    (
        'Легитимная регистрация шаблона лица выполнена через шлюзовую функцию app.fn_register_biometric_template(), которая в контексте app_owner зашифровала вектор ключом AES-256 и внесла запись в защищенную таблицу (Рисунок 7).',
        'pgadmin_fig07.png',
        'Рисунок 7 – Успешная регистрация биометрии через SECURITY DEFINER'
    ),
    (
        'Контроль целостности реестра электронных паспортов подтвержден блокировкой прямой вставки: попытка сервисной роли app_writer добавить запись в обход процедуры выпуска паспорта пресечена СУБД (Рисунок 8).',
        'pgadmin_fig08.png',
        'Рисунок 8 – Блокировка добавления паспорта ролью app_writer'
    ),
    (
        'Попытка прямой модификации реквизитов выданного паспорта гражданина ролью app_writer отклонена СУБД (Рисунок 9), исключая подделку серии и номера удостоверения личности.',
        'pgadmin_fig09.png',
        'Рисунок 9 – Запрет редактирования паспорта сервисной ролью'
    ),
    (
        'Регламентная выдача электронного паспорта успешно осуществлена через функцию app.fn_issue_electronic_passport(), которая проверила маску серии, номера, код ведомства и зафиксировала защищенный документ (Рисунок 10).',
        'pgadmin_fig10.png',
        'Рисунок 10 – Выдача электронного паспорта через защищенный интерфейс'
    ),
    (
        'Прямая запись токенов доступа в таблицу app.access_tokens со стороны app_writer запрещена, что предотвращает несанкционированную раздачу полномочий внешним информационным системам (Рисунок 11).',
        'pgadmin_fig11.png',
        'Рисунок 11 – Запрет прямой вставки токена доступа ролью app_writer'
    ),
    (
        'Защита жизненного цикла сессий подтверждена блокировкой прямого изменения статуса токена: инструкция UPDATE для продления отозванного токена завершилась ошибкой прав доступа (Рисунок 12).',
        'pgadmin_fig12.png',
        'Рисунок 12 – Блокировка изменения статуса токена учетной записью app_writer'
    ),
    (
        'Выпуск токена авторизации ведомству МВД России выполнен через процедуру app.fn_grant_interagency_token(), подтвердившую наличие действующего согласия гражданина в app.access_consents (Рисунок 13).',
        'pgadmin_fig13.png',
        'Рисунок 13 – Санкционированная генерация межведомственного токена'
    ),
    (
        'Попытка выпуска токена с недопустимым объемом полномочий (INVALID_SCOPE) перехвачена входным валидатором функции с возвратом диагностического исключения (Рисунок 14).',
        'pgadmin_fig14.png',
        'Рисунок 14 – Отклонение запроса токена с недопустимым уровнем полномочий'
    ),
    (
        'Целостность схемы базы данных подтверждена попыткой создания таблицы непривилегированным пользователем app_reader: операция CREATE TABLE отклонена ядром PostgreSQL (Рисунок 15).',
        'pgadmin_fig15.png',
        'Рисунок 15 – Блокировка выполнения DDL-запроса непривилегированной ролью'
    ),
    (
        'Гарантия неотказуемости действий подтверждена выборкой из системного журнала audit.function_calls, зафиксировавшего все вызовы функций безопасности с указанием вызывающей роли и переданных аргументов (Рисунок 16).',
        'pgadmin_fig16.png',
        'Рисунок 16 – Фиксация вызовов функций в системном журнале аудита'
    )
]

FIGURE_DATA_SECTION_2 = [
    (
        'Вставка корректной записи согласия гражданина в таблицу с декларативным ограничением stg.consents_benchmark_check завершилась успешной фиксацией данных (Рисунок 17).',
        'pgadmin_fig17.png',
        'Рисунок 17 – Успешная вставка согласия через декларативный CHECK'
    ),
    (
        'Аналогичная операция вставки валидного согласия в таблицу с процедурным триггером stg.consents_benchmark_trigger также выполнена штатно (Рисунок 18).',
        'pgadmin_fig18.png',
        'Рисунок 18 – Успешная валидация данных триггерной функцией'
    ),
    (
        'Попытка передачи фиктивного объема полномочий (SUPER_USER_ROOT) в таблицу с декларативным контролем была мгновенно пресечена констрейнтом chk_bm_scope (Рисунок 19).',
        'pgadmin_fig19.png',
        'Рисунок 19 – Срабатывание декларативного ограничения при некорректном scope'
    ),
    (
        'Процедурный триггер при обнаружении невалидного значения scope перехватил ошибку, зафиксировал инцидент в журнале audit.validation_violations и отклонил транзакцию (Рисунок 20).',
        'pgadmin_fig20.png',
        'Рисунок 20 – Перехват и аудит невалидного scope триггерной функцией'
    ),
    (
        'Тестирование инварианта хронологии (дата окончания действия должна быть строго позже даты выдачи) на таблице CHECK привело к срабатыванию констрейнта chk_bm_dates (Рисунок 21).',
        'pgadmin_fig21.png',
        'Рисунок 21 – Блокировка инвертированных дат декларативным констрейнтом'
    ),
    (
        'Триггерная функция при хронологической инверсии сформировала детализированное сообщение бизнес-ошибки и сохранила попытку нарушения в аудит (Рисунок 22).',
        'pgadmin_fig22.png',
        'Рисунок 22 – Диагностика нарушения хронологии дат процедурным триггером'
    ),
    (
        'Запрос согласия на 10 лет при законодательном нормативе не более 5 лет вызвал штатную блокировку ограничением chk_bm_dates (Рисунок 23).',
        'pgadmin_fig23.png',
        'Рисунок 23 – Отклонение превышения 5-летнего срока ограничением CHECK'
    ),
    (
        'Процедурный триггер рассчитал величину превышения норматива в днях и прервал выполнение операции с кодом ошибки 23514 (Рисунок 24).',
        'pgadmin_fig24.png',
        'Рисунок 24 – Вычисление величины превышения срока согласия триггером'
    ),
    (
        'Пакетная вставка 10 000 записей согласий в таблицу с ограничениями CHECK выполнена за 38.450 мс (Рисунок 25), продемонстрировав минимальные накладные расходы кода ядра СУБД.',
        'pgadmin_fig25.png',
        'Рисунок 25 – Время пакетной вставки 10 000 строк с ограничениями CHECK'
    ),
    (
        'Обработка аналогичного массива данных через процедурный триггер потребовала 97.910 мс (Рисунок 26), отражая затраты на вызов интерпретатора PL/pgSQL для каждой строки.',
        'pgadmin_fig26.png',
        'Рисунок 26 – Время вставки 10 000 строк с процедурной триггерной обработкой'
    ),
    (
        'Сводная гистограмма времени выполнения подтверждает выигрыш декларативных ограничений CHECK в 2.55 раза по сравнению с триггером (Рисунок 27).',
        'pgadmin_fig27.png',
        'Рисунок 27 – Сравнительная гистограмма времени валидации (CHECK vs Триггер)'
    ),
    (
        'Анализ плана EXPLAIN (ANALYZE, BUFFERS) показал, что чистый оверхед триггерного механизма составил 48.210 мс (Рисунок 28). Таким образом, для статических инвариантов строки целесообразно использовать CHECK, а триггеры применять при необходимости межтабличных проверок и аудита нарушений.',
        'pgadmin_fig28.png',
        'Рисунок 28 – План выполнения пакетной вставки и накладные расходы триггера'
    )
]

def generate_docx():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(1.5)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)

    # Footer page number
    footer = sec.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_run = f_p.add_run()
    f_run.font.name = 'Times New Roman'
    f_run.font.size = Pt(12)
    f_xml = f_run._element
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    f_xml.append(fldSimple)

    def add_p(text, space_before=0, space_after=0):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Cm(1.25)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_blank_line():
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run('')
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        return p

    def add_heading(text, space_before=0, space_after=12):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_fig_item(text_descr, img_filename, caption_text, width_cm=14.2):
        add_p(text_descr, space_before=0, space_after=4)

        img_path = os.path.join(IMG_DIR, img_filename)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.first_line_indent = Cm(0)
            p_img.paragraph_format.space_before = Pt(2)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.add_run().add_picture(img_path, width=Cm(width_cm))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.first_line_indent = Cm(0)
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(0)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(14)
        r_cap.font.color.rgb = RGBColor(0, 0, 0)

        # Empty line after caption
        add_blank_line()

    # --- Стр 1: ТИТУЛЬНЫЙ ЛИСТ ---
    def t_p(text, bold=False, size=11, space_after=2):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = bold
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    t_p('МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ', size=11)
    t_p('ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ', size=11)
    t_p('ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ', size=11)
    t_p('ВЫСШЕГО ОБРАЗОВАНИЯ', size=11)
    t_p('«НОВОСИБИРСКИЙ ГОСУДАРСТВЕННЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ»', bold=True, size=11, space_after=4)
    t_p('_________________________________________________________________', size=10, space_after=4)
    t_p('Факультет автоматики и вычислительной техники', size=12)
    t_p('Кафедра защиты информации', size=12, space_after=12)

    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.first_line_indent = Cm(0)
        p_logo.paragraph_format.space_after = Pt(12)
        p_logo.add_run().add_picture(LOGO_PATH, width=Cm(6.5))

    t_p('ЛАБОРАТОРНАЯ РАБОТА №2', bold=True, size=16, space_after=8)
    t_p('по дисциплине: «Безопасность систем баз данных»', size=13, space_after=10)
    t_p('Вариант: Защита БД систем цифровой идентификации граждан', bold=True, size=13, space_after=24)

    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Cm(8.0)
    tbl.columns[1].width = Cm(8.0)

    p_vl = tbl.cell(0, 0).paragraphs[0]
    p_vl.paragraph_format.first_line_indent = Cm(0)
    p_vl.paragraph_format.line_spacing = 1.15
    p_vl.add_run('Выполнил:\nстудент гр. «АБ-420», «АВТФ»\nКорецкий П. С.\n«___» ________ 2026 г.\n\n_____________________\n(подпись)')
    for r in p_vl.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)

    p_vr = tbl.cell(0, 1).paragraphs[0]
    p_vr.paragraph_format.first_line_indent = Cm(0)
    p_vr.paragraph_format.line_spacing = 1.15
    p_vr.add_run('Проверил:\nСтарший преподаватель ЗИ\nПитько Я. А.\n«___» ________ 2026 г.\n\n_____________________\n(подпись)')
    for r in p_vr.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)

    p_bot = doc.add_paragraph()
    p_bot.paragraph_format.space_before = Pt(24)
    p_bot.paragraph_format.first_line_indent = Cm(0)
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_city = p_bot.add_run('Новосибирск 2026')
    r_city.font.name = 'Times New Roman'
    r_city.font.size = Pt(12)

    doc.add_page_break()

    # --- Стр 2: SECURITY DEFINER-ФУНКЦИИ ---
    add_heading('SECURITY DEFINER-функции (точечное повышение)')
    add_p('Цель: изучение механизмов точечного повышения привилегий в базах данных систем цифровой идентификации граждан, управление доступом через функции-шлюзы и сравнительный анализ производительности контроля бизнес-логики.')
    add_p('В соответствии с требованиями законодательства о защите персональных данных (152-ФЗ) прямой доступ прикладной сервисной роли app_writer к таблицам биометрических дескрипторов, электронных паспортов и токенов доступа категорически запрещен. Любые операции добавления и модификации производятся исключительно через шлюзовые процедуры SECURITY DEFINER в контексте владельца схемы app_owner. Исходный код функций безопасности приведен в Приложении А.')
    add_p('Первая функция (app.fn_register_biometric_template()) производит регистрацию биометрических шаблонов лица и отпечатков пальцев. Процедура валидирует порог качества Liveness-сканирования (не ниже 50.00), рассчитывает хэш-сумму SHA-256 и выполняет симметричное шифрование сырого вектора алгоритмом AES-256 через модуль pgcrypto, обеспечивая профилю уровень доверия Trust Level 5.')
    add_p('Вторая функция (app.fn_issue_electronic_passport()) регламентирует выдачу удостоверения личности гражданина. Функция блокирует прямые DML-операции и контролирует соответствие серии (4 цифры), номера (6 цифр), кода органа (XXX-XXX) и структуры крипточипа (не менее 16 байт).')
    add_p('Третья функция (app.fn_grant_interagency_token()) формирует токен авторизации для внешних ведомств (МВД, ФНС, банков). Выдача токена осуществляется строго при наличии активного юридически значимого согласия субъекта в реестре app.access_consents.')

    doc.add_page_break()

    # --- РАЗДЕЛ 1: ТЕСТИРОВАНИЕ ПРАВ (Естественный поток, БЕЗ искусственных pagebreak между фигурами) ---
    add_heading('Тестирование прав')
    for text_descr, img_fn, cap in FIGURE_DATA_SECTION_1:
        add_fig_item(text_descr, img_fn, cap)

    doc.add_page_break()

    # --- РАЗДЕЛ 2: CHECK VS ТРИГГЕР (Естественный поток) ---
    add_heading('CHECK vs Триггер')
    add_p('Для контроля бизнес-правил согласий граждан (срок действия до 5 лет, допустимый scope) проведено сравнительное исследование декларативных ограничений CHECK и процедурных триггеров BEFORE INSERT. Исходный код структур приведен в Приложении Б.')
    for text_descr, img_fn, cap in FIGURE_DATA_SECTION_2:
        add_fig_item(text_descr, img_fn, cap)

    doc.add_page_break()

    # --- ВЫВОД (на отдельной странице, 3 абзаца связного текста БЕЗ списков) ---
    add_heading('Вывод')
    add_p('В ходе лабораторной работы реализовано точечное повышение привилегий с использованием процедур SECURITY DEFINER для защиты базы данных систем цифровой идентификации граждан. Для критических сущностей созданы изолированные функции регистрации биометрических шаблонов, выдачи электронных паспортов и выпуска межведомственных токенов доступа. Прикладной роли веб-портала и операторам МФЦ полностью закрыт прямой DML-доступ к защищенным таблицам, что исключает утечку персональных данных и несанкционированную модификацию реестров при компрометации внешних сервисов. Внутри функций обеспечено шифрование биометрических векторов ключом AES-256, проверка качества сканирования (Liveness не менее 50%), контроль структуры документов и обязательная проверка юридических согласий граждан.')
    add_p('Проведено всестороннее тестирование ролевой модели доступа, подтвердившее блокировку деструктивных операций для ролей app_reader, app_writer и auditor, а также корректную работу шлюзовых процедур при штатных и невалидных вызовах. Все факты обращений к защищенным интерфейсам гарантированно фиксируются в системном журнале audit.function_calls с перехватом исключений, обеспечивая непрерывную подотчетность действий пользователей и системных процессов.')
    add_p('Также выполнено экспериментальное сравнение декларативного ограничения CHECK и процедурного триггера при валидации бизнес-правил согласий субъектов персональных данных. Оба механизма успешно предотвращают инверсию дат, превышение предельного 5-летнего срока и назначение фиктивных полномочий, при этом процедурный триггер обеспечивает расширенную диагностику и автономную запись инцидентов в журнал audit.validation_violations. Нагрузочный замер на 10 000 операций выявил превосходство декларативного констрейнта CHECK в 2.55 раза (38.450 мс против 97.910 мс) за счет отсутствия накладных расходов интерпретатора PL/pgSQL, составивших 48.210 мс. Для промышленной эксплуатации цифрового профиля в качестве основного решения для внутристрочных правил обоснован выбор ограничений CHECK, тогда как триггеры и шлюзовые функции сохранены для межтабличного контроля согласий и форензики.')

    doc.add_page_break()

    # --- ПРИЛОЖЕНИЕ А ---
    p_ha = doc.add_paragraph()
    p_ha.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ha.paragraph_format.first_line_indent = Cm(0)
    p_ha.paragraph_format.space_before = Pt(0)
    p_ha.paragraph_format.space_after = Pt(12)
    r_ha = p_ha.add_run('Приложение А')
    r_ha.font.name = 'Times New Roman'
    r_ha.font.size = Pt(16)
    r_ha.bold = True
    r_ha.font.color.rgb = RGBColor(0, 0, 0)

    for line in SQL_APP_A.split('\n'):
        p_c = doc.add_paragraph()
        p_c.paragraph_format.first_line_indent = Cm(0)
        p_c.paragraph_format.space_before = Pt(0)
        p_c.paragraph_format.space_after = Pt(0)
        p_c.paragraph_format.line_spacing = 1.0
        r_c = p_c.add_run(line if line else ' ')
        r_c.font.name = 'Consolas'
        r_c.font.size = Pt(8.0)
        r_c.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_page_break()

    # --- ПРИЛОЖЕНИЕ Б ---
    p_hb = doc.add_paragraph()
    p_hb.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hb.paragraph_format.first_line_indent = Cm(0)
    p_hb.paragraph_format.space_before = Pt(0)
    p_hb.paragraph_format.space_after = Pt(12)
    r_hb = p_hb.add_run('Приложение Б')
    r_hb.font.name = 'Times New Roman'
    r_hb.font.size = Pt(16)
    r_hb.bold = True
    r_hb.font.color.rgb = RGBColor(0, 0, 0)

    for line in SQL_APP_B.split('\n'):
        p_c = doc.add_paragraph()
        p_c.paragraph_format.first_line_indent = Cm(0)
        p_c.paragraph_format.space_before = Pt(0)
        p_c.paragraph_format.space_after = Pt(0)
        p_c.paragraph_format.line_spacing = 1.0
        r_c = p_c.add_run(line if line else ' ')
        r_c.font.name = 'Consolas'
        r_c.font.size = Pt(8.0)
        r_c.font.color.rgb = RGBColor(0, 0, 0)

    target_paths = [
        r'e:\laba2\БСБД_КорецкийП.С._ЛР2.docx',
        r'e:\laba2\БСБД_Корецкий_П.С._ЛР2.docx',
        r'e:\laba2\БСБД_Корецкий_ПС_ЛР2_финал.docx',
        OUT_DOCX,
    ]
    for p in target_paths:
        try:
            doc.save(p)
            print("Successfully saved DOCX to:", p)
        except PermissionError:
            print("File locked by Word, skipped:", p)

def generate_typst():
    # Build Typst source
    # Section 1 items
    s1_items = ""
    for text_descr, img_fn, cap in FIGURE_DATA_SECTION_1:
        s1_items += f'''
{text_descr}

#fig-item("images/{img_fn}", [{cap}])
'''

    # Section 2 items
    s2_items = ""
    for text_descr, img_fn, cap in FIGURE_DATA_SECTION_2:
        s2_items += f'''
{text_descr}

#fig-item("images/{img_fn}", [{cap}])
'''

    typst_code = f'''#set page(
  paper: "a4",
  margin: (left: 3cm, right: 1.5cm, top: 2cm, bottom: 2cm),
  header: none,
  footer: context {{
    let p_num = counter(page).get().first()
    if p_num > 1 {{
      align(center)[#text(font: "Times New Roman", size: 12pt)[#p_num]]
    }}
  }},
)

#set text(
  font: "Times New Roman",
  size: 14pt,
  lang: "ru",
)

// ГОСТ 7.32-2017: 14pt, полуторный интервал (leading: 0.85em), отступ 1.25 см, выравнивание по ширине
#set par(
  justify: true,
  leading: 0.85em,
  first-line-indent: (amount: 1.25cm, all: true),
)

// Заголовок раздела: 16 пт, полужирный, по центру
#let heading-section(title) = {{
  set par(first-line-indent: 0cm)
  set text(size: 16pt, weight: "bold")
  v(0.3em)
  align(center)[#title]
  v(1.0em)
}}

// Подписи рисунков: 14 пт, по центру + ПУСТАЯ СТРОКА ПОСЛЕ ПОДПИСИ
// Изображения масштабируются по ширине пропорционально, без искусственного растягивания
#let fig-item(img, cap, w: 14.2cm) = {{
  set align(center)
  set par(first-line-indent: 0cm)
  v(0.3em)
  image(img, width: w)
  v(0.25em)
  text(size: 14pt)[#cap]
  v(1.35em) // ПУСТАЯ СТРОКА ПОСЛЕ ПОДПИСИ РИСУНКА (по Чубрейчу)
}}

// ============================================================================
// Стр 1: ТИТУЛЬНЫЙ ЛИСТ (полный аналог ЛР1, пропорциональный)
// ============================================================================
#set par(first-line-indent: 0cm)

#v(0.2cm)

#align(center)[
  #set text(size: 11pt, weight: "regular")
  МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ \\
  #v(5pt)
  ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ \\
  ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ \\
  ВЫСШЕГО ОБРАЗОВАНИЯ \\
  «НОВОСИБИРСКИЙ ГОСУДАРСТВЕННЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ»
]

#v(2pt)
#line(length: 100%, stroke: 0.5pt)
#v(4pt)

#align(center)[
  #set text(size: 12pt)
  Факультет автоматики и вычислительной техники \\
  Кафедра защиты информации
]

#v(18pt)

#align(center)[
  #image("images/nstu_logo.png", width: 6.5cm)
]

#v(20pt)

#align(center)[
  #text(size: 16pt, weight: "bold")[ЛАБОРАТОРНАЯ РАБОТА №2] \
  #v(8pt)
  #text(size: 13pt)[по дисциплине: #strong[#emph[«Безопасность систем баз данных»]]] \
  #v(10pt)
  #text(size: 13pt, weight: "bold")[Вариант: Защита БД систем цифровой идентификации граждан]
]

#v(25pt)

#grid(
  columns: (1fr, 1fr),
  column-gutter: 2.0cm,
  align: (left, left),
  [
    #set text(size: 12pt)
    Выполнил: \\
    #v(3pt)
    Студент гр. «АБ-420», «АВТФ» \\
    #v(3pt)
    #emph[Корецкий П. С.] \\
    #v(6pt)
    «#h(0.8cm)» #h(1.8cm) 2026 г. \\
    #v(10pt)
    #line(length: 5.5cm, stroke: 0.5pt)
    #v(-6pt)
    #text(size: 10pt)[(подпись)]
  ],
  [
    #set text(size: 12pt)
    Проверил: \\
    #v(3pt)
    Старший преподаватель ЗИ \\
    #v(3pt)
    #emph[Питько Я. А.] \\
    #v(6pt)
    «#h(0.8cm)» #h(1.8cm) 2026 г. \\
    #v(10pt)
    #line(length: 5.5cm, stroke: 0.5pt)
    #v(-6pt)
    #text(size: 10pt)[(подпись)]
  ]
)

#v(1fr)

#align(center)[
  #set text(size: 12pt)
  Новосибирск 2026
]

#pagebreak()

// ============================================================================
// Стр 2: SECURITY DEFINER-ФУНКЦИИ (КРАТКИЙ ОБЗОР)
// ============================================================================
#heading-section[SECURITY DEFINER-функции (точечное повышение)]

#set par(first-line-indent: 1.25cm, justify: true)

#text(weight: "bold")[Цель:] изучение механизмов точечного повышения привилегий в базах данных систем цифровой идентификации граждан, управление доступом через функции-шлюзы и сравнительный анализ производительности контроля бизнес-логики.

В соответствии с требованиями законодательства о защите персональных данных (152-ФЗ) прямой доступ прикладной сервисной роли `app_writer` к таблицам биометрических дескрипторов, электронных паспортов и токенов доступа категорически запрещен. Любые операции добавления и модификации производятся исключительно через шлюзовые процедуры `SECURITY DEFINER` в контексте владельца схемы `app_owner`. Исходный код функций безопасности приведен в Приложении А.

Первая функция (`app.fn_register_biometric_template()`) производит регистрацию биометрических шаблонов лица и отпечатков пальцев. Процедура валидирует порог качества Liveness-сканирования (не ниже 50.00), рассчитывает хэш-сумму SHA-256 и выполняет симметричное шифрование сырого вектора алгоритмом AES-256 через модуль `pgcrypto`, обеспечивая профилю уровень доверия Trust Level 5.

Вторая функция (`app.fn_issue_electronic_passport()`) регламентирует выдачу удостоверения личности гражданина. Функция блокирует прямые DML-операции и контролирует соответствие серии (4 цифры), номера (6 цифр), кода органа (XXX-XXX) и структуры крипточипа (не менее 16 байт).

Третья функция (`app.fn_grant_interagency_token()`) формирует токен авторизации для внешних ведомств (МВД, ФНС, банков). Выдача токена осуществляется строго при наличии активного юридически значимого согласия субъекта в реестре `app.access_consents`.

#pagebreak()

// ============================================================================
// ТЕСТИРОВАНИЕ ПРАВ (Естественный поток без искусственных pagebreak)
// ============================================================================
#heading-section[Тестирование прав]

#set par(first-line-indent: 1.25cm, justify: true)
{s1_items}

#pagebreak()

// ============================================================================
// CHECK VS ТРИГГЕР (Естественный поток)
// ============================================================================
#heading-section[CHECK vs Триггер]

#set par(first-line-indent: 1.25cm, justify: true)

Для контроля бизнес-правил согласий граждан (срок действия до 5 лет, допустимый scope) проведено сравнительное исследование декларативных ограничений `CHECK` и процедурных триггеров `BEFORE INSERT`. Исходный код структур приведен в Приложении Б.
{s2_items}

#pagebreak()

// ============================================================================
// ВЫВОД (на отдельной странице, 3 абзаца связного текста БЕЗ списков)
// ============================================================================
#heading-section[Вывод]

#set par(first-line-indent: 1.25cm, leading: 0.85em, justify: true)

В ходе лабораторной работы реализовано точечное повышение привилегий с использованием процедур SECURITY DEFINER для защиты базы данных систем цифровой идентификации граждан. Для критических сущностей созданы изолированные функции регистрации биометрических шаблонов, выдачи электронных паспортов и выпуска межведомственных токенов доступа. Прикладной роли веб-портала и операторам МФЦ полностью закрыт прямой DML-доступ к защищенным таблицам, что исключает утечку персональных данных и несанкционированную модификацию реестров при компрометации внешних сервисов. Внутри функций обеспечено шифрование биометрических векторов ключом AES-256, проверка качества сканирования (Liveness не менее 50%), контроль структуры документов и обязательная проверка юридических согласий граждан.

Проведено всестороннее тестирование ролевой модели доступа, подтвердившее блокировку деструктивных операций для ролей app_reader, app_writer и auditor, а также корректную работу шлюзовых процедур при штатных и невалидных вызовах. Все факты обращений к защищенным интерфейсам гарантированно фиксируются в системном журнале audit.function_calls с перехватом исключений, обеспечивая непрерывную подотчетность действий пользователей и системных процессов.

Также выполнено экспериментальное сравнение декларативного ограничения CHECK и процедурного триггера при валидации бизнес-правил согласий субъектов персональных данных. Оба механизма успешно предотвращают инверсию дат, превышение предельного 5-летнего срока и назначение фиктивных полномочий, при этом процедурный триггер обеспечивает расширенную диагностику и автономную запись инцидентов в журнал audit.validation_violations. Нагрузочный замер на 10 000 операций выявил превосходство декларативного констрейнта CHECK в 2.55 раза (38.450 мс против 97.910 мс) за счет отсутствия накладных расходов интерпретатора PL/pgSQL, составивших 48.210 мс. Для промышленной эксплуатации цифрового профиля в качестве основного решения для внутристрочных правил обоснован выбор ограничений CHECK, тогда как триггеры и шлюзовые функции сохранены для межтабличного контроля согласий и форензики.

#pagebreak()

// ============================================================================
// ПРИЛОЖЕНИЕ А
// ============================================================================
#heading-section[Приложение А]

#set text(font: "Consolas", size: 8.5pt)
#set par(first-line-indent: 0cm, leading: 0.45em, justify: false)

```sql
{SQL_APP_A}
```

#pagebreak()

// ============================================================================
// ПРИЛОЖЕНИЕ Б
// ============================================================================
#heading-section[Приложение Б]

#set text(font: "Consolas", size: 8.5pt)
#set par(first-line-indent: 0cm, leading: 0.45em, justify: false)

```sql
{SQL_APP_B}
```
'''

    with open(OUT_TYP, 'w', encoding='utf-8') as f:
        f.write(typst_code)
    print("Successfully written report.typ with natural flow!")

if __name__ == '__main__':
    generate_docx()
    generate_typst()
