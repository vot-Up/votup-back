from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from typing import Callable

from core.ports.pdf.pdf_generator_port import PdfGeneratorPort


class ReportlabPdfAdapter(PdfGeneratorPort):
    def __init__(self):
        self.buffer = None
        self.canvas = None
        self.width, self.height = A4

    def create_canvas(self) -> None:
        self.buffer = BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)

    def draw(self, draw_func: Callable) -> None:
        draw_func(self.canvas, self.width, self.height)

    def finish(self) -> bytes:
        self.canvas.showPage()
        self.canvas.save()
        self.buffer.seek(0)
        return self.buffer.read()
