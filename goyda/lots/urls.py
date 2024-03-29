from django.urls import path
from lots.views import general
from django.conf.urls.static import static
from django.conf import settings

app_name = 'lots'

urlpatterns = [
    path('', general, name='pass'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)