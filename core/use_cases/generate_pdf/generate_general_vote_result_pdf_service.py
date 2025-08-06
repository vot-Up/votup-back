from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class GenerateGeneralVoteResultPdfService:
    def __init__(self, rows: list):
        self.rows = rows

    def generate(self) -> bytes:
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 50
        p.setFont("Helvetica-Bold", 16)
        p.drawCentredString(width / 2, y, "RESULTADO GERAL DA VOTAÇÃO")

        y -= 50
        p.setFont("Helvetica", 12)

        for _, plate_name, vote_count in self.rows:
            p.drawString(50, y, f"Chapa: {plate_name} - Votos: {vote_count}")
            y -= 20
            if y < 50:
                p.showPage()
                y = height - 50

        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer.read()
