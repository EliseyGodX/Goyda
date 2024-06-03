import os
from celery import Celery
from trading.models import TradeLog


app = Celery()
BROKER_URL = "redis://localhost:6379"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gimsap.settings')
app.conf.broker_url = BROKER_URL
CELERY_BROKER_URL = BROKER_URL

@app.task
def lot_lifetime(trade_id):
    TradeLog.objects.filter(id=trade_id).update(status=0)