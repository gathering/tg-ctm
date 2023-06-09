from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks', views.view_tasks, name='view_tasks'),
    path('task/<int:task_id>', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/timeslots', views.view_timeslots_tasks, name='view_timeslots_tasks'),
    path('timeslots', views.view_timeslots, name='view_timeslots'),
    path('timeslot/<int:timeslot_id>', views.edit_timeslot, name='edit_timeslot'),
    path('timeslot/<int:timeslot_id>/attendance/<int:timeslot_attendance_id>', views.edit_timeslot_attendance, name='register_timeslot_attendance'),
    path('timeslot/<int:timeslot_id>/attendance/<int:timeslot_attendance_id>/delete', views.delete_timeslot_attendance, name='delete_timeslot_attendance'),
    path('timeslot/<int:timeslot_id>/attendance', views.register_attendance, name='register_attendance'),
    path('timeslot/<int:timeslot_id>/attendance/new/<int:user_id>', views.new_timeslot_attendance, name='new_timeslot_attendance'),
    path('timeslot/<int:timeslot_id>/user/<int:user_id>/remove', views.remove_user_from_timeslot, name='remove_user_from_timeslot'),
    path('timeslot/<int:timeslot_id>/unassign_all_unattended', views.remove_all_unattended_from_timeslot, name='unassign_all_unattended'),
    path('timeslot/new', views.new_timeslot, name='edit_timeslot'),
    path('timeslot_users', views.view_timeslots_users, name='view_timeslots_users'),
    path('timeslots_user/<int:timeslot_id>', views.view_timeslot_task_crew, name='view_timeslot_task_crew'),
    path('timeslots_user/<int:timeslot_id>/add', views.new_timeslot_task_crew, name='new_timeslot_task_crew'),
    path('timeslots_user/<int:timeslot_id>/addsearch', views.new_timeslot_task_crew_search, name='new_timeslot_task_crew_search'),
    path('crews', views.view_crews, name='view_crews'),
    path('crew/<int:crew_id>', views.edit_crew, name='edit_crew'),
    path('users', views.view_users, name='view_users'),
    path('user/<int:user_id>', views.view_user, name='view_user'),
    path('sync', views.view_sync_wannabe, name='view_sync_wannabe'),
    path('api/sync', views.sync_wannabe, name='sync_wannabe'),
]
