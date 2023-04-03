from django.urls import path
from .views import *
urlpatterns = [
    path('allHackathons/',AllHackathons),
    path('registerHackathon/<int:pk>/',RegisterHackathon),
    path('createHackathon/',CreateHackthon),
    path('makeSubmisson/<int:pk>/',MakeSubmission),
    path('getEnrolled/',GetEnrolledHackathon),
    path('getSubmission/<int:pk>/',GetSubmission)
]