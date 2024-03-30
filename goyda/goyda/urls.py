from django.contrib import admin
from django.urls import path, include
from core.views import general
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', general, name='general'),
    path('lots/', include('lots.urls', namespace='lots')),
    path('users/', include('users.urls', namespace='users')),
    path('category/', include('category.urls', namespace='category'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)