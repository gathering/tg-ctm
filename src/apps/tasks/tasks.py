from datetime import timedelta
from django.utils import timezone
from timeloop import Timeloop
from apps.tasks.utils import send_message_to_user
from .models import AssignedTimeslot

timeloop = Timeloop()

@timeloop.job(interval=timedelta(minutes=1))
def send_reminders():
  try:
    assigned_timeslots = AssignedTimeslot.objects.all()
    for assigned_timeslot in assigned_timeslots:
      # if 5 minutes left, send reminder
      if assigned_timeslot.reminder_status != AssignedTimeslot.ReminderStatus.SECOND and \
          assigned_timeslot.timeslot.start_time < timezone.now() + timedelta(minutes=10) and \
          assigned_timeslot.timeslot.start_time > timezone.now():
        print(f"Send reminder to {assigned_timeslot.profile} for task {assigned_timeslot.timeslot} (10 minutes)")
        success = send_message_to_user(assigned_timeslot.profile.user, f"🔔 Ti minutter igjen til `{assigned_timeslot.timeslot}`! {assigned_timeslot.timeslot.task.reminder_info}")
        if success:
          assigned_timeslot.reminder_status = AssignedTimeslot.ReminderStatus.SECOND
          assigned_timeslot.save()
      # if 60 minutes left, send reminder
      elif assigned_timeslot.reminder_status == AssignedTimeslot.ReminderStatus.NONE and \
          assigned_timeslot.timeslot.start_time < timezone.now() + timedelta(hours=2) and \
          assigned_timeslot.timeslot.start_time > timezone.now():
        print(f"Send reminder to {assigned_timeslot.profile} for task {assigned_timeslot.timeslot} (2 hours left)")
        success = send_message_to_user(assigned_timeslot.profile.user, f"🔔 Hei, oppgaven `{assigned_timeslot.timeslot}` starter om under to timer. {assigned_timeslot.timeslot.task.reminder_info}")
        if success:
          assigned_timeslot.reminder_status = AssignedTimeslot.ReminderStatus.FIRST
          assigned_timeslot.save()
  except Exception as e:
    print(e)

timeloop.start()
