from django.urls import path
from lots.views import NewLotView

app_name = 'lots'

urlpatterns = [
    path('new-lot/', NewLotView.as_view(), name='new_lot'),
]