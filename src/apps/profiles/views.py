from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from .models import *
from .utils.wannabe_sync import sync

@login_required
@user_passes_test(lambda u: u.is_superuser)
def wannabe_sync(request): return render(request, 'profiles/wannabe_sync.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def wannabe_sync_start(request): return JsonResponse(sync())
