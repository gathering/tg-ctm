from . import views
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
  path('', views.view_tasks, name='view_tasks'),
  path('<int:task_id>', views.view_task, name='view_task'),
  path('<int:task_id>/assign_from_crew/<int:crew_id>', views.assign_task_from_crew, name='assign_task_from_crew'),
  path('<int:task_id>/edit', views.edit_task, name='edit_task'),
  path('<int:task_id>/delete', views.delete_task, name='delete_task'),
  path('new', views.new_task, name='new_task'),
  path('timeslots', views.view_timeslots, name='view_timeslots'),
  path('timeslots/<int:timeslot_id>', views.view_timeslot, name='view_timeslot'),
  path('timeslots/<int:timeslot_id>/assign', views.assign_timeslot, name='assign_timeslot'),
  path('timeslots/<int:timeslot_id>/checkin', views.checkin_timeslot, name='checkin_timeslot'),
  path('timeslots/<int:timeslot_id>/checkin/<str:rfid>', views.scan_rfid, name='scan_rfid'),
  path('timeslots/<int:timeslot_id>/noshows', views.mark_noshows, name='mark_noshows'),
  path('timeslots/<int:timeslot_id>/edit', views.edit_timeslot, name='edit_timeslot'),
  path('timeslots/<int:timeslot_id>/delete', views.delete_timeslot, name='delete_timeslot'),
  path('timeslots/<int:timeslot_id>/raw_crewlist', views.raw_crewlist, name='raw_crewlist'),
  path('timeslots/<int:timeslot_id>/users/<int:profile_id>/add', views.add_user_to_timeslot, name='add_user_to_timeslot'),
  path('timeslots/<int:timeslot_id>/users/<int:profile_id>/checkin', views.check_in_user_to_timeslot, name='check_in_user_to_timeslot'),
  path('timeslots/<int:timeslot_id>/users/<int:profile_id>/remove', views.remove_user_from_timeslot, name='remove_user_from_timeslot'),
  path('timeslots/new/<int:task_id>', views.new_timeslot, name='new_timeslot'),
]
