from django.urls import path
from lots.views import NewLotView, LotInspectView

app_name = 'lots'

urlpatterns = [
    path('new-lot/', NewLotView.as_view(), name='new_lot'),
    path('lot-inspect/<slug:lot_id>/', LotInspectView.as_view(), name='inspect_lot')
]