import os
import xlsxwriter
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
output_filename = "test.xlsx"
output_filepath = f"{desktop_path}/{output_filename}"
workbook = xlsxwriter.Workbook(output_filepath)
worksheet = workbook.add_worksheet()
worksheet.set_paper(9)
# Top: 1 Zoll, Bottom: 1 Zoll, Left: 0.75 Zoll, Right: 0.75 Zoll
worksheet.set_margins(top=0, bottom=0, left=0, right=0)
img_path = 'Briefbogen Aktuell 2021.png'
worksheet.set_column("A:F", 15.4)
worksheet.insert_image('A1', img_path, {'x_scale': 0.8, 'y_scale': 0.8, 'x_offset': 0, 'y_offset': 0})

cell_format = workbook.add_format({
    'font_size': 8,
})
cell_format1 = workbook.add_format({
    'align':'center'
    })
merge_format = workbook.add_format({
    'align': 'center',
    'valign': 'vcenter',
    #'border': 1
})

'''worksheet.merge_range('C5:D5', 'Mitte von C und D', merge_format)
worksheet.merge_range('C6:D6', 'Mitte von C und D', merge_format)
worksheet.merge_range('C7:D7', 'Mitte von C und D', merge_format)
worksheet.write("C5:D5", "Reinmediensysteme ⋅ Planung", cell_format1)
worksheet.write("C6", "Projektierung ⋅ Montage",cell_format1)
worksheet.write("C7", "Mess- und Steuerungstechnik", cell_format1)'''

worksheet.write("A10", "Prüfauftrag")
worksheet.write("A11", "Projektnummer: P19-109")
#worksheet.write("C8", "Saatwinkler Damm 66, 13627 Berlin")
worksheet.write("D10", "Baustelle: Baustelle test")
#worksheet.write("E7", "Baustelle test")
worksheet.write("B12", "Feuchtemessung")
worksheet.write("B14", "Sensor: S220")
worksheet.write("D14", "Gasart: O2")
worksheet.add_table('B16:E19', {'header_row': False})
table_values = [
    ["Messgrößen", "Absolute Luftfeuchtigkeit", "Relative Luftfeuchtigkeit", "Drucktaupunkt"],
    ["Einheit", "ppm", "%rH", "°C Td"],
    ["MP1", "10000ppm", "fill", "fill", "fill"]]

for i in range(0, len(table_values[0])):
    worksheet.write(f"B{i + 15}", table_values[0][i])
    worksheet.write(f"D{i + 15}", table_values[1][i])
    worksheet.write(f"E{i + 15}", table_values[2][i])

worksheet.write("B21", "MP1: Messplatz")
worksheet.write("B22", "Prüfausdruck Nr.: " + str(1))
worksheet.write("B23", "Beschreibung: test1")
worksheet.write("A50", "Messbereich: -100 ... +20 °C Td", cell_format)
worksheet.write("C50",
                "Genauigkeit: ± 1 °C Td (0 ... 20 °C Td); ± 2 °C Td (-60 ... 0 °C Td); ± 3 °C (-100 ... -60 °C Td)",
                cell_format)
workbook.close()