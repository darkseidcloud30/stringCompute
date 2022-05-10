from django.urls import path

from . import views






urlpatterns = [
    path('', views.overview, name='overview'),
      path('similarity', views.similarity, name='similarity'),
      path('stringToVec', views.stringToVec, name='stringToVec'),
]