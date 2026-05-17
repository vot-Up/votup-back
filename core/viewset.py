import logging

from django.db import IntegrityError, transaction
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from reversion import revisions

from account import actions, exceptions, messages, models, params_serializer

from core import exceptions, filters, messages, mixins, params_serializer
from core.models import models
from core.schemas.schemas import REPORT_SCHEMAS, VOTER_SCHEMAS, VOTING_SCHEMAS
from core.serializer import serializers

from core.services.candidate_service import update_avatar
from core.services.plate_service import activate_plate, delete_user_plate, delete_voting_plate
from core.services.voting_plate_service import check_plate_associate
from core.services.voting_service import (
    active_vote,
    close_vote,
    delete_historic,
    get_resume_vote,
    get_voter_plate,
    get_voting_user,
)
from core.services.voter_service import get_voter
from core.services.report_service import generate_general_vote_result
from core.services.pdf_behaviors import (
    ResumeVoterProvisory,
    VoteByPlateBehavior,
    VoterInPlateResume,
    VotingUserBehavior,
)

logger = logging.getLogger(__name__)


class ViewSetPermissions(ViewSet):
    permission_classes_by_action: dict = {}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return super().get_permissions()


class ViewSetBase(viewsets.ModelViewSet, mixins.ViewSetExpandMixin):
    def create(self, request, *args, **kwargs):
        with transaction.atomic(), revisions.create_revision():
            revisions.set_user(request.user)
            revisions.set_comment("CREATE")
            logger.info(f"Creating {self.queryset.model.__name__} by user {request.user}")
            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        with transaction.atomic(), revisions.create_revision():
            revisions.set_user(request.user)
            revisions.set_comment("UPDATE")
            logger.info(f"Updating {self.queryset.model.__name__} by user {request.user}")
            return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.make_queryset_expandable(request)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.make_queryset_expandable(request)
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            logger.warning(f"Deleting {self.queryset.model.__name__} ID {kwargs.get('pk')} by user {request.user}")
            return super(self).destroy(request, *args, **kwargs)
        except IntegrityError as e:
            logger.error(f"IntegrityError on delete: {str(e)}")
            raise exceptions.ForeignKeyException


@extend_schema_view(list=VOTER_SCHEMAS["list"], can_vote=VOTER_SCHEMAS["can_vote"])
class VoterViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.Voter.objects.all()
    serializer_class = serializers.VoterSerializer
    filterset_class = filters.VoterFilter
    ordering = (
        "-active",
        "-modified_at",
    )
    permission_classes_by_action = {
        "create": (AllowAny,),
        "partial_update": (AllowAny,),
        "destroy": (AllowAny,),
        "can_vote": (AllowAny,),
    }

    @action(detail=False, methods=["GET"])
    def can_vote(self, request):
        cellphone = request.query_params.get("cellphone")
        if not cellphone:
            logger.warning("can_vote called without cellphone parameter")
            return Response({"detail": "O parâmetro 'cellphone' é obrigatório."}, status=400)
        try:
            voter = get_voter(cellphone=cellphone)
            logger.info(f"Voter {cellphone} can vote: {not voter['has_voted']}")
            return Response(voter)
        except Exception as e:
            logger.error(f"Error checking if voter {cellphone} can vote: {str(e)}")
            return Response({"detail": str(e)}, status=400)


@extend_schema(tags=["Candidates"])
class CandidateViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.Candidate.objects.all()
    serializer_class = serializers.CandidateSerializer
    filterset_class = filters.CandidateFilter
    ordering = (
        "-active",
        "-modified_at",
    )
    permission_classes_by_action = {"create": (AllowAny,), "partial_update": (AllowAny,), "destroy": (AllowAny,)}

    @action(detail=True, methods=["post"], url_path="upload-avatar")
    def upload_avatar(self, request, pk=None):
        file = request.FILES.get("avatar")
        if not file:
            return Response({"detail": "Arquivo de imagem ausente."}, status=400)
        update_avatar(candidate_id=pk, file=file.read(), filename=file.name)
        return Response(status=204)


@extend_schema(tags=["Plates"])
class PlateViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.Plate.objects.all()
    serializer_class = serializers.PlateSerializer
    filterset_class = filters.PlateFilter
    permission_classes_by_action = {
        "list": (AllowAny,),
        "create": (AllowAny,),
        "partial_update": (AllowAny,),
        "destroy": (AllowAny,),
    }
    ordering = (
        "-active",
        "-modified_at",
    )

    def update(self, request, *args, **kwargs):
        if request.data.get("active"):
            activate_plate(plate_id=self.get_object().id)
        return super().update(request, *args, **kwargs)


