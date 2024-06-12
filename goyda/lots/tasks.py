from celery import Celery
from django.db import transaction
from trading.models import TradeLog
from bids.models import Bid

app = Celery()

@app.task
def lot_lifetime(trade_id):
    trade = TradeLog.objects.get(id=trade_id)
    seller = trade.lot.seller
    try:
        bid = Bid.objects.filter(trade_id=trade.id).first()
        buyer = bid.user
    except Bid.DoesNotExist:
        bid = None
        buyer = None
    with transaction.atomic():
        if bid is not None:
            seller.balance += bid.bid
        trade.status = 0
        trade.buyer = buyer
        trade.save()
        seller.save()