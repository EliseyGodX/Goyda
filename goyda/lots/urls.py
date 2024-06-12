from django.urls import path
from lots.views import AddLotView, LotInspectView

app_name = 'lots'

urlpatterns = [
    path('add/', AddLotView.as_view(), name='add'),
    path('inspect/<slug:lot_id>/', LotInspectView.as_view(), name='inspect')
]