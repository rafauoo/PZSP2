from django.urls import path

from .views.competition import CompetitionList, CompetitionDetail
from .views.index import index

urlpatterns = [
    path('', index, name="index"),

    # path('applications', ),
    # path('applications/<int:id>', ),

    path('competitions', CompetitionList.as_view(), name='competition-list'),
    path('competitions/<int:id>/', CompetitionDetail.as_view(), name='competition-detail'),

    # path('files'),
    # path('files/<int:id'),

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