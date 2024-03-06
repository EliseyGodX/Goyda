from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from lots.views import general

urlpatterns = [
    path('', general, name='general'),
    path('admin/', admin.site.urls),
    path('lots/', include('lots.urls', namespace='lots')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)