from django.urls import path
from . import views

app_name = "votes"

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('<int:poll_id>/', views.poll_detail, name='poll_detail'),
]
