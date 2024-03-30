from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from lots.views import purchases

app_name = 'lots'

urlpatterns = [
    path('', purchases, name='pass'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)