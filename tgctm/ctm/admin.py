from django.contrib import admin
from .models import *

admin.site.register(Task)
admin.site.register(TaskTimeSlot)
admin.site.register(Crew)
admin.site.register(CrewUser)
admin.site.register(TaskTimeSlotUser)
admin.site.register(Profile)
admin.site.register(CheckInUserTaskTimeSlot)