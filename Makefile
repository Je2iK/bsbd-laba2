.PHONY: help test benchmark screenshots report docx all clean

TYPST = .\typst.exe
PYTHON = python

help:
	@echo "======================================================================"
	@echo "              КОМАНДЫ ДЛЯ УПРАВЛЕНИЯ ЛАБОРАТОРНОЙ РАБОТОЙ №2           "
	@echo "======================================================================"
	@echo "  make test             - Запустить набор 13 проверочных тестов прав доступа"
	@echo "  make benchmark        - Запустить бенчмарк CHECK vs Триггер (10 000 строк)"
	@echo "  make screenshots      - Сгенерировать терминальные скриншоты и график"
	@echo "  make report           - Скомпилировать отчёт ГОСТ 7.32 в PDF (Typst)"
	@echo "  make docx             - Сгенерировать отчёт ГОСТ 7.32 в формате Word (.docx)"
	@echo "  make all              - Запустить тесты, бенчмарк, скриншоты и собрать PDF/DOCX"
	@echo "  make clean            - Очистить временные файлы"
	@echo "======================================================================"

test:
	$(PYTHON) scripts/run_all_tests.py

benchmark:
	$(PYTHON) scripts/run_benchmark.py

screenshots:
	$(PYTHON) scripts/generate_screenshots.py

report:
	$(TYPST) compile report.typ "БСБД_Корецкий_ПС_ЛР2.pdf"
	@echo "Отчет успешно скомпилирован в PDF: БСБД_Корецкий_ПС_ЛР2.pdf"

docx:
	$(PYTHON) scripts/build_docx.py
	@echo "Отчет успешно сгенерирован в Word: БСБД_Корецкий_ПС_ЛР2.docx"

all: test benchmark screenshots report docx
	@echo "Все этапы лабораторной работы №2 успешно выполнены!"

clean:
	@powershell -NoProfile -Command "Remove-Item -Force -ErrorAction SilentlyContinue *.log, test*.typ, test*.pdf"
