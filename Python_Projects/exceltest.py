import xlsxwriter

# Create a new Workbook and add a worksheet
workbook = xlsxwriter.Workbook('output.xlsx')
worksheet = workbook.add_worksheet()

# Path to your image file
img_path = 'ultratube_logo.png'
worksheet.set_column("A:G", 11.29)
#image_path = "ultratube_logo.png"
#worksheet.set_header('&L&G', {'image_left': image_path, 'image_left_width': 10, 'image_left_height': 5})
# Insert the image with specific options
worksheet.insert_image('E1', img_path, {'x_scale': 0.2, 'y_scale': 0.2, 'x_offset': 10, 'y_offset': 5})
#header1 = "&R&G"
#worksheet.set_header(header1, {"image_right": "ultratube_logo.png"},{'x_scale': 0.4, 'y_scale': 0.4, 'x_offset': 10, 'y_offset': 10})
worksheet.write("A2", "Projektnummer: P18-187")
worksheet.write("A6", "Kunde:")
worksheet.write("A7", "Test GmbH")
worksheet.write("A8", "teststraße 5")
worksheet.write("A9", "10716 Berlin")
worksheet.write("E4", "Saatwinkler Damm 66, 13627 Berlin")
worksheet.write("E6", "Baustelle:")
worksheet.write("E7", "321 - Physik Neubau 1.Ba")
worksheet.write("E8", "Zülpicher Str.77")
worksheet.write("E9", "50937 Köln")


# Close the workbook
workbook.close()
