from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/', snippet_list),#vtuber 全件取得
    path('api/data/<int:pk>', snippet_detail),
    path('api/onlive', onlive_all),#onlive 全件取得
    path('api/onlive/<str:pk>/', OnLiveDetail.as_view()),
    path('api/onlive/', OnLiveListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)