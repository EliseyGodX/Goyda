from core.views import GeneralView, GeneralSearchView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django_select2 import urls as select2_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GeneralView.as_view(), name='general'),
    path('search/', GeneralSearchView.as_view(), name='search'),
    path('lots/', include('lots.urls', namespace='lots')),
    path('users/', include('users.urls', namespace='users')),
    path('categories/', include('categories.urls', namespace='categories')),
    path('bids/', include('bids.urls', namespace='bids')),
    path('select2/', include(select2_urls))
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns