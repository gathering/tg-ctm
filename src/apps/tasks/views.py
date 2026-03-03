from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST

from apps.tasks.utils import send_message_to_user
from .random import get_random
from .models import *
from ..profiles.models import Profile, Crew
from django.urls import reverse
from ..profiles.idam import TGBT
from django.http import JsonResponse

@login_required
@permission_required('tasks.view_task')
def view_tasks(request): return render(request, 'tasks/task_list.html', { "tasks": Task.objects.all() })

@login_required
@permission_required('tasks.view_task')
def view_task(request, task_id):
  task = Task.objects.get(id=task_id)
  crews = []
  for crew in Crew.objects.all():
    members = crew.members_without_team.count()
    assigned = crew.members_without_team.filter(profile__assigned_timeslots__timeslot__task=task).distinct().count()
    percentage = int((assigned / members) * 100) if members > 0 else 0
    teams = []
    for team in crew.teams.all():
      team_members = team.members.count()
      team_assigned = team.members.filter(profile__assigned_timeslots__timeslot__task=task).distinct().count()
      team_percentage = int((team_assigned / team_members) * 100) if team_members > 0 else 0
      teams.append((team, team_members, team_assigned, team_percentage))
    crews.append((crew, members, assigned, percentage, teams))
  return render(request, 'tasks/task_view.html', { "task": task, "crews": crews })

@login_required
@permission_required('tasks.add_assignedtimeslot')
def assign_task_from_crew(request, task_id, crew_id):
  task = Task.objects.get(id=task_id)
  crew = Crew.objects.get(id=crew_id)
  crew_members_without_team = [(member, AssignedTimeslot.objects.filter(profile=member.profile, timeslot__task=task, no_show=False).first()) for member in crew.members_without_team.all().order_by("profile__user__last_name", "profile__user__first_name", "-is_chief")]
  crew_teams = [(team, [(member, AssignedTimeslot.objects.filter(profile=member.profile, timeslot__task=task, no_show=False).first()) for member in team.members.all().order_by("profile__user__last_name", "profile__user__first_name", "-is_chief")]) for team in crew.teams.all()]
  return render(request, 'tasks/task_assign_from_crewlist.html', { "task": task, "crew": crew, "crew_members_without_team": crew_members_without_team, "crew_teams": crew_teams })

@login_required
@permission_required('tasks.change_task')
def edit_task(request, task_id):
  task = Task.objects.get(id=task_id)
  if request.POST:
    fields = {
      "name": request.POST.get("name"),
      "description": request.POST.get("description"),
      "send_reminders": request.POST.get("send_reminders") == "on",
      "reminder_info": request.POST.get("reminder_info"),
    }
    for key, value in fields.items():
      if value != getattr(task, key):
        setattr(task, key, value)
    task.save()
    return redirect(reverse("view_task", args=[task_id]))
  return render(request, 'tasks/task_edit.html', {
    "task": task,
    "random": {
      "name": get_random("task_name"),
      "description": get_random("task_description"),
      "reminder_info": get_random("reminder_info"),
    }
  })

@login_required
@permission_required('tasks.delete_task')
def delete_task(request, task_id):
  Task.objects.get(id=task_id).delete()
  return redirect(reverse("view_tasks"))

@login_required
@permission_required('tasks.add_task')
def new_task(request):
  if request.POST:
    task = Task.objects.create(
      name=request.POST.get("name"),
      description=request.POST.get("description"),
      send_reminders=request.POST.get("send_reminders") == "on",
      reminder_info=request.POST.get("reminder_info"),
    )
    return redirect(reverse("view_task", args=[task.id]))
  return render(request, 'tasks/task_new.html', {
    "random": {
      "name": get_random("task_name"),
      "description": get_random("task_description"),
      "reminder_info": get_random("reminder_info"),
    }
  })

@login_required
@permission_required('tasks.view_timeslot')
def view_timeslots(request): return render(request, 'tasks/timeslots/timeslot_list.html', { "timeslots": Timeslot.objects.all() })

@login_required
@permission_required('tasks.view_timeslot')
def view_timeslot(request, timeslot_id): return render(request, 'tasks/timeslots/timeslot_view.html', { "timeslot": Timeslot.objects.get(id=timeslot_id) })

@login_required
@permission_required('tasks.add_assignedtimeslot')
def assign_timeslot(request, timeslot_id):
  timeslot = Timeslot.objects.get(id=timeslot_id)
  profiles_and_actions = [(
    profile,
    AssignedTimeslot.objects.filter(profile=profile, timeslot__task=timeslot.task).order_by("no_show", "-timeslot__start_time").first(),
    "exists_here" if AssignedTimeslot.objects.filter(profile=profile, timeslot=timeslot).exists() else
    "exists_elsewhere" if AssignedTimeslot.objects.filter(profile=profile, timeslot__task=timeslot.task, no_show=False).exclude(timeslot=timeslot).exists() else
    "exists_elsewhere_no_show" if AssignedTimeslot.objects.filter(profile=profile, timeslot__task=timeslot.task).exists() else
    "not_assigned",
  ) for profile in Profile.objects.all()]
  return render(request, 'tasks/timeslots/timeslot_assign.html', { "timeslot": timeslot, "profiles_and_actions": profiles_and_actions })

@login_required
@permission_required('tasks.add_timeslotcheckin')
def checkin_timeslot(request, timeslot_id): return render(request, 'tasks/timeslots/timeslot_checkin.html', { "timeslot": Timeslot.objects.get(id=timeslot_id) })

@login_required
@permission_required('tasks.add_timeslotcheckin')
@require_POST
def scan_rfid(request, timeslot_id, rfid):
  timeslot = Timeslot.objects.get(id=timeslot_id)
  tgbt = TGBT()
  try:
    profile = Profile.objects.get(wannabe_id=tgbt.get_wannabe_id_from_nfc_tag(rfid))

    if TimeslotCheckIn.objects.filter(profile=profile, timeslot=timeslot).exists():
      return JsonResponse({ "success": True, "status": "already_checked_in", "profile": profile.__str__() })

    assigned_this = AssignedTimeslot.objects.filter(profile=profile, timeslot=timeslot)
    if not assigned_this.exists():
      assigned_other = AssignedTimeslot.objects.filter(profile=profile, timeslot__task=timeslot.task, no_show=False).exclude(timeslot=timeslot)
      assigned_other_exists = assigned_other.exists()
      force = request.POST.get("force", "false") == "true"
      if assigned_other_exists or force:
        if force:
          if assigned_other_exists: assigned_other.delete()
          AssignedTimeslot.objects.create(profile=profile, timeslot=timeslot)
          TimeslotCheckIn.objects.create(profile=profile, timeslot=timeslot, extra=True)
          if timeslot.task.send_reminders: send_message_to_user(profile.user, f"✅ Du har blitt flyttet til `{timeslot}` og oppmøte er registrert. Takk for innsatsen!")
          return JsonResponse({ "success": True, "status": "moved" if assigned_other_exists else "created", "profile": profile.__str__(), "crew": profile.crew_name })
        return JsonResponse({ "success": False, "status": "assigned_other", "profile": profile.__str__(), "assigned_timeslot": assigned_other.first().timeslot.__str__() })
      return JsonResponse({ "success": False, "status": "not_assigned", "profile": profile.__str__() })
    TimeslotCheckIn.objects.create(profile=profile, timeslot=timeslot)
    if timeslot.task.send_reminders: send_message_to_user(profile.user, f"✅ Ditt oppmøte for oppgaven `{timeslot}` er registrert. Takk for innsatsen!")
    return JsonResponse({ "success": True, "status": "success", "profile": profile.__str__(), "crew": profile.crew_name })
  except Profile.DoesNotExist:
    return JsonResponse({ "success": False, "status": "profile_not_found" })
  except:
    return JsonResponse({ "success": False, "status": "error" })

@login_required
@permission_required('tasks.change_assignedtimeslot')
@require_POST
def mark_noshows(request, timeslot_id):
  timeslot = Timeslot.objects.get(id=timeslot_id)
  assigned = AssignedTimeslot.objects.filter(timeslot=timeslot, no_show=False)
  for assignment in assigned:
    if not TimeslotCheckIn.objects.filter(profile=assignment.profile, timeslot=timeslot).exists():
      assignment.no_show = True
      assignment.save()
      if timeslot.task.send_reminders: send_message_to_user(assignment.profile.user, f"❗ Du er fjernet fra oppgaven `{timeslot}` grunnet manglende oppmøte. Spør din chief hvis du lurer på noe.")
  return JsonResponse({ "success": True })

