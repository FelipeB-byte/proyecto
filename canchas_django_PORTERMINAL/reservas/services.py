
from django.conf import settings
from .models import Reserva
def time_slots_for(date_str):
    slots=[]; oh=settings.OPEN_HOUR; ch=settings.CLOSE_HOUR; interval=settings.RESERVA_INTERVAL_MINUTES
    for h in range(oh,ch):
        slots.append(f"{h:02d}:00")
        if interval!=60:
            m=0
            while m+interval<60:
                m+=interval; slots.append(f"{h:02d}:{m:02d}")
    return slots
def reservas_por_dia(fecha):
    return Reserva.objects.select_related('cancha','user').filter(fecha=fecha).order_by('cancha_id','hora')
