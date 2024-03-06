from django.urls import path
from lots.views import lots

app_name = 'lots'

urlpatterns = [
    path('test/', lots, name='test')
]