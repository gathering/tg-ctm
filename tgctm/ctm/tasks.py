from datetime import timedelta
from django.utils import timezone
from timeloop import Timeloop
from .models import TaskTimeSlotUser
from .utils import send_message_to_user
from django.contrib.auth import get_user_model

timeloop = Timeloop()

@timeloop.job(interval=timedelta(seconds=10))
def send_reminders():
    timeslotusers = TaskTimeSlotUser.objects.all()
    for timeslotuser in timeslotusers:
        # if 5 minutes left, send reminder
        if timeslotuser.reminder_status != "TW" and timeslotuser.timeslot.starts < timezone.now() + timedelta(minutes=10) and timeslotuser.timeslot.starts > timezone.now():
            print("Send reminder to " + timeslotuser.user.username + " for task " + str(timeslotuser.timeslot) + " (10 minutes)")
            success = send_message_to_user(timeslotuser.user, "🔔 Ti minutter igjen til `" + str(timeslotuser.timeslot) + "`! Oppmøte er ved trappen utenfor logistikk.")
            if success:
                timeslotuser.reminder_status = "TW"
                timeslotuser.save()
            return
        # if 60 minutes left, send reminder
        if timeslotuser.reminder_status == "NO" and timeslotuser.timeslot.starts < timezone.now() + timedelta(hours=2) and timeslotuser.timeslot.starts > timezone.now():
            print("Send reminder to " + timeslotuser.user.username + " for task " + str(timeslotuser.timeslot) + " (2 hours left)")
            success = send_message_to_user(timeslotuser.user, "🔔 Hei, oppgaven `" + str(timeslotuser.timeslot) + "` starter om under to timer. Oppmøte er ved trappen utenfor logistikk.")
            if success:
                timeslotuser.reminder_status = "ON"
                timeslotuser.save()
            return

timeloop.start()
