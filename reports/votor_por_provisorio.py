from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.db import connection
import datetime


def generate_provisional_vote_report(request, event_id: int):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ev.description,
                   p.name,
                   v.quantity_vote
            FROM resume_vote v
            INNER JOIN plate p ON v.id_plate = p.id
            INNER JOIN event_voting ev ON v.id_voting = ev.id
            WHERE ev.id = %s
        """, [event_id])
        rows = cursor.fetchall()

    if not rows:
        return HttpResponse("Nenhum dado encontrado.", status=404)

    description = rows[0][0]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resultado_provisorio.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 40

    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, y, "RESULTADO GERAL DA VOTAÇÃO")

    y -= 40
    p.setFont("Helvetica", 12)
    p.drawString(40, y, f"Nome do evento: {description}")

    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Chapa")
    p.drawString(320, y, "Quantidade de Votos")

    y -= 10
    p.line(40, y, width - 40, y)

    y -= 20
    p.setFont("Helvetica", 11)

    for row in rows:
        plate_name = row[1]
        votes = row[2]
        p.drawString(40, y, plate_name)
        p.drawRightString(550, y, str(votes))
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 40

    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2, 30, f"Gerado em {datetime.datetime.now().strftime('%d/%m/%Y')}")
    p.showPage()
    p.save()

    return response
