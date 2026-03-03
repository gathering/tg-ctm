from django.contrib import admin
from .models import *

admin.site.register(Task)
admin.site.register(Timeslot)
admin.site.register(AssignedTimeslot)
admin.site.register(TimeslotCheckIn)
