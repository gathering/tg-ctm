from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

import re

from .models import *
from .forms import *

from .idam import TGBT

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    chiefcrews = CrewUser.objects.filter(user=request.user, is_chief=True)
    crewusers = CrewUser.objects.filter(crew__in=[crewuser.crew for crewuser in chiefcrews])
    context = {"chiefcrews": chiefcrews, "crewusers": crewusers}
    return render(request, 'index.html', context)

@login_required
@staff_member_required
def view_tasks(request):
    tasks = Task.objects.all()
    context = {"tasks": tasks}
    return render(request, 'tasks.html', context)

@login_required
@staff_member_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        task = Task.objects.get(id=task_id)
    context = {"task": task, "form": form}
    return render(request, 'edit_task.html', context)

@login_required
@staff_member_required
def view_timeslots(request):
    timeslots = TaskTimeSlot.objects.all().order_by("starts")
    context = {"timeslots": timeslots}
    return render(request, 'timeslots.html', context)

@login_required
@staff_member_required
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
@staff_member_required
def new_timeslot(request):
    form = TaskTimeSlotForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("/timeslots")
    context = {"form": form}
    return render(request, 'edit_timeslot.html', context)

@login_required
@staff_member_required
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
@staff_member_required
def delete_timeslot_attendance(request, timeslot_id, timeslot_attendance_id):
    timeslot_attendance = CheckInUserTaskTimeSlot.objects.get(id=timeslot_attendance_id)
    timeslot_attendance.delete()
    return redirect("/timeslot/" + str(timeslot_id))

@login_required
@staff_member_required
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
@staff_member_required
def view_timeslots_tasks(request, task_id):
    task = Task.objects.get(id=task_id)
    timeslots = TaskTimeSlot.objects.filter(task=task_id).order_by("starts")
    context = {"tasks": task, "timeslots": timeslots}
    return render(request, 'timeslots.html', context)

@login_required
@staff_member_required
def view_timeslot_task_crew(request, timeslot_id):
    timeslot = TaskTimeSlot.objects.get(id=timeslot_id)
    timeslot_users = TaskTimeSlotUser.objects.filter(timeslot=timeslot_id)
    context = {"timeslot_users": timeslot_users, "timeslot": timeslot}
    return render(request, 'timeslot_users.html', context)

@login_required
@staff_member_required
def new_timeslot_task_crew(request, timeslot_id):
    timeslot = TaskTimeSlot.objects.get(id=timeslot_id)
    form = TaskTimeSlotUserForm(request.POST or None, initial={"timeslot": timeslot})

    if form.is_valid():
        form.save()
        return redirect("/timeslot/" + str(timeslot.id))

    context = {"timeslot": timeslot, "form": form}
    return render(request, 'new_timeslot_user.html', context)

@login_required
@staff_member_required
def new_timeslot_task_crew_search(request, timeslot_id):
    timeslot = TaskTimeSlot.objects.get(id=timeslot_id)
    timeslots = TaskTimeSlot.objects.all()
    User = get_user_model()
    users = User.objects.all()
    context = {"timeslots": timeslots, "cur_timeslot": timeslot, "users": users}

    if request.POST:
        user = User.objects.get(id=request.POST.get('id_user'))
        timeslot = TaskTimeSlot.objects.get(id=request.POST.get('id_timeslot'))

        if TaskTimeSlotUser.objects.filter(user=user, timeslot=timeslot).exists():
            context = {"timeslots": timeslots, "cur_timeslot": timeslot, "users": users, "alerts": [{"text": "Duplicate attendance!", "color": "warning"}]}
            return render(request, 'new_timeslot_user_search.html', context)

        timeslot_user = TaskTimeSlotUser(user=user, timeslot=timeslot)
        timeslot_user.save()
        return redirect("/timeslots_user/" + str(timeslot.id) + "/addsearch")


    return render(request, 'new_timeslot_user_search.html', context)

