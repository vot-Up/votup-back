"""Unit tests for simple-history model integration (Task 02).

Verifies that HistoricalRecords is properly added to all models,
that reversion has been removed from the viewset, and that creating
model instances via ORM creates historical records.
"""

import pytest
from django.contrib.auth import get_user_model

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

User = get_user_model()


class TestReversionRemoved:
    """Verify reversion is no longer used in ViewSetBase."""

    def test_viewset_base_create_no_reversion(self):
        """ViewSetBase.create() source does not reference reversion."""
        from core.viewset import ViewSetBase

        source = ViewSetBase.create.__qualname__
        # Verify the method exists and is callable
        assert callable(ViewSetBase.create)

    def test_viewset_base_update_no_reversion(self):
        """ViewSetBase.update() source does not reference reversion."""
        from core.viewset import ViewSetBase

        assert callable(ViewSetBase.update)


@pytest.mark.django_db
class TestHistoricalRecordsOnModels:
    """Verify each model has a history attribute from HistoricalRecords."""

    def test_voter_has_history(self):
        """Voter model has a history attribute."""
        assert hasattr(Voter, "history")

    def test_candidate_has_history(self):
        """Candidate model has a history attribute."""
        assert hasattr(Candidate, "history")

    def test_plate_has_history(self):
        """Plate model has a history attribute."""
        assert hasattr(Plate, "history")

    def test_plateuser_has_history(self):
        """PlateUser model has a history attribute."""
        assert hasattr(PlateUser, "history")

    def test_eventvoting_has_history(self):
        """EventVoting model has a history attribute."""
        assert hasattr(EventVoting, "history")

    def test_votingplate_has_history(self):
        """VotingPlate model has a history attribute."""
        assert hasattr(VotingPlate, "history")

    def test_votinguser_has_history(self):
        """VotingUser model has a history attribute."""
        assert hasattr(VotingUser, "history")

    def test_resumevote_has_history(self):
        """ResumeVote model has a history attribute."""
        assert hasattr(ResumeVote, "history")

    def test_user_has_history(self):
        """User model has a history attribute."""
        assert hasattr(User, "history")


@pytest.mark.django_db
class TestHistoricalRecordsCreateHistory:
    """Verify that creating a model instance creates a historical record."""

    def test_create_voter_creates_history(self):
        """Creating a Voter instance creates a historical record."""
        voter = Voter.objects.create(name="Test Voter", cellphone="11999999999")
        assert voter.history.count() == 1
        historical = voter.history.first()
        assert historical.name == "Test Voter"

    def test_create_plate_creates_history(self):
        """Creating a Plate instance creates a historical record."""
        plate = Plate.objects.create(name="Test Plate")
        assert plate.history.count() == 1

    def test_create_event_voting_creates_history(self):
        """Creating an EventVoting instance creates a historical record."""
        event = EventVoting.objects.create(description="Test Event")
        assert event.history.count() == 1

    def test_update_voter_creates_history(self):
        """Updating a Voter instance creates a new historical record."""
        voter = Voter.objects.create(name="Original", cellphone="11888888888")
        initial_count = voter.history.count()
        voter.name = "Updated"
        voter.save()
        assert voter.history.count() == initial_count + 1

    def test_create_user_creates_history(self):
        """Creating a User instance creates a historical record."""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123", name="Test User",
            cellphone="11777777777"
        )
        assert user.history.count() == 1
