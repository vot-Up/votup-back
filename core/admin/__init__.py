from core.admin.people import CandidateAdmin, VoterAdmin
from core.admin.plates import PlateAdmin, PlateUserAdmin, PlateUserInline
from core.admin.voting import (
    EventVotingAdmin,
    ResumeVoteAdmin,
    ResumeVoteInline,
    VotingPlateAdmin,
    VotingPlateInline,
    VotingUserAdmin,
    VotingUserInline,
)

__all__ = [
    "VoterAdmin",
    "CandidateAdmin",
    "PlateAdmin",
    "PlateUserAdmin",
    "PlateUserInline",
    "EventVotingAdmin",
    "VotingPlateAdmin",
    "VotingPlateInline",
    "VotingUserAdmin",
    "VotingUserInline",
    "ResumeVoteAdmin",
    "ResumeVoteInline",
]
