import aiohttp
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


async def get_student_info(params):
    url = f"http://13.60.230.147/api/v1/courseit/results/?ids={params}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


def print_table(headers, data):
    # Calculate column widths
    col_widths = [max(len(str(item)) for item in column) for column in zip(headers, *data)]

    # Create a format string for the table
    header_format = '| ' + ' | '.join(f'{{:<{w}}}' for w in col_widths) + ' |'
    separator = '+=' + '=+='.join('=' * w for w in col_widths) + '=+'

    # Print the headers
    result = ""
    result += f"{separator}\n"
    result += f"{header_format.format(*headers)}\n"
    result += f"{separator}\n"

    # Print each row
    for row in data:
        result += f"{header_format.format(*row)}\n"
    result += f"{separator}\n"

    return result
