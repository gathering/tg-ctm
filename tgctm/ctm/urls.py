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
    path('timeslot/new', views.new_timeslot, name='edit_timeslot'),
    path('timeslots_crew/<int:timeslot_id>', views.view_timeslot_task_crew, name='view_timeslot_task_crew'),
    path('timeslots_crew/<int:timeslot_id>/add', views.new_timeslot_task_crew, name='new_timeslot_task_crew'),
    path('crews', views.view_crews, name='view_crews'),
    path('crew/<int:crew_id>', views.edit_crew, name='edit_crew'),
    path('users', views.view_users, name='view_users'),
    path('sync', views.view_sync_wannabe, name='view_sync_wannabe'),
    path('api/sync', views.sync_wannabe, name='sync_wannabe'),
]