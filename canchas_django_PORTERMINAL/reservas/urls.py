from django.urls import path
from .views import CrearReservaView, MisReservasView, AdminListaView
urlpatterns=[path('crear/',CrearReservaView.as_view(),name='crear_reserva'),path('mias/',MisReservasView.as_view(),name='mis_reservas'),path('admin-lista/',AdminListaView.as_view(),name='admin_reservas')]
