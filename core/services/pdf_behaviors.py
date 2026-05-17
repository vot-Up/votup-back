"""
core/services/pdf_behaviors.py — Comportamentos de geração de PDF (migrados de use_cases/behaviors.py)

Contém os behaviors que ainda são usados diretamente pelo viewset:
- VotingUserBehavior
- VoterInPlateResume
- ResumeVoterProvisory
- VoteByPlateBehavior

Acessa modelos diretamente via core.models.models, sem Port/Repository.
"""

import datetime
from io import BytesIO

from django.db import connection
from django.db.models import Count, F, OuterRef, Subquery
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from core.models import models


class PDFWithFooter:
    """Utilitário para gerar PDFs com rodapé 'votup Labs'."""

    def __init__(self):
        self.buffer = BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
        self.y = self.height - 50

    def footer(self):
        self.canvas.setFont("Helvetica", 10)
        self.canvas.drawCentredString(self.width / 2, 15, "votup Labs")

    def save(self):
        self.footer()
        self.canvas.showPage()
        self.canvas.save()
        self.buffer.seek(0)
        return self.buffer.read()


class VotingUserBehavior:
    """Gera PDF com quantidade de votos por chapa em um evento."""

    def __init__(self, event_vote):
        self.event_vote = event_vote

    def get_header(self):
        return models.EventVoting.objects.get(pk=self.event_vote)

    def get_body(self):
        return (
            models.VotingUser.objects.all()
            .values("plate__id", "plate__name")
            .annotate(total=Count("*"))
            .filter(voting_id=self.get_header().id, voter__isnull=False)
            .order_by("-total")
        )

    def run(self):
        pdf = PDFWithFooter()
        c = pdf.canvas
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(pdf.width / 2, pdf.y, self.get_header().description)
        pdf.y -= 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, pdf.y, "Chapa")
        c.drawString(300, pdf.y, "Quantidade de Votos")
        pdf.y -= 20
        c.setFont("Helvetica", 12)
        for item in self.get_body():
            c.drawString(40, pdf.y, item["plate__name"])
            c.drawString(300, pdf.y, str(item["total"]))
            pdf.y -= 20
        return pdf.save()


class VoterInPlateResume:
    """Gera PDF com eleitores de uma chapa."""

    def __init__(self, plate):
        self.plate = plate

    def get_header(self):
        return models.Plate.objects.get(pk=self.plate)

    def get_body(self):
        return models.Voter.objects.filter(votinguser__plate=self.plate).values("name")

    def run(self):
        pdf = PDFWithFooter()
        c = pdf.canvas
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(pdf.width / 2, pdf.y, self.get_header().name)
        pdf.y -= 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, pdf.y, "Eleitor")
        pdf.y -= 20
        c.setFont("Helvetica", 12)
        for item in self.get_body():
            c.drawString(40, pdf.y, item["name"])
            pdf.y -= 20
        return pdf.save()


class ResumeVoterProvisory:
    """Gera PDF com resumo provisório de votação."""

    def __init__(self, event_vote):
        self.event_vote = event_vote

    def get_header(self):
        return models.EventVoting.objects.get(pk=self.event_vote)

    def get_body(self):
        return models.ResumeVote.objects.all().values("plate__name", "quantity")

    def run(self):
        pdf = PDFWithFooter()
        c = pdf.canvas
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(pdf.width / 2, pdf.y, self.get_header().description)
        pdf.y -= 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, pdf.y, "Chapa")
        c.drawString(300, pdf.y, "Quantidade de Votos")
        pdf.y -= 20
        c.setFont("Helvetica", 12)
        for item in self.get_body():
            c.drawString(40, pdf.y, item["plate__name"])
            c.drawString(300, pdf.y, str(item["quantity"]))
            pdf.y -= 20
        return pdf.save()


class VoteByPlateBehavior:
    """Gera PDF detalhado com votos de uma chapa específica."""

    def __init__(self, event_vote: int, plate: int):
        self.event_vote = event_vote
        self.plate = plate

    def _get_data(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT ev.description, p.name, v2.name AS eleitor, v2.avatar,
                       presidente.name AS presidente, presidente.avatar_url,
                       vice_presidente.name AS vice_presidente, vice_presidente.avatar_url
                FROM voting_user v
                INNER JOIN event_voting ev ON ev.id = v.id_voting
                INNER JOIN plate p ON v.id_plate = p.id
                INNER JOIN voter v2 ON v.id_voter = v2.id
                INNER JOIN plate_user pu ON p.id = pu.id_plate AND pu.type = 'P'
                INNER JOIN candidate presidente ON pu.id_candidate = presidente.id
                INNER JOIN plate_user puv ON p.id = puv.id_plate AND puv.type = 'V'
                INNER JOIN candidate vice_presidente ON puv.id_candidate = vice_presidente.id
                WHERE ev.id = %s AND p.id = %s
                ORDER BY eleitor DESC
                """,
                [self.event_vote, self.plate],
            )
            return cursor.fetchall()

    def run(self):
        rows = self._get_data()
        if not rows:
            return None

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        y = height - 40
        first_row = rows[0]
        description = first_row[0]
        plate_name = first_row[1]
        presidente = first_row[4]
        vice_presidente = first_row[6]

        p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(width / 2, y, "VOTOS DA CHAPA")
        y -= 40
        p.setFont("Helvetica", 12)
        p.drawString(40, y, f"Nome da Votação: {description}")
        y -= 20
        p.drawString(40, y, f"Nome da Chapa: {plate_name}")
        y -= 20
        p.drawString(40, y, f"Presidente: {presidente}")
        y -= 20
        p.drawString(40, y, f"Vice-Presidente: {vice_presidente}")
        y -= 40

        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, y, "Eleitores:")
        y -= 20
        p.setFont("Helvetica", 11)
        for row in rows:
            eleitor = row[2]
            p.drawString(60, y, f"- {eleitor}")
            y -= 15
            if y < 50:
                p.showPage()
                y = height - 40

        p.setFont("Helvetica", 10)
        p.drawCentredString(width / 2, 30, f"Gerado em {datetime.datetime.now().strftime('%d/%m/%Y')}")
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer.read()
