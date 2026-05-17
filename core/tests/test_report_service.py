"""tests/test_report_service.py — Testes unitários para core/services/report_service.py"""

from django.test import TestCase

from core.models import models
from core.services import report_service


class GenerateGeneralVoteResultTests(TestCase):
    def setUp(self):
        self.voting = models.EventVoting.objects.create(description="Eleição Teste")
        self.plate = models.Plate.objects.create(name="Chapa 1")
        self.voter = models.Voter.objects.create(name="Eleitor", cellphone="11999999999")
        models.VotingUser.objects.create(
            voting=self.voting, voter=self.voter, plate=self.plate
        )

    def test_generate_returns_pdf_bytes(self):
        """generate_general_vote_result retorna bytes de PDF."""
        result = report_service.generate_general_vote_result(event_vote_id=self.voting.id)
        self.assertIsInstance(result, bytes)
        self.assertTrue(result.startswith(b"%PDF"))

    def test_generate_empty_voting_returns_pdf(self):
        """generate_general_vote_result com votação sem votos retorna PDF válido."""
        empty_voting = models.EventVoting.objects.create(description="Vazia")
        result = report_service.generate_general_vote_result(event_vote_id=empty_voting.id)
        self.assertIsInstance(result, bytes)
        self.assertTrue(result.startswith(b"%PDF"))

    def test_fetch_general_vote_result_returns_rows(self):
        """_fetch_general_vote_result retorna dados da votação."""
        rows = report_service._fetch_general_vote_result(self.voting.id)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Chapa 1")  # plate_name
        self.assertEqual(rows[0][2], 1)  # vote_count
