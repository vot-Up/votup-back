from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.db import connection
import datetime


def generate_vote_report_by_plate(request, event_id: int, plate_id: int):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ev.description,
                   p.name,
                   v2.name AS eleitor,
                   v2.avatar,
                   presidente.name AS presidente,
                   presidente.avatar_url,
                   vice_presidente.name AS vice_presidente,
                   vice_presidente.avatar_url
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
        """, [event_id, plate_id])
        rows = cursor.fetchall()

    if not rows:
        return HttpResponse("Nenhum dado encontrado.", status=404)

    first_row = rows[0]
    description = first_row[0]
    plate_name = first_row[1]
    presidente = first_row[4]
    vice_presidente = first_row[6]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="votos_da_chapa.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 40

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

    return response
