from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from category.views import LotsByCategory

app_name = 'category'

urlpatterns = [
    path('<slug:category_slug>', LotsByCategory.as_view(), name='category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)