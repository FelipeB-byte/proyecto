
from datetime import date
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from .forms import ReservaForm
from .models import Reserva, Cancha
from .services import time_slots_for, reservas_por_dia
class HomeView(TemplateView):
    template_name='home.html'
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs)
        d=self.request.GET.get('date') or date.today().isoformat()
        ctx['date']=d; ctx['canchas']=Cancha.objects.all().order_by('id'); ctx['slots']=time_slots_for(d)
        mapa={}; 
        for r in reservas_por_dia(d): mapa.setdefault(r.cancha_id, {})[r.hora.strftime('%H:%M')]=r
        ctx['mapa']=mapa; return ctx
class CrearReservaView(LoginRequiredMixin, View):
    template_name='reservas/crear.html'
    def get(self, request):
        initial={'fecha': self.request.GET.get('date', date.today().isoformat())}
        return render(request,self.template_name,{'form':ReservaForm(initial=initial)})
    def post(self, request):
        form=ReservaForm(request.POST)
        if form.is_valid():
            cancha=form.cleaned_data['cancha']; fecha=form.cleaned_data['fecha']; hora=form.cleaned_data['hora']
            if Reserva.objects.filter(cancha=cancha,fecha=fecha,hora=hora,estado='confirmada').exists():
                messages.error(request,'Ese horario ya está reservado.')
            else:
                Reserva.objects.create(user=request.user, cancha=cancha, fecha=fecha, hora=hora, estado='confirmada')
                messages.success(request,'Reserva creada.'); return redirect('mis_reservas')
        return render(request,self.template_name,{'form':form})
class MisReservasView(LoginRequiredMixin, TemplateView):
    template_name='reservas/mis_reservas.html'
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs)
        ctx['items']=Reserva.objects.select_related('cancha').filter(user=self.request.user).order_by('-fecha','-hora'); return ctx
    def post(self, request):
        rid=request.POST.get('rid')
        if rid: Reserva.objects.filter(id=rid, user=request.user).update(estado='cancelada'); messages.success(request,'Reserva cancelada.')
        return redirect('mis_reservas')
def es_staff_o_admin(u): return u.is_staff or u.is_superuser
@method_decorator(user_passes_test(es_staff_o_admin), name='dispatch')
class AdminListaView(TemplateView):
    template_name='reservas/lista_admin.html'
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs)
        d=self.request.GET.get('date') or date.today().isoformat()
        ctx['date']=d; ctx['items']=Reserva.objects.select_related('user','cancha').filter(fecha=d).order_by('cancha_id','hora'); return ctx
    def post(self, request):
        rid=request.POST.get('rid')
        if rid: Reserva.objects.filter(id=rid).update(estado='cancelada'); messages.success(request,'Reserva cancelada por admin.')
        return redirect('admin_reservas')

