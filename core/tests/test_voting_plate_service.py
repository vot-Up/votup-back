"""tests/test_voting_plate_service.py — Testes unitários para core/services/voting_plate_service.py"""

from django.test import TestCase

from core.models import models
from core.services import voting_plate_service


class CheckPlateAssociateTests(TestCase):
    def setUp(self):
        self.plate1 = models.Plate.objects.create(name="Chapa 1")
        self.plate2 = models.Plate.objects.create(name="Chapa 2")
        self.voting = models.EventVoting.objects.create(description="Eleição Teste")

    def test_check_plate_associate_returns_associated_plates(self):
        """check_plate_associate retorna chapas associadas à votação."""
        models.VotingPlate.objects.create(voting=self.voting, plate=self.plate1)
        models.VotingPlate.objects.create(voting=self.voting, plate=self.plate2)
        result = list(voting_plate_service.check_plate_associate(voting_id=self.voting.id))
        self.assertEqual(len(result), 2)

    def test_check_plate_associate_returns_empty_for_no_associations(self):
        """check_plate_associate com votação sem chapas retorna lista vazia."""
        result = list(voting_plate_service.check_plate_associate(voting_id=self.voting.id))
        self.assertEqual(len(result), 0)

    def test_check_plate_associate_returns_only_associated_plates(self):
        """check_plate_associate não retorna chapas não associadas."""
        plate3 = models.Plate.objects.create(name="Chapa 3")
        models.VotingPlate.objects.create(voting=self.voting, plate=self.plate1)
        # plate3 not associated
        result = list(voting_plate_service.check_plate_associate(voting_id=self.voting.id))
        plate_ids = [r["id"] for r in result]
        self.assertIn(self.plate1.id, plate_ids)
        self.assertNotIn(plate3.id, plate_ids)

    def test_check_plate_associate_inexistent_voting_returns_empty(self):
        """check_plate_associate com ID de votação inexistente retorna lista vazia."""
        result = list(voting_plate_service.check_plate_associate(voting_id=9999))
        self.assertEqual(len(result), 0)

    def test_check_plate_associate_single_plate(self):
        """check_plate_associate com apenas uma chapa associada retorna 1 resultado."""
        models.VotingPlate.objects.create(voting=self.voting, plate=self.plate1)
        result = list(voting_plate_service.check_plate_associate(voting_id=self.voting.id))
        self.assertEqual(len(result), 1)
