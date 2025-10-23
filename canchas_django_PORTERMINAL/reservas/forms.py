
from django import forms
from django.conf import settings
from .models import Reserva, Cancha
from datetime import date
class ReservaForm(forms.ModelForm):
    fecha=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    hora=forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))
    cancha=forms.ModelChoiceField(queryset=Cancha.objects.all())
    class Meta: model=Reserva; fields=['fecha','hora','cancha']
    def clean(self):
        cleaned=super().clean(); h=cleaned.get('hora'); f=cleaned.get('fecha')
        if h and not (settings.OPEN_HOUR <= h.hour < settings.CLOSE_HOUR): raise forms.ValidationError('Hora fuera del rango permitido.')
        if f and f < date.today(): raise forms.ValidationError('La fecha no puede ser en el pasado.')
        return cleaned
