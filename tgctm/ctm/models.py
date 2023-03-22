from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class TaskTimeSlot(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    max_participants = models.IntegerField(blank=True)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task.name + " (" + str(self.starts) + " - " + str(self.ends) + ")"
    
    @property
    def num_assigned_users(self):
        return len(TaskTimeSlotUser.objects.filter(timeslot=self.id))

    @property
    def assigned_users(self):
        return TaskTimeSlotUser.objects.filter(timeslot=self.id)
    
    @property 
    def num_assiged_users_checked_in(self):
        return len(CheckInUserTaskTimeSlot.objects.filter(timeslot=self.id))

class Crew(models.Model):
    name = models.CharField(max_length=200)
    crew_id = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def users(self):
        return CrewUser.objects.filter(crew=self.id)

    @property
    def num_users(self):
        return len(CrewUser.objects.filter(crew=self.id))
    
    @property
    def num_users_assigned(self):
        if len(self.users) == 0:
            return 0
        num_assigned = 0
        for crewuser in self.users:
            if crewuser.user.profile.is_assigned_any_timeslot > 0:
                num_assigned=num_assigned+1
        return num_assigned
    
    @property
    def percentage_users_with_assigned_timeslot(self):
        if self.num_users > 0:
            return (self.num_users_assigned / self.num_users) * 100
        else:
            return 0

class CrewUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class TaskTimeSlotUser(models.Model):
    timeslot = models.ForeignKey(TaskTimeSlot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.timeslot.task.name + " (" + str(self.timeslot.starts) + " - " + str(self.timeslot.ends) + ") - " + self.user.username

    @property
    def attendance(self):
        return CheckInUserTaskTimeSlot.objects.get(user=self.user.id, timeslot=self.timeslot)
    

class CheckInUserTaskTimeSlot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TaskTimeSlot, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.wannabe_user + " - " + self.timeslot
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wannabe_id = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username
    
    @property
    def is_assigned_any_timeslot(self):
        if len(TaskTimeSlotUser.objects.filter(user=self.user)) > 0:
            return True
        return False

    @property
    def num_assigned_timeslots(self):
        return len(TaskTimeSlotUser.objects.filter(user=self.user))
    
    @property
    def assigned_timeslots(self):
        return TaskTimeSlotUser.objects.filter(user=self.user)

    @property 
    def get_all_crews(self):
        crewusers = CrewUser.objects.filter(user=self.user)
        crews = list()
        for crewuser in crewusers:
            crews.append(crewuser.crew)
        return crews
    