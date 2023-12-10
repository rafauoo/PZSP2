from django.urls import path

from .views.application import ApplicationList, ApplicationDetail
from .views.competition import CompetitionList, CompetitionDetail
from .views.file import FileList, FileDetail
from .views.index import index

urlpatterns = [
    path('', index, name="index"),

    path('applications', ApplicationList.as_view(), name="application-list"),
    path('applications/<int:id>', ApplicationDetail.as_view(), name="application-detail"),

    path('competitions', CompetitionList.as_view(), name='competition-list'),
    path('competitions/<int:id>', CompetitionDetail.as_view(), name='competition-detail'),

    path('files', FileList.as_view(), name="file-list"),
    path('files/<int:id>', FileDetail.as_view(), name="file-detail"),

    # path('groups'),
    # path('groups/<int:id>'),

    # path('participants'),
    # path('participants/<int:id>'),

    # path('permissions'),
    # path('permissions/<int:id>'),

    # path('schools'),
    # path('schools/<int:id>'),

    # path('users'),
    # path('users/<int:id>'),

]