@login_required
@staff_member_required
def view_crews(request):
    crews = Crew.objects.all()
    context = {"crews": crews}
    return render(request, "crews.html", context)

@login_required
@staff_member_required
def edit_crew(request, crew_id):
    crew = Crew.objects.get(id=crew_id)
    form = CrewForm(request.POST or None, instance=crew)
    crewusers = CrewUser.objects.filter(crew_id=crew_id)
    if form.is_valid():
        form.save()
        return redirect("/crew/" + str(crew.id))

    context = {"crew":crew, "form": form, "crewusers": crewusers}
    return render(request, 'edit_crew.html', context)

@login_required
@staff_member_required
def view_users(request):
    User = get_user_model()
    users = User.objects.filter(profile__isnull=False)
    context = {"users": users}
    return render(request, "users.html", context)

@login_required
@staff_member_required
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
                if not TaskTimeSlotUser.objects.filter(user=user, timeslot=timeslot).exists():
                    context = {"timeslot": timeslot, "form": form, "alerts": [{"text": "User not registered to this timeslot!", "color": "danger"}]}
                else:
                    attendance = CheckInUserTaskTimeSlot(user=user, timeslot=timeslot)
                    attendance.save()
                    context = {"timeslot": timeslot, "form": form, "alerts": [{"text": "User checked in!", "color": "success"}]}
            else:
                context = {"timeslot": timeslot, "form": form, "alerts": [{"text": "Duplicate attendance!", "color": "warning"}]}
        except:
            context = {"timeslot": timeslot, "form": form, "alerts": [{"text": "NFC Tag not found!", "color": "danger"}]}

    return render(request, "register_attendance.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def view_sync_wannabe(request):
    User = get_user_model()
    num_users = User.objects.all().count()
    num_crews = Crew.objects.all().count()

    context = {"num_users": num_users, "num_crews": num_crews}
    return render(request, 'wannabe_sync.html', context)

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def sync_wannabe(request):
    # Little bit ugly sync code
    tgbt = TGBT()
    all_crews_all_users = tgbt.get_all_crews_with_crew_members()
    User = get_user_model()
    num_new_users = 0
    num_new_crews = 0
    current_syced_wannabe_users = User.objects.filter(profile__wannabe_id__isnull=False)
    for crew in all_crews_all_users:
        crew['name']
        if not Crew.objects.filter(crew_id=crew['id']):
            new_crew = Crew(name=crew['name'], crew_id=crew['id'])
            new_crew.save()
            num_new_crews=num_new_crews+1
        else:
            new_crew = Crew.objects.get(crew_id=crew['id'])
        for user in crew['users']:
            if not User.objects.filter(email=user['profile']['email']).exists():
                full_name = remove_emojis(user['profile']['name']) # This is because of you, Sklirg.
                first_name, last_name = str(full_name).rsplit(' ', 1)
                new_user = User(username=user['profile']['email'], email=user['profile']['email'], first_name=first_name, last_name=last_name)
                new_user.save()
                new_user.profile.wannabe_id = user['user_id']
                new_user.save()
                num_new_users=num_new_users+1
            else:
                new_user = User.objects.get(email=user['profile']['email'])

            current_syced_wannabe_users = current_syced_wannabe_users.exclude(id=new_user.id)

            if not CrewUser.objects.filter(user=new_user, crew=new_crew).exists():
                is_chief = True if user['role']['id'] in {8, 9} else False
                new_crew_user = CrewUser(user=new_user, crew=new_crew, is_chief=is_chief)
                new_crew_user.save()

    deleted_users = 0
    for olduser in current_syced_wannabe_users:
        if not olduser.is_superuser:
            olduser.delete()
            deleted_users = deleted_users+1

    result = {"new_users": num_new_users, "new_crews": num_new_crews, "deleted_users": deleted_users}

    return JsonResponse(result)
