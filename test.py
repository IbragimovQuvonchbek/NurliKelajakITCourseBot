from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont

def create_table_image(headers, data, output_file):
    # Define some parameters
    font = ImageFont.load_default()
    padding = 10
    cell_height = 40
    col_widths = [max(len(str(item)) for item in column) * 10 for column in zip(headers, *data)]
    table_width = sum(col_widths) + padding * (len(headers) + 1)
    table_height = cell_height * (len(data) + 1)

    # Create a blank image with white background
    image = Image.new("RGB", (table_width, table_height), "white")
    draw = ImageDraw.Draw(image)

    # Create the header format
    x_offset = padding
    for i, header in enumerate(headers):
        draw.text((x_offset, padding), header, font=font, fill="black")
        x_offset += col_widths[i] + padding

    # Draw the data rows
    for row_idx, row in enumerate(data):
        x_offset = padding
        y_offset = (row_idx + 1) * cell_height + padding // 2
        for col_idx, item in enumerate(row):
            draw.text((x_offset, y_offset), str(item), font=font, fill="black")
            x_offset += col_widths[col_idx] + padding

    # Save the image as a PNG file
    image.save(output_file)

# Test numbers and results
x = [1, 2, 3, 4]
y = [100, 80, 0, 89]

# Combine the test numbers and results into rows
data = list(zip(x, y))

# Headers for the table
headers = ["Test raqami", "Natija %"]

# Output file name
output_file = f"{uuid4()}.png"

# Create the table image
create_table_image(headers, data, output_file)
