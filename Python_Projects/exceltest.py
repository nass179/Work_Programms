import xlsxwriter

# Create a new Workbook and add a worksheet
workbook = xlsxwriter.Workbook('output.xlsx')
worksheet = workbook.add_worksheet()

# Path to your image file
img_path = 'ultratube_logo.png'

# Insert the image with specific options
worksheet.insert_image('A1', img_path, {'x_scale': 0.4, 'y_scale': 0.4, 'x_offset': 10, 'y_offset': 10})

# Close the workbook
workbook.close()