@login_required
@permission_required('tasks.change_timeslot')
def edit_timeslot(request, timeslot_id):
  timeslot = Timeslot.objects.get(id=timeslot_id)
  if request.POST:
    fields = {
      "max_participants": request.POST.get("max_participants"),
      "start_time": request.POST.get("start_time"),
      "end_time": request.POST.get("end_time"),
    }
    for key, value in fields.items():
      if value != getattr(timeslot, key):
        setattr(timeslot, key, value)
    timeslot.save()
    return redirect(reverse("view_timeslot", args=[timeslot_id]))
  return render(request, 'tasks/timeslots/timeslot_edit.html', { "timeslot": timeslot })

@login_required
@permission_required('tasks.delete_timeslot')
def delete_timeslot(request, timeslot_id):
  Timeslot.objects.get(id=timeslot_id).delete()
  return redirect(reverse("view_timeslots"))

@login_required
@permission_required('tasks.view_timeslot')
def raw_crewlist(request, timeslot_id): return render(request, 'tasks/timeslots/components/crewlist.html', { "timeslot": Timeslot.objects.get(id=timeslot_id), "raw": True })

@login_required
@permission_required('tasks.add_assignedtimeslot')
@require_POST
def add_user_to_timeslot(request, timeslot_id, profile_id):
  timeslot = Timeslot.objects.get(id=timeslot_id)
  profile = Profile.objects.get(id=profile_id)
  reassign = request.POST.get("reassign", "false") == "true"
  if reassign:
    assigned_timeslot = AssignedTimeslot.objects.filter(profile=profile, timeslot__task=timeslot.task, no_show=False).first()
    if assigned_timeslot:
      assigned_timeslot.timeslot = timeslot
      assigned_timeslot.save()
      if timeslot.task.send_reminders: send_message_to_user(profile.user, f"✅ Din oppgave har blitt endret til `{timeslot}`. Spør din chief hvis du lurer på noe.")
      return JsonResponse({ "success": True, "status": "reassigned" })
  AssignedTimeslot.objects.get_or_create(profile=profile, timeslot=timeslot)
  if timeslot.task.send_reminders: send_message_to_user(profile.user, f"✅ Du har blitt tildelt oppgaven `{timeslot}`. Du vil få en påminnelse to timer før oppdatt tidspunkt. Spør din chief hvis du lurer på noe.")
  return JsonResponse({ "success": True })

@login_required
@permission_required('tasks.add_timeslotcheckin')
@require_POST
def check_in_user_to_timeslot(request, timeslot_id, profile_id):
  timeslot = Timeslot.objects.get(id=timeslot_id)
  profile = Profile.objects.get(id=profile_id)
  remove = request.POST.get("remove", "false") == "true"
  if remove:
    TimeslotCheckIn.objects.filter(profile=profile, timeslot=timeslot).delete()
    return JsonResponse({ "success": True, "status": "removed" })
  if not AssignedTimeslot.objects.filter(profile=profile, timeslot=timeslot).exists():
    return JsonResponse({ "success": False, "status": "not_assigned" })
  TimeslotCheckIn.objects.get_or_create(profile=profile, timeslot=timeslot)
  return JsonResponse({ "success": True })

@login_required
@permission_required('tasks.delete_assignedtimeslot')
@require_POST
def remove_user_from_timeslot(request, timeslot_id, profile_id):
  timeslot = Timeslot.objects.get(id=timeslot_id)
  profile = Profile.objects.get(id=profile_id)
  AssignedTimeslot.objects.filter(profile=profile, timeslot=timeslot).delete()
  TimeslotCheckIn.objects.filter(profile=profile, timeslot=timeslot).delete()
  if timeslot.task.send_reminders: send_message_to_user(profile.user, f"❕ Du er fjernet fra oppgaven `{timeslot}`. Spør din chief hvis du lurer på noe.")
  return JsonResponse({ "success": True })

@login_required
@permission_required('tasks.add_timeslot')
def new_timeslot(request, task_id):
  task = Task.objects.get(id=task_id)
  if request.POST:
    timeslot = Timeslot.objects.create(
      task=task,
      max_participants=request.POST.get("max_participants"),
      start_time=request.POST.get("start_time"),
      end_time=request.POST.get("end_time")
    )
    return redirect(reverse("view_timeslot", args=[timeslot.id]))
  return render(request, 'tasks/timeslots/timeslot_new.html', { "task": task })
