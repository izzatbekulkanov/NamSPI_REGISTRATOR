from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),  # MUHIM
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('queueing.urls')),  # bu default root URL bo‘ladi
    path('staff/', include('members.urls')),  # bu default root URL bo‘ladi
    path('registrator/', include('registrator.urls')),  # bu default root URL bo‘ladi
]
