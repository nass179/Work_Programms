import os
import xlsxwriter
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
output_filename = "test.xlsx"
output_filepath = f"{desktop_path}/{output_filename}"
workbook = xlsxwriter.Workbook(output_filepath)
worksheet = workbook.add_worksheet()
# Top: 1 Zoll, Bottom: 1 Zoll, Left: 0.75 Zoll, Right: 0.75 Zoll
worksheet.set_margins(top=1, bottom=1, left=1)
img_path = 'Logo1.jpg'
worksheet.set_column("A:F", 13.17)
worksheet.insert_image('B1', img_path, {'x_scale': 1, 'y_scale': 1, 'x_offset': 80, 'y_offset': 0})

cell_format = workbook.add_format({
    'font_size': 8,
})
cell_format1 = workbook.add_format({
    'align':'center'
    })
merge_format = workbook.add_format({
    'align': 'center',
    'valign': 'vcenter',
    'border': 1
})

worksheet.merge_range('C5:D5', 'Mitte von C und D', merge_format)
worksheet.merge_range('C6:D6', 'Mitte von C und D', merge_format)
worksheet.merge_range('C7:D7', 'Mitte von C und D', merge_format)
worksheet.write("C5:D5", "Reinmediensysteme Planung")
worksheet.write("C6", "Projektierung Montage")
worksheet.write("C7", "Mess- und Steuerungstechnik")

worksheet.write("A10", "Prüfauftrag")
worksheet.write("A11", "Projektnummer: P19-109")
worksheet.write("C8", "Saatwinkler Damm 66, 13627 Berlin")
worksheet.write("E10", "Baustelle: Baustelle test")
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