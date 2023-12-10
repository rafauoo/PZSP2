from django.urls import path

from .views.competition import CompetitionList, CompetitionDetail
from .views.index import index

urlpatterns = [
    path("", index, name="index"),
    path('competitions', CompetitionList.as_view(), name='competition-list'),
    path('competitions/<int:id>/', CompetitionDetail.as_view(), name='competition-detail')
]