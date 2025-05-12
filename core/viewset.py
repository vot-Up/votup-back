from django.db import transaction, IntegrityError
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from reversion import revisions

from core import mixins, params_serializer, messages, behaviors, helpers
from core import models, serializers, filters, exceptions, actions


class ViewSetPermissions(ViewSet):
    permission_classes_by_action: dict = {}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return super().get_permissions()


class ViewSetBase(viewsets.ModelViewSet,
                  mixins.ViewSetExpandMixin):

    def create(self, request, *args, **kwargs):
        with transaction.atomic(), revisions.create_revision():
            revisions.set_user(request.user)
            revisions.set_comment("CREATE")
            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        with transaction.atomic(), revisions.create_revision():
            revisions.set_user(request.user)
            revisions.set_comment("UPDATE")
            return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.make_queryset_expandable(request)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.make_queryset_expandable(request)
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            return super(ViewSetBase, self).destroy(request, *args, **kwargs)
        except IntegrityError:
            raise exceptions.ForeignKeyException


class VoterViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.Voter.objects.all()
    serializer_class = serializers.VoterSerializer
    filterset_class = filters.VoterFilter
    ordering = ('-active', '-modified_at',)
    permission_classes_by_action = {'create': (AllowAny,), 'partial_update': (AllowAny,), 'destroy': (AllowAny,)}


class CandidateViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.Candidate.objects.all()
    serializer_class = serializers.CandidateSerializer
    filterset_class = filters.CandidateFilter
    ordering = ('-active', '-modified_at',)
    permission_classes_by_action = {'create': (AllowAny,), 'partial_update': (AllowAny,), 'destroy': (AllowAny,)}


class PlateViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.Plate.objects.all()
    serializer_class = serializers.PlateSerializer
    filterset_class = filters.PlateFilter
    permission_classes_by_action = {
        'list': (AllowAny,),
        'create': (AllowAny,),
        'partial_update': (AllowAny,),
        'destroy': (AllowAny,)
    }
    ordering = ('-active', '-modified_at',)

    def update(self, request, *args, **kwargs):
        if 'active' in request.data:
            if request.data.get('active'):
                list_candidate = models.PlateUser.objects.filter(plate=self.get_object().id).values('candidate_id')
                plate_list = models.PlateUser.objects.filter(
                    candidate__in=list_candidate
                ).values('plate_id').exclude(plate_id=self.get_object().id)

                if models.Plate.objects.filter(id__in=plate_list, active=True).exists():
                    raise exceptions.PlateUserIsActiveException

        return super().update(request, *args, **kwargs)


class VotingViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.EventVoting.objects.all()
    serializer_class = serializers.EventVotingSerializer
    filterset_class = filters.EventVotingFilter
    ordering = ('-active', '-id',)
    permission_classes = (AllowAny,)

    def destroy(self, request, *args, **kwargs):
        if not self.get_object().active:
            try:
                actions.EventVotingAction.delete_historic(kwargs.get('pk'))
                return Response(data="Foi excluido com sucesso", status=200)
            except Exception:
                raise exceptions.DeleteVoteActiveException
        else:
            raise exceptions.DeleteVoteActiveException()

    @action(methods=['PATCH'], detail=False)
    def active_vote(self, request, *args, **kwargs):
        param_serializer = params_serializer.ActiveOrCloseVoteParamSerializer(data=request.data)
        param_serializer.is_valid(raise_exception=True)
        actions.VotingAction.active_vote(**param_serializer.validated_data)
        return Response(data={'message': messages.ACTIVE_VOTE}, status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=False)
    def close_vote(self, request, *args, **kwargs):
        param_serializer = params_serializer.ActiveOrCloseVoteParamSerializer(data=request.data)
        param_serializer.is_valid(raise_exception=True)
        actions.VotingAction.close_vote(**param_serializer.validated_data)
        return Response(data={'message': messages.CLOSE_VOTE}, status=status.HTTP_200_OK)


class PlateUserViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.PlateUser.objects.all()
    serializer_class = serializers.PlateUserSerializer
    filterset_class = filters.PlateUserFilter
    permission_classes_by_action = {'create': (AllowAny,), 'partial_update': (AllowAny,), 'destroy': (AllowAny,)}

    @action(detail=False, methods=['DELETE'])
    def delete_user_plate(self, request, *args, **kwargs):
        param_serializer = params_serializer.PlateUserParamSerializer(data=request.data)
        param_serializer.is_valid(raise_exception=True)
        actions.PlateUserAction.delete_user_plate(**param_serializer.validated_data)
        return Response(status=200)


class VotingPlateViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.VotingPlate.objects.all()
    serializer_class = serializers.VotingPlateSerializer
    filterset_class = filters.VotingPlateFilter
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['DELETE'])
    def delete_voting_plate(self, request, *args, **kwargs):
        param_serializer = params_serializer.VotingPlateParamSerializer(data=request.data)
        param_serializer.is_valid(raise_exception=True)
        actions.VotingPlateAction.delete_voting_plate(**param_serializer.validated_data)
        return Response(status=200)

    @action(detail=False, methods=['GET'])
    def check_associate(self, request, *args, **kwargs):
        id_associate = request.query_params['associate']
        result = actions.VotingPlateAction.check_plate_voting(id_associate)
        return Response(data={"data": result}, status=200)


class VotingUserViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.VotingUser.objects.all()
    serializer_class = serializers.VotingUserSerializer
    filterset_class = filters.VotingUserFilter
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['POST'])
    def voting(self, request, *args, **kwargs):
        param_serializer = params_serializer.InitVotingParamSerializer(data=request.data)
        param_serializer.is_valid(raise_exception=True)
        voting_plate = actions.VotingUserAction.get_voting_user(**param_serializer.validated_data)
        return Response(voting_plate, status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def ranking(self, request, *args, **kwargs):
        voting_id = kwargs.get('pk')
        queryset = models.VotingUser.objects.ranking(voting_id=voting_id)
        return Response(data=queryset, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def get_voter_plate(self, request):
        query_params_plate = request.query_params['plate']
        result = actions.VotingUserAction.get_voter_plate(query_params_plate)
        return Response(data={"data": result}, status=200)

    @action(detail=False, methods=['POST'])
    def get_voting_user_plate_quantity_pdf(self, request):
        params_serializers = params_serializer.VotingUserParamsSerializer(data=request.data)
        params_serializers.is_valid(raise_exception=True)

        behavior = behaviors.VotingUserBehavior(event_vote=params_serializers.initial_data['event_vote'])
        pdf_content = behavior.run()

        response = HttpResponse(pdf_content, content_type='application/pdf', status=200)
        response['Content-Disposition'] = 'inline; filename=resume.pdf'

        return response

    @action(detail=False, methods=['POST'])
    def resume_report(self, request, *args, **kwargs):
        result_serializer = params_serializer.ResumeVotingSerializerParams(
            data=request.data,
            context={'request': request}
        )
        result_serializer.is_valid(raise_exception=True)
        response = helpers.generate_report_to_download(
            name="resume_vote",
            params=result_serializer.validated_data
        )
        return response

    @action(detail=False, methods=['POST'])
    def resume_report_plate_vote(self, request, *args, **kwargs):
        result_serializer = params_serializer.VoterInPlateSerializerParams(
            data=request.data,
            context={'request': request}
        )
        result_serializer.is_valid(raise_exception=True)
        response = helpers.generate_report_to_plate_user_download(
            name="resume_vote_voter_in_plate",
            params=result_serializer.validated_data
        )
        return response

    @action(detail=False, methods=['POST'])
    def get_voter_plate_pdf(self, request):
        params_serializers = params_serializer.VoterPlateParamsSerializer(data=request.data)
        params_serializers.is_valid(raise_exception=True)

        behavior = behaviors.VoterInPlate(plate=params_serializers.initial_data['plate'])
        pdf_content = behavior.run()

        response = HttpResponse(pdf_content, content_type='application/pdf', status=200)
        response['Content-Disposition'] = 'inline; filename=resume.pdf'

        return response


class ResumeVoteViewSet(ViewSetBase, ViewSetPermissions):
    queryset = models.ResumeVote.objects.all()
    serializer_class = serializers.ResumeVoteSerializer
    filterset_class = filters.ResumeVoteFilter
    permission_classes_by_action = {'create': (AllowAny,), 'partial_update': (AllowAny,), 'destroy': (AllowAny,)}

    @action(detail=False, methods=['GET'])
    def get_voter_plate_resume_pdf(self, request):
        result = actions.ResumeVoteAction.get_resume_vote()
        return Response(data={"data": result}, status=200)

    @action(detail=False, methods=['POST'])
    def resume_report(self, request, *args, **kwargs):
        result_serializer = params_serializer.ResumeVotingSerializerParams(
            data=request.data,
            context={'request': request}
        )
        result_serializer.is_valid(raise_exception=True)
        response = helpers.generate_report_to_resume_download(
            name="resume_vote",
            params=result_serializer.validated_data
        )
        return response
