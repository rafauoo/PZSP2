from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from ..models import Competition, User, Application, Participant
from ..permissions import allow_admin


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

        data = {
            'competitions_count': competitions_count,
            'ongoing_competitions_count': ongoing_competitions.count(),
            'upcoming_competitions_count': upcoming_competitions.count(),
            'finished_competitions_count': finished_competitions.count(),

            'users_count': users_count,
            'school_user_count': school_users_count,
            'applications_count': applications_count,
            'participants_count': participants_count,
            'attachments_count': attachments_count,
        }

        return Response(data=data, status=status.HTTP_200_OK)
