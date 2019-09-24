from django.urls import path
from .views import *

urlpatterns = [
    path('api/', snippet_list),#vtuber 全件取得
    path('api/data/<int:pk>', snippet_detail),
    path('api/onlive', onlive_all),#onlive 全件取得
    path('api/onlive/<int:pk>', onlive_detail),
    path('api/onlive/', OnLiveListView.as_view()),
]