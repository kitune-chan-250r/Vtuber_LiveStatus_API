from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/', VtuberList.as_view()),#vtuber 全件取得
    path('api/<str:pk>', VtuberDetail.as_view()),
    path('api/onlive', OnLiveList.as_view()),#onlive 全件取得
    path('api/onlive/<str:pk>/', OnLiveDetail.as_view()),
    path('api/onlive/', OnLiveListView.as_view()),
    #path('api/scheduledlive/', ScheduledLiveListView.as_view()),
    #path('api/scheduledlive/<str:pk>/', ScheduledLiveDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
