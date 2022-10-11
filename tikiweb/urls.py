from django.urls import path

from . import views

urlpatterns = [
    path('', views.top, name='top'),
    path('region/<str:region>/', views.top, name='top_by_region'),
    path('region/<str:region>/count/<int:player_count>/', views.top, name='top_n'),
    path('player/<str:account_id>/', views.player, name='player'),
]
