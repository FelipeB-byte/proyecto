import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','canchas.settings'); import django; django.setup()
from django.contrib.auth.models import User
from reservas.models import Cancha
if not User.objects.filter(username='admin').exists(): User.objects.create_superuser('admin','admin@site.com','Admin123!'); print('Admin: admin / Admin123!')
if Cancha.objects.count()==0:
  [Cancha.objects.create(nombre=f'Cancha {i}') for i in range(1,6)]
  print('Canchas 1..5 creadas')
print('OK')
