from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Competition, User, Application, Participant, \
    PendingApproval
from django.db.models import Count
from ..permissions import allow_admin


@authentication_classes([JWTAuthentication])
class StatsView(APIView):
    @allow_admin
    def get(self, request, *args, **kwargs):
        current_date = datetime.now()

        ongoing_competitions = Competition.objects.filter(
            start_at__lte=current_date, end_at__gte=current_date)
        upcoming_competitions = Competition.objects.filter(
            start_at__gt=current_date)
        finished_competitions = Competition.objects.filter(
            end_at__lt=current_date)

        competitions_count = Competition.objects.count()

        users_count = User.objects.count()
        school_users_count = User.objects.exclude(school__isnull=True).count()

        applications_count = Application.objects.count()
        participants_count = Participant.objects.count()
        attachments_count = Participant.objects.exclude(
            attachment__isnull=True).count()

        approvals_count = PendingApproval.objects.count()

        competition_participants = {
            comp['id']: {'title': comp['title'],
                         'participants_count': comp['participants_count']}
            for comp in Competition.objects.annotate(
                participants_count=Count('application__participant')).values(
                'id',
                'title',
                'participants_count')}

        user_participants = {
            user['id']: {'user': f"{user['first_name']} {user['last_name']}",
                         'participants_count': user['participants_count']} for
            user in
            User.objects.annotate(
                participants_count=Count('application__participant')).values(
                'id',
                'first_name',
                'last_name',
                'participants_count')}

        competition_dates = {
            comp['id']: {'start_at': comp['start_at'], 'end_at': comp['end_at']}
            for comp in Competition.objects.values('id', 'start_at', 'end_at')}
        data = {
            'competitions_count': competitions_count,
            'ongoing_competitions_count': ongoing_competitions.count(),
            'upcoming_competitions_count': upcoming_competitions.count(),
            'finished_competitions_count': finished_competitions.count(),
            'competitions_dates': competition_dates,

            'users_count': users_count,
            'school_user_count': school_users_count,
            'applications_count': applications_count,
            'participants_count': participants_count,
            'attachments_count': attachments_count,
            'approvals_count': approvals_count,
            'competition_participants': competition_participants,
            'user_participants': user_participants
        }

        return Response(data=data, status=status.HTTP_200_OK)
