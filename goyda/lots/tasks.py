from celery import Celery
from trading.models import TradeLog


app = Celery()

@app.task
def lot_lifetime(trade_id):
    TradeLog.objects.filter(id=trade_id).update(status=0)