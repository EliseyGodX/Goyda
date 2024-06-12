from bids.views import BidView
from django.urls import path

app_name = 'bids'

urlpatterns = [
    path('<slug:lot_id>/', BidView.as_view(), name='bid'),
]

