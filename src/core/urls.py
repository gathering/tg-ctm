"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
  path('accounts/', include('django.contrib.auth.urls'), name="accounts"),
  path('admin/', admin.site.urls, name="admin"),
  path('auth/', include('social_django.urls', namespace='social')),
  path('', views.index, name="index"),
  re_path(r"^serviceworker\.js$", views.pwa_service_worker, name="service_worker"),
  re_path(r"^manifest\.json$", views.pwa_manifest, name="manifest"),
  re_path(r"^offline/?$", views.pwa_offline, name="offline"),
  # todo: path('kitchen/', include('apps.kitchen.urls'), name="kitchen"),
  path('tasks/', include('apps.tasks.urls'), name="tasks"),
  path('profiles/', include('apps.profiles.urls'), name="profiles"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = "core.views.handler400"
handler403 = "core.views.handler403"
handler404 = "core.views.handler404"
handler500 = "core.views.handler500"
