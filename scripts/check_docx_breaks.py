import docx

doc = docx.Document(r'e:\laba2\БСБД_Корецкий_ПС_ЛР2.docx')
count = 0
for p in doc.paragraphs:
    if 'type="page"' in p._p.xml:
        count += 1
print('Page breaks count in docx:', count)
