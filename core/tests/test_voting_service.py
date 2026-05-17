"""tests/test_voting_service.py — Testes unitários para core/services/voting_service.py"""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core import exceptions
from core.models import models
from core.services import voting_service


class ActiveVoteTests(TestCase):
    def setUp(self):
        self.voting = models.EventVoting.objects.create(
            description="Eleição Teste", active=False
        )

    def test_active_vote_activates_event(self):
        """active_vote ativa o evento de votação."""
        voting_service.active_vote(self.voting.id)
        self.voting.refresh_from_db()
        self.assertTrue(self.voting.active)

    def test_active_vote_activates_associated_plates(self):
        """active_vote ativa as chapas associadas à votação."""
        plate = models.Plate.objects.create(name="Chapa 1", active=False)
        models.VotingPlate.objects.create(voting=self.voting, plate=plate)
        voting_service.active_vote(self.voting.id)
        plate.refresh_from_db()
        self.assertTrue(plate.active)

    def test_active_vote_raises_when_another_active(self):
        """active_vote lança ExistVoteActiveException se já houver votação ativa."""
        models.EventVoting.objects.create(description="Já Ativa", active=True)
        with self.assertRaises(exceptions.ExistVoteActiveException):
            voting_service.active_vote(self.voting.id)

    def test_active_vote_no_associated_plates(self):
        """active_vote sem chapas associadas ainda ativa a votação."""
        voting_service.active_vote(self.voting.id)
        self.voting.refresh_from_db()
        self.assertTrue(self.voting.active)


class CloseVoteTests(TestCase):
    def setUp(self):
        self.plate = models.Plate.objects.create(name="Chapa 1", active=True)
        self.voting = models.EventVoting.objects.create(
            description="Eleição Teste", active=True
        )
        models.VotingPlate.objects.create(voting=self.voting, plate=self.plate)

    def test_close_vote_deactivates_event(self):
        """close_vote desativa o evento de votação."""
        voting_service.close_vote(self.voting.id)
        self.voting.refresh_from_db()
        self.assertFalse(self.voting.active)

    def test_close_vote_deactivates_associated_plates(self):
        """close_vote desativa as chapas associadas."""
        voting_service.close_vote(self.voting.id)
        self.plate.refresh_from_db()
        self.assertFalse(self.plate.active)


class DeleteHistoricTests(TestCase):
    def setUp(self):
        self.plate = models.Plate.objects.create(name="Chapa 1")
        self.voting = models.EventVoting.objects.create(
            description="Eleição Teste", active=False
        )
        self.voter = models.Voter.objects.create(name="Eleitor", cellphone="11999999999")
        models.VotingPlate.objects.create(voting=self.voting, plate=self.plate)
        self.voting_user = models.VotingUser.objects.create(
            voting=self.voting, voter=self.voter
        )

    def test_delete_historic_removes_everything(self):
        """delete_historic remove todos os registros associados."""
        voting_service.delete_historic(self.voting.id)
        self.assertFalse(models.VotingUser.objects.filter(id=self.voting_user.id).exists())
        self.assertFalse(models.EventVoting.objects.filter(id=self.voting.id).exists())


class GetVotingUserTests(TestCase):
    def setUp(self):
        self.voter = models.Voter.objects.create(name="Eleitor", cellphone="11999999999")
        self.voting = models.EventVoting.objects.create(
            description="Eleição Teste",
            active=True,
            date=timezone.now() + timedelta(days=1),
        )
        plate1 = models.Plate.objects.create(name="Chapa 1")
        plate2 = models.Plate.objects.create(name="Chapa 2")
        models.VotingPlate.objects.create(voting=self.voting, plate=plate1)
        models.VotingPlate.objects.create(voting=self.voting, plate=plate2)

    def test_get_voting_user_returns_data(self):
        """get_voting_user retorna dados do eleitor e votação."""
        result = voting_service.get_voting_user(cellphone="11999999999")
        self.assertIn("id", result)
        self.assertIn("voting", result)
        self.assertIn("voter", result)

    def test_get_voting_user_invalid_cellphone_raises(self):
        """get_voting_user com celular inexistente lança CellphoneDoesNotUserException."""
        with self.assertRaises(exceptions.CellphoneDoesNotUserException):
            voting_service.get_voting_user(cellphone="00000000000")

    def test_get_voting_user_already_voted_raises(self):
        """get_voting_user com eleitor já votado lança UserHasAlreadyVotedException."""
        plate = models.Plate.objects.first()
        models.VotingUser.objects.create(
            voting=self.voting, voter=self.voter, plate=plate
        )
        with self.assertRaises(exceptions.UserHasAlreadyVotedException):
            voting_service.get_voting_user(cellphone="11999999999")


class GetVoterPlateTests(TestCase):
    def test_get_voter_plate_returns_voters(self):
        """get_voter_plate retorna eleitores da chapa."""
        plate = models.Plate.objects.create(name="Chapa 1")
        voter = models.Voter.objects.create(name="Eleitor", cellphone="11999999999")
        voting = models.EventVoting.objects.create(description="Teste")
        models.VotingUser.objects.create(voting=voting, voter=voter, plate=plate)
        result = list(voting_service.get_voter_plate(plate.id))
        self.assertEqual(len(result), 1)


class GetResumeVoteTests(TestCase):
    def test_get_resume_vote_returns_all(self):
        """get_resume_vote retorna todos os resumos."""
        result = list(voting_service.get_resume_vote())
        self.assertEqual(len(result), 0)
