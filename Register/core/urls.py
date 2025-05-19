from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('api/', include('api.urls')),                  # API marshrutlari
    path('admin/', admin.site.urls),                    # Django admin
    path('', include('queueing.urls')),                 # Root URL: navbat
    path('staff/', include('members.urls')),            # Hodimlar uchun login/register
    path('registrator/', include('registrator.urls')),  # Registrator bo‘limi
]

# # Faqat DEBUG holatda browser reload yo‘llarini qo‘shish
# if settings.DEBUG:
#     urlpatterns += [
#         path("__reload__/", include("django_browser_reload.urls")),
#     ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)