from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Flores', FloresViewSet)

urlpatterns = [
    path('',home,name='home'),
    path('galeria/',galeria,name='galeria'),
    path('formulario/',formulario,name='formu'),
    path('contactenos/',contactenos,name='contactenos'),
    path('sobreNosotros/',sobreNosotros,name='sobreNosotros'),
    path('login/',login,name='login'),
    path('login_iniciar/',login_iniciar,name='login_iniciar'),
    path('cerrar_session/',cerrar_session,name='cerrar_session'),
    path('eliminar_flores/<id>/',eliminar_flores,name='eliminar_flores'),
    path('agregar_carro/<id>/',carro_compras,name='agregar_carro'),
    path('carro/',carros,name='carro'),
    path('carro_mas/<id>/',carro_compras_mas,name='carro_mas'),
    path('carro_menos/<id>/',carro_compras_menos,name='carro_menos'),
    path('grabar_carro/',grabar_carro,name='grabar_carro'),
    path('api/',include(router.urls)),
    path('',include('pwa.urls')),
    path('guardar-token/',guardar_token, name='guardar_token'),
]