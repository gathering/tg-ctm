from . import views
from django.urls import path

urlpatterns = [
  path('sync', views.wannabe_sync, name='wannabe_sync'),
  path('sync_start', views.wannabe_sync_start, name='wannabe_sync_start'),
]
