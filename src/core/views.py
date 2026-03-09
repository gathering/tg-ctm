from django.shortcuts import render, redirect
from django.conf import settings
import os, json
from django.http import JsonResponse
from django.urls import reverse
from apps.tasks.models import AssignedTimeslot

def index(request):
  if not request.user.is_authenticated:
    if settings.SOCIAL_AUTH_KEYCLOAK_KEY is None: return redirect(reverse("login"))
    else: return redirect(reverse("social:begin", args=["keycloak"]))
  chief_memberships = request.user.profile.crew_memberships.filter(is_chief=True)
  return render(request, "index.html", { "chief_memberships": [(membership, AssignedTimeslot.objects.filter(profile__crew_memberships__crew=membership.crew).order_by("timeslot__start_time", "profile__user__first_name", "profile__user__last_name")) for membership in chief_memberships]})

def handler400(request, exception):
  print("Exception with status 400", exception)
  return render(request, 'errors/400.html', status=400)

def handler403(request, exception):
  print("Exception with status 403", exception)
  return render(request, 'errors/403.html', status=403)

def handler404(request, exception):
  print("Exception with status 404", exception)
  return render(request, 'errors/404.html', status=404)

def handler500(request):
  return render(request, 'errors/500.html', status=500)

def pwa_service_worker(request):
  with open(os.path.join(settings.BASE_DIR, settings.STATIC_ROOT, "staticfiles.json")) as static_files_raw:
    static_files = json.load(static_files_raw)
    files = [file for file in list(static_files["paths"].values())]
    return render(request, 'pwa/serviceworker.js', { "files": files, "hash": static_files["hash"] }, content_type='application/javascript')

def pwa_manifest(request):
  shortcuts = [{ "name": "Hjem", "url": reverse("index") }]

  return JsonResponse({
    "name": settings.PWA_APP_NAME,
    "short_name": settings.PWA_APP_NAME,
    "description": settings.PWA_APP_DESCRIPTION,
    "start_url": settings.PWA_APP_START_URL,
    "display": settings.PWA_APP_DISPLAY,
    "scope": settings.PWA_APP_SCOPE,
    "orientation": settings.PWA_APP_ORIENTATION,
    "background_color": settings.PWA_APP_BACKGROUND_COLOR,
    "theme_color": settings.PWA_APP_THEME_COLOR,
    "status_bar": settings.PWA_APP_STATUS_BAR_COLOR,
    "icons": settings.PWA_APP_ICONS,
    "dir": settings.PWA_APP_DIR,
    "lang": settings.PWA_APP_LANG,
    "screenshots" : settings.PWA_APP_SCREENSHOTS,
    "shortcuts" : shortcuts,
  })

def pwa_offline(request): return render(request, "pwa/offline.html")
