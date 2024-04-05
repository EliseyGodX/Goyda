from django.urls import path
from lots.views import purchases

app_name = 'lots'

urlpatterns = [
    path('', purchases, name='pass'),
]