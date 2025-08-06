from core.ports.pdf.pdf_generator_port import ReportRepositoryPort


class BasePdfService:
    def __init__(self, pdf_generator: ReportRepositoryPort):
        self.pdf = pdf_generator

    def generate(self, draw_func) -> bytes:
        pass
