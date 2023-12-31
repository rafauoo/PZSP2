from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from .views.application import ApplicationList, ApplicationDetail
from .views.auth import RegisterView, ProfileView
from .views.competition import CompetitionList, CompetitionDetail
from .views.competition_type import CompetitionTypeList
from .views.file import FileList, FileDetail
from .views.index import index
from .views.participant import ParticipantList, ParticipantDetail
from .views.school import SchoolList, SchoolDetail
from .views.user import UserList, UserDetail

urlpatterns = [
    path('', index, name="index"),

    path('applications/', ApplicationList.as_view(), name="application-list"),
    path('applications/<int:id>/', ApplicationDetail.as_view(), name="application-detail"),

    path('competitions/', CompetitionList.as_view(), name='competition-list'),
    path('competitions/<int:id>/', CompetitionDetail.as_view(), name='competition-detail'),

    path('competition_types/', CompetitionTypeList.as_view(), name='competition_type-list'),

    path('files/', FileList.as_view(), name="file-list"),
    path('files/<int:id>/', FileDetail.as_view(), name="file-detail"),

    # path('groups/', GroupList.as_view(), name="group-list"),
    # path('groups/<int:id>/', GroupDetail.as_view(), name="group-detail"),

    path('participants/', ParticipantList.as_view(), name="participant-list"),
    path('participants/<int:id>/', ParticipantDetail.as_view(), name="participant-detail"),

    # path('permissions/', PermissionList.as_view(), name="permission-list"),
    # path('permissions/<int:id>/', PermissionDetail.as_view(), name="permission-detail"),

    path('schools/', SchoolList.as_view(), name="school-list"),
    path('schools/<int:id>/', SchoolDetail.as_view(), name="school-detail"),

    path('users/', UserList.as_view(), name="user-list"),
    path('users/<int:id>/', UserDetail.as_view(), name="user-detail"),

    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', ProfileView.as_view(), name='me')
]
