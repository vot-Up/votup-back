"""Unit tests for task_02: HistoricalRecords on models and ViewSetBase without reversion."""
import inspect

import pytest
from simple_history.manager import HistoryDescriptor

from account.models import User
from core.models.models import (
    Candidate,
    EventVoting,
    Plate,
    PlateUser,
    ResumeVote,
    Voter,
    VotingPlate,
    VotingUser,
)
from core.viewset import ViewSetBase


class TestViewSetBaseNoReversion:
    """ViewSetBase.create/update use transaction.atomic without reversion."""

    def test_create_uses_transaction_atomic(self):
        source = inspect.getsource(ViewSetBase.create)
        assert "transaction.atomic" in source

    def test_update_uses_transaction_atomic(self):
        source = inspect.getsource(ViewSetBase.update)
        assert "transaction.atomic" in source

    def test_create_has_no_reversion(self):
        source = inspect.getsource(ViewSetBase.create)
        assert "revisions" not in source
        assert "reversion" not in source

    def test_update_has_no_reversion(self):
        source = inspect.getsource(ViewSetBase.update)
        assert "revisions" not in source
        assert "reversion" not in source


def _has_historical_records(model):
    """Check that a model has a HistoricalRecords field (registered as HistoryDescriptor)."""
    return isinstance(model.__dict__.get("history"), HistoryDescriptor)


class TestModelsHaveHistory:
    """Each business model and User expose a HistoricalRecords field."""

    def test_voter_has_history(self):
        assert _has_historical_records(Voter)

    def test_candidate_has_history(self):
        assert _has_historical_records(Candidate)

    def test_plate_has_history(self):
        assert _has_historical_records(Plate)

    def test_plate_user_has_history(self):
        assert _has_historical_records(PlateUser)

    def test_event_voting_has_history(self):
        assert _has_historical_records(EventVoting)

    def test_voting_plate_has_history(self):
        assert _has_historical_records(VotingPlate)

    def test_voting_user_has_history(self):
        assert _has_historical_records(VotingUser)

    def test_resume_vote_has_history(self):
        assert _has_historical_records(ResumeVote)

    def test_user_has_history(self):
        assert _has_historical_records(User)


@pytest.mark.django_db(transaction=True)
class TestHistoricalRecordsCreation:
    """Creating model instances via ORM generates a historical record."""

    def test_voter_create_generates_history(self):
        voter = Voter.objects.create(name="Test Voter", cellphone="11111111111")
        assert voter.history.count() == 1
        assert voter.history.first().history_type == "+"

    def test_candidate_create_generates_history(self):
        candidate = Candidate.objects.create(name="Test Candidate", cellphone="22222222222")
        assert candidate.history.count() == 1

    def test_plate_create_generates_history(self):
        plate = Plate.objects.create(name="Chapa Test")
        assert plate.history.count() == 1

    def test_event_voting_create_generates_history(self):
        event = EventVoting.objects.create(description="Eleição Test")
        assert event.history.count() == 1

    def test_voter_update_adds_history(self):
        voter = Voter.objects.create(name="Original", cellphone="33333333333")
        voter.name = "Updated"
        voter.save()
        assert voter.history.count() == 2
        types = list(voter.history.values_list("history_type", flat=True))
        assert "+" in types
        assert "~" in types
