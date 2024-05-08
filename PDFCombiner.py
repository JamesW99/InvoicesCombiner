
from PIL import Image, ImageFilter, ImageEnhance
import fitz  # PyMuPDF library
from datetime import datetime
import os

class PDFCombiner:
    def __init__(self, file_paths, dpi=600):
        self.file_paths = file_paths
        self.dpi = dpi
        self.a4_width, self.a4_height = 4960, 7016  # A4 size in pixels at 600 DPI.
        self.output_directory = 'combined'
        self.vertical_margin = 100  # Vertical margin to avoid printing issues at the edges
        self.content_height = self.a4_height - 2 * self.vertical_margin  # Adjusted content height after accounting for margins
        self.right_margin = 200  # Right margin
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        self.output_path = os.path.join(self.output_directory, f"combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        self.file_initialized = False

    def process_files(self):
        grouped_files = [self.file_paths[i:i+3] for i in range(0, len(self.file_paths), 3)]
        for group in grouped_files:
            self.process_group(group)
        return self.output_path

    def process_group(self, group):
        combined_image = Image.new("RGB", (self.a4_width, self.a4_height), color="white")
        available_height = self.content_height // 3
        for idx, file_path in enumerate(group):
            pdf_image = self.load_image(file_path, available_height)
            if pdf_image:
                # Calculate horizontal position for right alignment with margin
                horizontal_position = self.a4_width - pdf_image.width - self.right_margin
                combined_image.paste(pdf_image, (horizontal_position, self.vertical_margin + available_height * idx))
        save_mode = 'PDF'
        save_kwargs = {'resolution': self.dpi}
        if self.file_initialized:
            save_kwargs['append'] = True
        else:
            self.file_initialized = True
        combined_image.save(self.output_path, save_mode, **save_kwargs)

    def load_image(self, file_path, available_height):
        if file_path.endswith(".pdf"):
            pdf_file = fitz.open(file_path)
            pdf_page = pdf_file.load_page(0)
            pix = pdf_page.get_pixmap(dpi=self.dpi)
            pdf_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        elif file_path.endswith(".jpg"):
            pdf_image = Image.open(file_path)
        else:
            return None
        return self.resize_and_enhance(pdf_image, available_height)

    def resize_and_enhance(self, image, target_height):
        scaling_factor = target_height / image.height
        new_width = int(image.width * scaling_factor)
        image = image.resize((new_width, target_height), Image.BICUBIC)
        image = image.filter(ImageFilter.SHARPEN)
        contrast_enhancer = ImageEnhance.Contrast(image)
        return contrast_enhancer.enhance(1.2)


# Usage
if __name__ == '__main__':
    file_paths = ["1.pdf", "2.pdf", "3.pdf", "4.pdf"]
    combiner = PDFCombiner(file_paths)
    pdf_path = combiner.process_files()
    print(f"The combined PDF is saved at {pdf_path}")
