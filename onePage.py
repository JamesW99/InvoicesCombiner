from PIL import Image, ImageFilter, ImageEnhance
import fitz  # PyMuPDF library

# Define the file paths
file_paths = ["1.pdf", "2.pdf", "3.pdf"]

# Define the desired output path
output_path = "combined_invoices.pdf"

# Define the A4 dimensions in pixels at 600 DPI
a4_width, a4_height = 4960, 7016

# Calculate the available height for each file
available_height = a4_height // 3

# Create a new A4 image
combined_image = Image.new("RGB", (a4_width, a4_height), color="white")

# Define the vertical offsets for each file
offsets = [0, available_height, available_height * 2]

# Loop through the file paths and add each file to the combined image
for idx, file_path in enumerate(file_paths):
    if file_path.endswith(".pdf"):
        # Open the PDF file with PyMuPDF
        pdf_file = fitz.open(file_path)
        pdf_page = pdf_file.load_page(0)  # Get the first page
        pix = pdf_page.get_pixmap(dpi=600)  # Render the page as an image at 600 DPI
        pdf_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pdf_image = pdf_image.rotate(180, expand=True)  # Rotate the image to the correct orientation
    elif file_path.endswith(".jpg"):
        # Open the JPG file
        pdf_image = Image.open(file_path)
    else:
        continue

    # Calculate the scaling factor to fit the image within the available height
    scaling_factor = available_height / pdf_image.height
    new_width = int(pdf_image.width * scaling_factor)
    new_height = available_height

    # Resize the image while maintaining the aspect ratio and using BICUBIC for better clarity
    pdf_image = pdf_image.resize((new_width, new_height), Image.BICUBIC)

    # Apply a sharpening filter
    pdf_image = pdf_image.filter(ImageFilter.SHARPEN)

    # Enhance the contrast
    contrast_enhancer = ImageEnhance.Contrast(pdf_image)
    pdf_image = contrast_enhancer.enhance(1.2)

    # Paste the image onto the combined image
    combined_image.paste(pdf_image, (0, offsets[idx]))

# Save the combined image as a PDF
combined_image.save(output_path, "PDF", resolution=600.0)

print(f"Combined invoices saved to {output_path}")