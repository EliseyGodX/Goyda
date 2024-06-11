from django.urls import path
from lots.views import AddLotView, LotInspectView, LotBidView

app_name = 'lots'

urlpatterns = [
    path('new-lot/', AddLotView.as_view(), name='add'),
    path('lot-inspect/<slug:lot_id>/', LotInspectView.as_view(), name='inspect'),
    path('bid/<slug:lot_id>/', LotBidView.as_view(), name='bid')
]