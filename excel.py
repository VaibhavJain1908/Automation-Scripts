import xlsxwriter

workbook = xlsxwriter.Workbook('sample_data4.xlsx')
sheet = workbook.add_worksheet()

sheet.write('A1', 'Maisam')
sheet.write('A2', 'Abbas')

workbook.close()