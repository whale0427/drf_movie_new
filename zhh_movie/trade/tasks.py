from datetime import timedelta
from django.utils import timezone

from celery import shared_task
from .models import Order

@shared_task
def order_expired(order_id):
    order=Order.objects.get(id=order_id)
    expired_time=order.created_at+timedelta(minutes=30)
    if timezone.now()>expired_time:
        order.pay_status="TRADE_CLOSED"
        order.save()
        print(f"order {order.id} 过期，订单状态：TRADE_CLOSED")
    else:
        print(f"order {order.id} 未过期，订单状态：PAYING")

@shared_task
def order_recurring_tasks():
    orders=Order.objects.filter(pay_status="PAYING")
    for order in orders:
        order_expired.delay(order.id)