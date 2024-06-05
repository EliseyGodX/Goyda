from celery import Celery
from trading.models import TradeLog


app = Celery('goyda', broker='amqp://myuser:mypassword@localhost:5672/myvhost')

@app.task
def lot_lifetime(trade_id):
    TradeLog.objects.filter(id=trade_id).update(status=0)