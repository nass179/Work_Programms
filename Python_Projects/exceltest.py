import xlsxwriter

# Create a new Workbook and add a worksheet
workbook = xlsxwriter.Workbook('output.xlsx')
worksheet = workbook.add_worksheet()

# Path to your image file
img_path = 'ultratube_logo.png'
worksheet.set_column("A:A", 22)
# Insert the image with specific options
worksheet.insert_image('C1', img_path, {'x_scale': 0.4, 'y_scale': 0.4, 'x_offset': 10, 'y_offset': 10})
#header1 = "&R&G"
#worksheet.set_header(header1, {"image_right": "ultratube_logo.png"},{'x_scale': 0.4, 'y_scale': 0.4, 'x_offset': 10, 'y_offset': 10})
worksheet.write("A4", "Projektnummer: P18-187")
worksheet.write("A8", "Test GmbH")
worksheet.write("A9", "teststraße 5")
worksheet.write("A10", "10716 Berlin")

# Close the workbook
workbook.close()
