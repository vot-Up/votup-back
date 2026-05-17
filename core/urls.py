from rest_framework.routers import DefaultRouter

from core import viewset

router = DefaultRouter()
router.register("voter", viewset.VoterViewSet)
router.register("candidate", viewset.CandidateViewSet)
router.register("resume_vote", viewset.ResumeVoteViewSet)
router.register("plate", viewset.PlateViewSet)
router.register("voting", viewset.VotingViewSet)
router.register("plate_user", viewset.PlateUserViewSet)
router.register("voting_plate", viewset.VotingPlateViewSet)
router.register("voting_user", viewset.VotingUserViewSet)
urlpatterns = router.urls
