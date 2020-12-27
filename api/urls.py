from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('vtuber/', VtuberList.as_view()),#vtuber 全件取得
    path('vtuber/<str:pk>', VtuberDetail.as_view()),
    path('onlive', OnLiveList.as_view()),#onlive 全件取得
    path('onlive/<str:pk>/', OnLiveDetail.as_view()),
    path('onlive/', OnLiveListView.as_view()),
    path('reminder/', ReminderListView.as_view()),#2020-12-28 reminder
    path('reminder/<str:pk>/', ReminderDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)