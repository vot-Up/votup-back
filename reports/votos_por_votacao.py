from django.db import connection
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_vote_report(event_id):
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
            [event_id],
        )
        rows = cursor.fetchall()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="resultado_votacao.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, y, "RESULTADO GERAL DA VOTAÇÃO")

    y -= 50
    p.setFont("Helvetica", 12)

    for row in rows:
        description, plate_name, vote_count = row
        p.drawString(50, y, f"Chapa: {plate_name} - Votos: {vote_count}")
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()

    return response
