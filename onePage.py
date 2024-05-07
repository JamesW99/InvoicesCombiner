from PIL import Image, ImageFilter, ImageEnhance
import fitz  # PyMuPDF library

class PDFCombiner:
    def __init__(self, file_paths, output_path="combined_invoices.pdf", dpi=600):
        self.file_paths = file_paths
        self.output_path = output_path
        self.dpi = dpi
        self.a4_width, self.a4_height = 4960, 7016
        self.available_height = self.a4_height // len(self.file_paths)
        self.offsets = [self.available_height * i for i in range(len(self.file_paths))]
        self.combined_image = Image.new("RGB", (self.a4_width, self.a4_height), color="white")

    def process_files(self):
        for idx, file_path in enumerate(self.file_paths):
            pdf_image = self.load_image(file_path)
            if pdf_image:
                self.add_image_to_combined(pdf_image, idx)

        self.combined_image.save(self.output_path, "PDF", resolution=self.dpi)
        print(f"Combined invoices saved to {self.output_path}")

    def load_image(self, file_path):
        if file_path.endswith(".pdf"):
            pdf_file = fitz.open(file_path)
            pdf_page = pdf_file.load_page(0)
            pix = pdf_page.get_pixmap(dpi=self.dpi)
            pdf_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            pdf_image = pdf_image.rotate(180, expand=True)
        elif file_path.endswith(".jpg"):
            pdf_image = Image.open(file_path)
        else:
            return None

        pdf_image = self.resize_and_enhance(pdf_image)
        return pdf_image

    def resize_and_enhance(self, image):
        scaling_factor = self.available_height / image.height
        new_width = int(image.width * scaling_factor)
        image = image.resize((new_width, self.available_height), Image.BICUBIC)
        image = image.filter(ImageFilter.SHARPEN)
        contrast_enhancer = ImageEnhance.Contrast(image)
        return contrast_enhancer.enhance(1.2)

    def add_image_to_combined(self, image, idx):
        self.combined_image.paste(image, (0, self.offsets[idx]))


# Usage
file_paths = ["1.pdf", "2.pdf", "3.pdf"]
combiner = PDFCombiner(file_paths)
combiner.process_files()