@extend_schema_view(active_vote=VOTING_SCHEMAS["active_vote"], close_vote=VOTING_SCHEMAS["close_vote"])
class VotingViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.EventVoting.objects.all()
    serializer_class = serializers.EventVotingSerializer
    filterset_class = filters.EventVotingFilter
    ordering = (
        "-active",
        "-id",
    )
    permission_classes = (AllowAny,)

    def destroy(self, request, *args, **kwargs):
        if not self.get_object().active:
            try:
                logger.info(f"Deleting voting event {kwargs.get('pk')} and its history")
                delete_historic(event_vote=kwargs.get("pk"))
                return Response(data="Foi excluido com sucesso", status=200)
            except Exception as e:
                logger.error(f"Error deleting voting event: {str(e)}")
                raise exceptions.DeleteVoteActiveException
        else:
            logger.warning(f"Attempt to delete active voting event {kwargs.get('pk')}")
            raise exceptions.DeleteVoteActiveException()

    @action(methods=["PATCH"], detail=False)
    def active_vote(self, request, *args, **kwargs):
        param_serializer = params_serializer.ActiveOrCloseVoteParamSerializer(data=request.data)
        param_serializer.is_valid(raise_exception=True)
        logger.info(f"Activating vote {param_serializer.validated_data['vote_id']}")
        active_vote(vote_id=param_serializer.validated_data["vote_id"])
        return Response(data={"message": messages.ACTIVE_VOTE}, status=status.HTTP_200_OK)

    @action(methods=["PATCH"], detail=False)
    def close_vote(self, request, *args, **kwargs):
        param_serializer = params_serializer.ActiveOrCloseVoteParamSerializer(data=request.data)
        param_serializer.is_valid(raise_exception=True)
        logger.info(f"Closing vote {param_serializer.validated_data['vote_id']}")
        close_vote(vote_id=param_serializer.validated_data["vote_id"])
        return Response(data={"message": messages.CLOSE_VOTE}, status=status.HTTP_200_OK)


@extend_schema(tags=["Plates"])
class PlateUserViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.PlateUser.objects.all()
    serializer_class = serializers.PlateUserSerializer
    filterset_class = filters.PlateUserFilter
    permission_classes_by_action = {"create": (AllowAny,), "partial_update": (AllowAny,), "destroy": (AllowAny,)}

    @extend_schema(
        summary="Remover usuário da chapa",
        description="Remove um candidato de uma chapa específica.",
        request={
            "application/json": {
                "type": "object",
                "properties": {"plate": {"type": "integer"}, "candidate": {"type": "integer"}},
                "required": ["plate", "candidate"],
            }
        },
        responses={200: {"description": "Usuário removido da chapa com sucesso"}},
    )
    @action(detail=False, methods=["DELETE"])
    def delete_user_plate(self, request, *args, **kwargs):
        param_serializer = params_serializer.PlateUserParamSerializer(data=request.data)
        param_serializer.is_valid(raise_exception=True)
        logger.info(
            f"Removing user {param_serializer.validated_data['candidate']} from plate {param_serializer.validated_data['plate']}"
        )
        data = param_serializer.validated_data
        delete_user_plate(candidate_id=data["candidate"], plate_id=data["plate"])
        return Response(status=200)


@extend_schema(tags=["Voting Events"])
class VotingPlateViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.VotingPlate.objects.all()
    serializer_class = serializers.VotingPlateSerializer
    filterset_class = filters.VotingPlateFilter
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Remover chapa da votação",
        description="Remove uma chapa de um evento de votação.",
        request={
            "application/json": {
                "type": "object",
                "properties": {"voting": {"type": "integer"}, "plate": {"type": "integer"}},
                "required": ["voting", "plate"],
            }
        },
        responses={200: {"description": "Chapa removida da votação com sucesso"}},
    )
    @action(detail=False, methods=["DELETE"])
    def delete_voting_plate(self, request, *args, **kwargs):
        param_serializer = params_serializer.VotingPlateParamSerializer(data=request.data)
        param_serializer.is_valid(raise_exception=True)
        logger.info(
            f"Removing plate {param_serializer.validated_data['plate']} from voting {param_serializer.validated_data['voting']}"
        )
        delete_voting_plate(**param_serializer.validated_data)
        return Response(status=200)

    @extend_schema(
        summary="Verificar chapas associadas",
        description="Verifica quais chapas estão associadas a uma votação.",
        parameters=[{"name": "associate", "in": "query", "required": True, "schema": {"type": "integer"}}],
        responses={200: {"description": "Lista de chapas associadas"}},
    )
    @action(detail=False, methods=["GET"])
    def check_associate(self, request, *args, **kwargs):
        id_associate = int(request.query_params["associate"])
        result = check_plate_associate(voting_id=id_associate)
        return Response(data={"data": result}, status=200)


