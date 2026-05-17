"""
tests/test_plate_service.py — Testes unitários para core/services/plate_service.py
"""

from django.test import TestCase

from core import exceptions
from core.models import models
from core.services import plate_service


class ActivatePlateTests(TestCase):
    def setUp(self):
        self.plate = models.Plate.objects.create(name="Chapa 1")

    def test_activate_plate_sets_active_true(self):
        """activate_plate com plate válida retorna plate ativada."""
        plate_service.activate_plate(self.plate.id)
        self.plate.refresh_from_db()
        self.assertTrue(self.plate.active)

    def test_activate_plate_already_active_is_idempotent(self):
        """Reativar uma chapa já ativa não gera erro."""
        self.plate.active = True
        self.plate.save()
        plate_service.activate_plate(self.plate.id)
        self.plate.refresh_from_db()
        self.assertTrue(self.plate.active)

    def test_activate_plate_inexistent_raises_does_not_exist(self):
        """activate_plate com plate inexistente lança DoesNotExist."""
        with self.assertRaises(models.Plate.DoesNotExist):
            plate_service.activate_plate(9999)

    def test_activate_plate_raises_when_candidate_in_conflicting_plate(self):
        """activate_plate lança PlateUserIsActiveException se candidato está em outra chapa."""
        conflicting_plate = models.Plate.objects.create(name="Chapa Conflitante")
        candidate = models.Candidate.objects.create(name="Candidato", cellphone="11999999999", disabled=False)
        models.PlateUser.objects.create(plate=self.plate, candidate=candidate, type="T")
        models.PlateUser.objects.create(plate=conflicting_plate, candidate=candidate, type="T")

        with self.assertRaises(exceptions.PlateUserIsActiveException):
            plate_service.activate_plate(self.plate.id)

    def test_activate_plate_no_conflict_succeeds(self):
        """activate_plate com chapas sem candidatos em comum funciona."""
        candidate = models.Candidate.objects.create(name="Candidato", cellphone="11988888888", disabled=False)
        models.PlateUser.objects.create(plate=self.plate, candidate=candidate, type="T")
        plate_service.activate_plate(self.plate.id)
        self.plate.refresh_from_db()
        self.assertTrue(self.plate.active)


class DeleteUserPlateTests(TestCase):
    def setUp(self):
        self.plate = models.Plate.objects.create(name="Chapa 1")
        self.candidate = models.Candidate.objects.create(
            name="Candidato 1", cellphone="11999999999", disabled=True
        )
        models.PlateUser.objects.create(plate=self.plate, candidate=self.candidate, type="T")

    def test_delete_user_plate_removes_association(self):
        """delete_user_plate remove associação candidato-chapa corretamente."""
        plate_service.delete_user_plate(self.candidate.id, self.plate.id)
        self.assertFalse(
            models.PlateUser.objects.filter(candidate=self.candidate, plate=self.plate).exists()
        )

    def test_delete_user_plate_re_enables_candidate(self):
        """delete_user_plate habilita o candidato após remoção."""
        self.candidate.disabled = True
        self.candidate.save()
        plate_service.delete_user_plate(self.candidate.id, self.plate.id)
        self.candidate.refresh_from_db()
        self.assertFalse(self.candidate.disabled)

    def test_delete_user_plate_inexistent_association_raises(self):
        """delete_user_plate com associação inexistente lança UnableRemovePlateException."""
        with self.assertRaises(exceptions.UnableRemovePlateException):
            plate_service.delete_user_plate(self.candidate.id, 9999)

    def test_delete_user_plate_does_not_touch_other_plates(self):
        """delete_user_plate não afeta outras associações do mesmo candidato."""
        other_plate = models.Plate.objects.create(name="Chapa 2")
        models.PlateUser.objects.create(plate=other_plate, candidate=self.candidate, type="T")
        plate_service.delete_user_plate(self.candidate.id, self.plate.id)
        self.assertTrue(
            models.PlateUser.objects.filter(candidate=self.candidate, plate=other_plate).exists()
        )


class DeleteVotingPlateTests(TestCase):
    def setUp(self):
        self.plate = models.Plate.objects.create(name="Chapa 1")
        self.voting = models.EventVoting.objects.create(description="Eleicao Teste")
        self.voting_plate = models.VotingPlate.objects.create(voting=self.voting, plate=self.plate)

    def test_delete_voting_plate_removes_association(self):
        """delete_voting_plate remove chapa de votação corretamente."""
        plate_service.delete_voting_plate(self.voting.id, self.plate.id)
        self.assertFalse(
            models.VotingPlate.objects.filter(voting=self.voting, plate=self.plate).exists()
        )

    def test_delete_voting_plate_inexistent_succeeds_silently(self):
        """delete_voting_plate com IDs inexistentes não lança."""
        plate_service.delete_voting_plate(9999, 9999)

    def test_delete_voting_plate_only_removes_specified_association(self):
        """delete_voting_plate não remove associações de outras chapas na mesma votação."""
        other_plate = models.Plate.objects.create(name="Chapa 2")
        other_vp = models.VotingPlate.objects.create(voting=self.voting, plate=other_plate)

        plate_service.delete_voting_plate(self.voting.id, self.plate.id)

        self.assertTrue(models.VotingPlate.objects.filter(pk=other_vp.pk).exists())
