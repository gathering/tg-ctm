from django.db import models
from django.utils.translation import gettext_lazy as _
from ..profiles.models import Profile


class Task(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  send_reminders = models.BooleanField(default=True)
  reminder_info = models.TextField(blank=True)

  def __str__(self): return self.name
  # extra properties: timeslots


class Timeslot(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="timeslots")
  max_participants = models.IntegerField(blank=True, null=True)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()

  def __str__(self): return f"{self.task.name} ({self.start_time.astimezone().strftime("%Y-%m-%d %H:%M")})"
  # extra properties: assigned_profiles, checkins

  @property
  def extra_checkins(self):
    return self.checkins.filter(extra=True)

  @property
  def no_shows(self):
    return self.assigned_timeslots.filter(no_show=True)


class AssignedTimeslot(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="assigned_timeslots")
  timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE, related_name="assigned_timeslots")
  no_show = models.BooleanField(default=False)

  class ReminderStatus(models.TextChoices):
    NONE = "NO", _("None")
    FIRST = "1R", _("First reminder sent")
    SECOND = "2R", _("Second reminder sent")
    DISABLE = "DS", _("Disable reminder")

  reminder_status = models.CharField(max_length=2, choices=ReminderStatus.choices, default=ReminderStatus.NONE)

  def __str__(self): return f"{self.profile} - {self.timeslot}"
  # extra properties: none

  @property
  def checkin(self):
    return TimeslotCheckIn.objects.filter(profile=self.profile, timeslot=self.timeslot).first()


class TimeslotCheckIn(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="task_checkins")
  timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE, related_name="checkins")
  extra = models.BooleanField(default=False)

  def __str__(self): return f"{self.profile} - {self.timeslot}"
