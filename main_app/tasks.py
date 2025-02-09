from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import reservationClass

@shared_task
def check_expired_reservations():
    now = timezone.now()
    expired_reservations = reservationClass.objects.filter(status='cart', expires_at__lt=now)

    for reservation in expired_reservations:
        reservation.status = 'expired'
        reservation.appointment.schedule.is_available = True       
        reservation.appointment.schedule.save()
        reservation.save()
