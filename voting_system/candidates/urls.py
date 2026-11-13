from django.urls import path
from . import views

app_name = 'candidates'

urlpatterns = [
    path('', views.candidates_list, name='candidates_list'),
    path('<int:candidate_id>', views.candidate_detail, name='candidate_detail')
]
