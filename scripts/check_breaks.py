import docx

doc = docx.Document(r'e:\laba2\БСБД_Корецкий_ПС_ЛР2.docx')
for i in [133, 134, 135, 379, 380, 381]:
    p = doc.paragraphs[i]
    print(f'P{i}: text={p.text[:40]} | page_break_before={p.paragraph_format.page_break_before}')
    for r in p.runs:
        if 'w:br' in r._element.xml:
            print(f'   P{i} run has w:br!')
