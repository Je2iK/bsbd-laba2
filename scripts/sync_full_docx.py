import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 1. Read real SQL from migrations
with open(r'e:\laba2\migrations\000008_security_definer_functions.up.sql', 'r', encoding='utf-8') as f:
    sql_app_a = f.read()

with open(r'e:\laba2\migrations\000009_check_vs_trigger_benchmarks.up.sql', 'r', encoding='utf-8') as f:
    sql_app_b = f.read()

doc_path = r'e:\laba2\БСБД_Корецкий_ПС_ЛР2.docx'
doc = docx.Document(doc_path)

# Fix in-text references
for p in doc.paragraphs:
    if 'Приложении A' in p.text or 'Приложении А' in p.text:
        p.text = p.text.replace('Приложении A', 'Приложении А')
    if 'Приложении B' in p.text or 'Приложении В' in p.text:
        p.text = p.text.replace('Приложении B', 'Приложении Б').replace('Приложении В', 'Приложении Б')

# Find where Appendix A starts
idx_app_a = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() in ['Приложение A', 'Приложение А']:
        idx_app_a = i
        break

print(f"Index of Appendix A in docx: {idx_app_a}")

if idx_app_a is not None:
    # Delete everything from idx_app_a to the end of document
    # In python-docx, deleting paragraphs from the end
    p_elements = [p._p for p in doc.paragraphs[idx_app_a:]]
    for p_elem in p_elements:
        p_elem.getparent().remove(p_elem)

# Now add Appendix A
p_head_a = doc.add_paragraph()
p_head_a.paragraph_format.page_break_before = True
p_head_a.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_head_a.paragraph_format.first_line_indent = Inches(0)
p_head_a.paragraph_format.space_before = Pt(6)
p_head_a.paragraph_format.space_after = Pt(12)
run_a = p_head_a.add_run("Приложение А")
run_a.font.name = "Times New Roman"
run_a.font.size = Pt(16)
run_a.font.bold = True
run_a.font.color.rgb = RGBColor(0, 0, 0)

for line in sql_app_a.split('\n'):
    p_code = doc.add_paragraph()
    p_code.paragraph_format.first_line_indent = Inches(0)
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(0)
    p_code.paragraph_format.line_spacing = 1.0
    run_code = p_code.add_run(line if line else ' ')
    run_code.font.name = "Consolas"
    run_code.font.size = Pt(7.5)
    run_code.font.color.rgb = RGBColor(0, 0, 0)

# Now add Appendix B
p_head_b = doc.add_paragraph()
p_head_b.paragraph_format.page_break_before = True
p_head_b.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_head_b.paragraph_format.first_line_indent = Inches(0)
p_head_b.paragraph_format.space_before = Pt(6)
p_head_b.paragraph_format.space_after = Pt(12)
run_b = p_head_b.add_run("Приложение Б")
run_b.font.name = "Times New Roman"
run_b.font.size = Pt(16)
run_b.font.bold = True
run_b.font.color.rgb = RGBColor(0, 0, 0)

for line in sql_app_b.split('\n'):
    p_code = doc.add_paragraph()
    p_code.paragraph_format.first_line_indent = Inches(0)
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(0)
    p_code.paragraph_format.line_spacing = 1.0
    run_code = p_code.add_run(line if line else ' ')
    run_code.font.name = "Consolas"
    run_code.font.size = Pt(7.5)
    run_code.font.color.rgb = RGBColor(0, 0, 0)

doc.save(doc_path)
print("Successfully updated БСБД_Корецкий_ПС_ЛР2.docx with genuine Appendix A and B!")
