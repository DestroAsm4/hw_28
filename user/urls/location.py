from django.contrib import admin
from django.urls import path

from user.views.location import *

urlpatterns = [

    path('', LocationListView.as_view()),
    path('<int:pk>/', LocationDetailView.as_view()),
    path('create/', LocationCreateView.as_view()),
    path('<int:pk>/update/', LocationUpdateView.as_view()),
    path('<int:pk>/delete/', LocationDeleteView.as_view()),
]