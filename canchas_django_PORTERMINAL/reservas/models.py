
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
class Cancha(models.Model):
    nombre=models.CharField(max_length=100)
    def __str__(self): return self.nombre
class Reserva(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    cancha=models.ForeignKey(Cancha,on_delete=models.CASCADE)
    fecha=models.DateField(); hora=models.TimeField()
    estado=models.CharField(max_length=10,choices=(('confirmada','Confirmada'),('cancelada','Cancelada')),default='confirmada')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['cancha','fecha','hora','estado'],name='uq_cancha_fecha_hora_estado')]
        ordering=['fecha','hora']
    def clean(self):
        from django.conf import settings as s
        if not (s.OPEN_HOUR <= self.hora.hour < s.CLOSE_HOUR):
            raise ValidationError('Hora fuera del rango permitido.')