@extend_schema_view(
    voting=VOTING_SCHEMAS["voting"],
    ranking=VOTING_SCHEMAS["ranking"],
    get_voting_user_plate_quantity_pdf=REPORT_SCHEMAS["get_voting_user_plate_quantity_pdf"],
    resume_report=REPORT_SCHEMAS["resume_report"],
)
class VotingUserViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.VotingUser.objects.all()
    serializer_class = serializers.VotingUserSerializer
    filterset_class = filters.VotingUserFilter
    permission_classes = (AllowAny,)

    @action(detail=False, methods=["POST"])
    def voting(self, request, *args, **kwargs):
        param_serializer = params_serializer.InitVotingParamSerializer(data=request.data)
        param_serializer.is_valid(raise_exception=True)
        logger.info(f"Starting voting process for cellphone {param_serializer.validated_data['cellphone']}")
        voting_plate = get_voting_user(**param_serializer.validated_data)
        return Response(voting_plate, status.HTTP_200_OK)

    @action(methods=["GET"], detail=True)
    def ranking(self, request, *args, **kwargs):
        voting_id = kwargs.get("pk")
        logger.info(f"Generating ranking for voting {voting_id}")
        queryset = models.VotingUser.objects.ranking(voting_id=voting_id)
        return Response(data=queryset, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_voter_plate(self, request):
        query_params_plate = request.query_params["plate"]
        result = get_voter_plate(query_params_plate)
        return Response(data={"data": result}, status=200)

    @action(detail=False, methods=["POST"])
    def get_voting_user_plate_quantity_pdf(self, request):
        params_serializers = params_serializer.VotingUserParamsSerializer(data=request.data)
        params_serializers.is_valid(raise_exception=True)
        logger.info(f"Generating PDF report for voting event {params_serializers.initial_data['event_vote']}")
        behavior = VotingUserBehavior(event_vote=params_serializers.initial_data["event_vote"])
        pdf_content = behavior.run()
        response = HttpResponse(pdf_content, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="voter_plate.pdf"'
        return response

    @action(detail=False, methods=["POST"])
    def resume_report(self, request, *args, **kwargs):
        serializer = params_serializer.ResumeVotingSerializerParams(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_vote = serializer.validated_data["event_vote"]
        logger.info(f"Generating resumido report for event {event_vote}")
        pdf_content = generate_general_vote_result(event_vote_id=event_vote)
        return HttpResponse(pdf_content, content_type="application/pdf")

    @action(detail=False, methods=["POST"])
    def resume_report_plate_vote(self, request):
        serializer = params_serializer.VoterInPlateSerializerParams(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_vote = serializer.validated_data["event_vote"]
        plate = serializer.validated_data["plate"]
        logger.info(f"Generating plate vote report for event {event_vote} and plate {plate}")
        behavior = VoteByPlateBehavior(event_vote=event_vote, plate=plate)
        pdf_content = behavior.run()
        if pdf_content is None:
            return Response({"detail": "Nenhum dado encontrado."}, status=404)
        return HttpResponse(pdf_content, content_type="application/pdf")

    @action(detail=False, methods=["POST"])
    def get_voter_plate_pdf(self, request):
        serializer = params_serializer.VoterInPlateSerializerParams(data=request.data)
        serializer.is_valid(raise_exception=True)
        plate = serializer.validated_data["plate"]
        logger.info(f"Generating plate vote report for plate {plate}")
        behavior = VoterInPlateResume(plate=plate)
        pdf_content = behavior.run()
        return HttpResponse(pdf_content, content_type="application/pdf")


@extend_schema(tags=["Reports"])
class ResumeVoteViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.ResumeVote.objects.all()
    serializer_class = serializers.ResumeVoteSerializer
    filterset_class = filters.ResumeVoteFilter
    permission_classes_by_action = {"create": (AllowAny,), "partial_update": (AllowAny,), "destroy": (AllowAny,)}

    @extend_schema(
        summary="Obter resumo de votação PDF",
        description="Retorna dados do resumo de votação.",
        responses={200: {"description": "Dados do resumo de votação"}},
    )
    @action(detail=False, methods=["GET"])
    def get_voter_plate_resume_pdf(self, request):
        result = get_resume_vote()
        return Response(data={"data": result}, status=200)

    @extend_schema(
        summary="Relatório de resumo de votação",
        description="Gera um relatório PDF com o resumo da votação.",
        request={
            "application/json": {
                "type": "object",
                "properties": {"event_vote": {"type": "integer"}},
                "required": ["event_vote"],
            }
        },
        responses={
            200: {
                "description": "Relatório PDF gerado",
                "content": {"application/pdf": {"schema": {"type": "string", "format": "binary"}}},
            }
        },
    )
    @action(detail=False, methods=["POST"])
    def resume_report(self, request):
        serializer = params_serializer.ResumeVotingSerializerParams(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_vote = serializer.validated_data["event_vote"]
        logger.info(f"Generating resumido report for event {event_vote}")
        behavior = ResumeVoterProvisory(event_vote=event_vote)
        pdf_content = behavior.run()
        return HttpResponse(pdf_content, content_type="application/pdf")
