from core.views import GeneralView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django_select2 import urls as select2_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GeneralView.as_view(), name='general'),
    path('lots/', include('lots.urls', namespace='lots')),
    path('users/', include('users.urls', namespace='users')),
    path('categories/', include('categories.urls', namespace='categories')),
    path('select2/', include(select2_urls))
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns