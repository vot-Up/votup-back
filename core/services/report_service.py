"""
core/services/report_service.py — Lógica de geração de relatórios/PDF (migrada de use_cases/)

Substitui GenerateGeneralVoteResultUseCase + ReportRepository + GenerateGeneralVoteResultPdfService.
Acessa modelos diretamente via core.models.models e db.connection, sem Port/Repository intermediário.
"""

from io import BytesIO

from django.db import connection
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_general_vote_result(event_vote_id: int) -> bytes:
    """Gera PDF com o resultado geral da votação.

    Substitui GenerateGeneralVoteResultUseCase(report_repository=ReportRepository()).execute(event_vote_id).

    Args:
        event_vote_id: ID do evento de votação.

    Returns:
        bytes do conteúdo PDF gerado.
    """
    rows = _fetch_general_vote_result(event_vote_id)
    return _generate_general_vote_result_pdf(rows)


def _fetch_general_vote_result(event_vote_id: int) -> list[tuple]:
    """Busca dados de resultado geral da votação via SQL direto.

    Args:
        event_vote_id: ID do evento de votação.

    Returns:
        Lista de tuplas (description, plate_name, vote_count).
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT ev.description, p.name, COUNT(*)
            FROM voting_user v
            INNER JOIN event_voting ev ON ev.id = v.id_voting
            INNER JOIN plate p ON v.id_plate = p.id
            WHERE ev.id = %s
            GROUP BY ev.description, p.name
            ORDER BY p.name DESC
            """,
            [event_vote_id],
        )
        return cursor.fetchall()


def _generate_general_vote_result_pdf(rows: list[tuple]) -> bytes:
    """Gera o PDF do resultado geral a partir dos dados.

    Args:
        rows: Lista de tuplas (description, plate_name, vote_count).

    Returns:
        bytes do PDF.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, y, "RESULTADO GERAL DA VOTAÇÃO")
    y -= 50

    p.setFont("Helvetica", 12)
    for _, plate_name, vote_count in rows:
        p.drawString(50, y, f"Chapa: {plate_name} - Votos: {vote_count}")
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.read()
