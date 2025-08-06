from django.db import connection

from core.ports.pdf.pdf_generator_port import ReportRepositoryPort


class ReportRepository(ReportRepositoryPort):
    def get_general_vote_result(self, event_vote_id: int):
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
