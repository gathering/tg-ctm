from . import settings
from django.utils import timezone

def constants(request):
  return { "settings": settings, "now": timezone.now() }
