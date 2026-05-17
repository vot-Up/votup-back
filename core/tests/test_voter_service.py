"""tests/test_voter_service.py — Testes unitários para core/services/voter_service.py"""

from django.test import TestCase

from core import exceptions
from core.models import models
from core.services import voter_service


class GetVoterTests(TestCase):
    def setUp(self):
        self.voter = models.Voter.objects.create(
            name="Eleitor Teste", cellphone="11999999999"
        )

    def test_get_voter_returns_dict(self):
        """get_voter retorna dict com id, name, cellphone, has_voted."""
        result = voter_service.get_voter(cellphone="11999999999")
        self.assertEqual(result["id"], self.voter.id)
        self.assertEqual(result["name"], "Eleitor Teste")
        self.assertEqual(result["cellphone"], "11999999999")
        self.assertFalse(result["has_voted"])

    def test_get_voter_nonexistent_raises(self):
        """get_voter com celular inexistente lança CellphoneDoesNotUserException."""
        with self.assertRaises(exceptions.CellphoneDoesNotUserException):
            voter_service.get_voter(cellphone="00000000000")

    def test_get_voter_already_voted_raises(self):
        """get_voter com eleitor já votado lança Exception."""
        voting = models.EventVoting.objects.create(description="Teste")
        plate = models.Plate.objects.create(name="Chapa 1")
        models.VotingUser.objects.create(
            voting=voting, voter=self.voter, plate=plate
        )
        with self.assertRaises(Exception):
            voter_service.get_voter(cellphone="11999999999")

    def test_get_voter_not_voted_returns_has_voted_false(self):
        """get_voter com eleitor que não votou retorna has_voted=False."""
        result = voter_service.get_voter(cellphone="11999999999")
        self.assertFalse(result["has_voted"])
