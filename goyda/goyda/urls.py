from django.contrib import admin
from django.urls import path, include
from core.views import General
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', General.as_view(), name='general'),
    path('lots/', include('lots.urls', namespace='lots')),
    path('users/', include('users.urls', namespace='users')),
    path('category/', include('category.urls', namespace='category'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)