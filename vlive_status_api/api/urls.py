from django.urls import path
from api import views

urlpatterns = [
    path('api/', views.snippet_list),
    path('api/data/<int:pk>', views.snippet_detail),
    path('api/onlive', views.onlive_all),
]