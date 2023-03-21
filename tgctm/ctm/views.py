from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

from .idam import TGBT

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    return render(request, 'index.html')

@login_required
def view_tasks(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, 'tasks.html', context)

@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        task = Task.objects.get(id=task_id)
    context = {"task": task, "form": form}
    return render(request, 'edit_task.html', context)

@login_required
def view_timeslots(request):
    timeslots = TaskTimeSlot.objects.all().order_by("starts")
    context = {"timeslots": timeslots}
    return render(request, 'timeslots.html', context)

@login_required
def edit_timeslot(request, timeslot_id):
    timeslot = TaskTimeSlot.objects.get(id=timeslot_id)
    form = TaskTimeSlotForm(request.POST or None, instance=timeslot)
    timeslot_users = TaskTimeSlotUser.objects.filter(timeslot=timeslot_id)
    if form.is_valid():
        form.save()
        timeslot = TaskTimeSlot.objects.get(id=timeslot_id)
    context = {"timeslot": timeslot, "form": form, "timeslot_users": timeslot_users}
    return render(request, 'edit_timeslot.html', context)

@login_required
def new_timeslot(request):
    form = TaskTimeSlotForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("/timeslots")
    context = {"form": form}
    return render(request, 'edit_timeslot.html', context)

@login_required
def edit_timeslot_attendance(request, timeslot_id, timeslot_attendance_id):
    timeslot = TaskTimeSlot.objects.get(id=timeslot_id)
    timeslot_attendance = CheckInUserTaskTimeSlot.objects.get(id=timeslot_attendance_id)
    form = CheckInUserTaskTimeSlotForm(request.POST or None, instance=timeslot_attendance)
    
    if form.is_valid():
        form.save()
        return redirect("/timeslot/" + str(timeslot.id))
    
    context = {"timeslot_attendance":timeslot_attendance, "timeslot": timeslot, "form": form}
    return render(request, 'edit_register_attendance.html', context)

@login_required
def delete_timeslot_attendance(request, timeslot_id, timeslot_attendance_id):
    timeslot_attendance = CheckInUserTaskTimeSlot.objects.get(id=timeslot_attendance_id)
    timeslot_attendance.delete()
    return redirect("/timeslot/" + str(timeslot_id))

@login_required
def new_timeslot_attendance(request, timeslot_id, user_id):
    timeslot = TaskTimeSlot.objects.get(id=timeslot_id)
    User = get_user_model()
    user = User.objects.get(id=user_id)
    form = CheckInUserTaskTimeSlotForm(request.POST or None, initial={"user": user, "timeslot": timeslot})
    context = {"timeslot": timeslot, "form": form}

    if form.is_valid():
        form.save()
        return redirect("/timeslot/" + str(timeslot.id))    
    
    return render(request, 'edit_register_attendance.html', context)

@login_required
def view_timeslots_tasks(request, task_id):
    task = Task.objects.get(id=task_id)
    timeslots = TaskTimeSlot.objects.filter(task=task_id).order_by("starts")
    context = {"tasks": task, "timeslots": timeslots}
    return render(request, 'timeslots.html', context)

@login_required
def view_timeslot_task_crew(request, timeslot_id):
    timeslot = TaskTimeSlot.objects.get(id=timeslot_id)
    timeslot_users = TaskTimeSlotUser.objects.filter(timeslot=timeslot_id)
    context = {"timeslot_users": timeslot_users, "timeslot": timeslot}
    return render(request, 'timeslot_users.html', context)

@login_required
def new_timeslot_task_crew(request, timeslot_id):
    timeslot = TaskTimeSlot.objects.get(id=timeslot_id)
    form = TaskTimeSlotUserForm(request.POST or None, initial={"timeslot": timeslot})

    if form.is_valid():
        form.save()
        return redirect("/timeslot/" + str(timeslot.id))
    
    context = {"timeslot": timeslot, "form": form}
    return render(request, 'new_timeslot_user.html', context)

@login_required
def view_crews(request):
    crews = Crew.objects.all()
    context = {"crews": crews}
    return render(request, "crews.html", context)

@login_required
def edit_crew(request, crew_id):
    crew = Crew.objects.get(id=crew_id)
    form = CrewForm(request.POST or None, instance=crew)
    
    if form.is_valid():
        form.save()
        return redirect("/crew/" + str(crew.id))
    
    context = {"crew":crew, "form": form}
    return render(request, 'edit_crew.html', context)

@login_required
def view_users(request):
    User = get_user_model()
    users = User.objects.filter(profile__isnull=False)
    context = {"users": users}
    return render(request, "users.html", context)

@login_required
def register_attendance(request, timeslot_id):
    form = RegisterAttendanceForm()
    timeslot = TaskTimeSlot.objects.get(id=timeslot_id)
    context = {"timeslot":timeslot, "form": form}
    if request.POST:
        User = get_user_model()
        nfc = request.POST.get("nfc_tag")
        tgbt = TGBT()
        try:
            user = User.objects.filter(profile__wannabe_id=tgbt.get_wannabe_id_from_nfc_tag(nfc)).first()
            if len(CheckInUserTaskTimeSlot.objects.filter(user=user, timeslot=timeslot)) == 0:
                attendance = CheckInUserTaskTimeSlot(user=user, timeslot=timeslot)
                attendance.save()
                context = {"timeslot": timeslot, "form": form, "alerts": [{"text": "Saved!", "color": "success"}]}
            else:
                context = {"timeslot": timeslot, "form": form, "alerts": [{"text": "Duplicate attendance!", "color": "warning"}]}
        except:
            context = {"timeslot": timeslot, "form": form, "alerts": [{"text": "NFC Tag not found!", "color": "danger"}]}

    return render(request, "register_attendance.html", context)