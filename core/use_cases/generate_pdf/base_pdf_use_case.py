from core.ports.pdf.pdf_generator_port import PdfGeneratorPort


class BasePdfService:
    def __init__(self, pdf_generator: PdfGeneratorPort):
        self.pdf = pdf_generator

    def generate(self, draw_func) -> bytes:
        self.pdf.create_canvas()
        self.pdf.draw(draw_func)
        return self.pdf.finish()