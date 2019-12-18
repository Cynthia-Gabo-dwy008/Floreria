from django.shortcuts import render
from .models import Estado,Flores,Comprobante

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login as auth_login

from django.contrib.auth.decorators import login_required
import datetime
from .clases import elemento

#rest_framework 

from rest_framework import viewsets
from .serializers import FloresSerializer

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseBadRequest

from django.core import serializers
import json

from fcm_django.models import FCMDevice

@csrf_exempt
@require_http_methods(['POST'])
def guardar_token(request):
    body = request.body.decode('utf-8')
    bodyDict = json.loads(body)

    token = bodyDict['token']

    existe = FCMDevice.objects.filter(registration_id = token, active = True)

    if len(existe)>0:
        return HttpResponseBadRequest(json.dumps({'mensaje':'el token ya existe'}))
    
    dispositivo = FCMDevice()
    dispositivo.registration_id = token
    dispositivo.active = True 

    if request.user.is_authenticated:
        dispositivo.user = request.user

    try:
        dispositivo.save()
        return HttpResponse(json.dumps({'mensaje':'token guardado'}))
    except:
        return HttpResponseBadRequest(json.dumps({'mensaje':'no se ha podido guardar'}))


@login_required(login_url='/login/')
def home(request):
    return render(request,'core/home.html')
    
@login_required(login_url='/login/')
def contactenos(request):
    return render(request,'core/contactenos.html')

@login_required(login_url='/login/')
def sobreNosotros(request):
    return render(request,'core/sobreNosotros.html')

#--------------------- inicio de sesion ----------------------#

def login(request):
    if request.POST:
        usuario=request.POST.get("txtUser")
        password=request.POST.get("txtPass")
        us=authenticate(request,username=usuario,password=password)
        msg=''
        request.session["carrito"] = []        
        request.session["carritox"] = []        
        print('realizado')
        if us is not None and us.is_active:
            login_autent(request,us)          
            return render(request,'core/home.html')
        else:
            return render(request,'core/login.html')

    return render(request,'core/login.html')

def login_iniciar(request):
    if request.POST:
        usuario=request.POST.get("txtUser")
        password=request.POST.get("txtPass")
        us=authenticate(request,username=usuario,password=password)
        msg=''
        request.session["carritox"]=[]
        print("cargado")
        if us is not None and us.is_active:
            auth_login(request,us)
            return render(request,'core/home.html')
        else:
            return render(request,'core/login.html')


def cerrar_session(request):
    logout(request)
    return render(request,'core/login.html')

#---------------------------- carros -------------------------------------#


@login_required(login_url='/login/')
def carros(request):
    x=request.session["carritox"]
    suma=0
    for item in x:
        suma=suma+int(item["total"])           
    return render(request,'core/carro.html',{'x':x,'total':suma})

@login_required(login_url='/login/')
def grabar_carro(request):
    x=request.session["carritox"]    
    usuario=request.user.username
    suma=0
    try:
        for item in x:        
            nombre=item["nombre"]
            valor=int(item["valor"])
            cantidad=int(item["cantidad"])
            total=int(item["total"])        
            comprobante=Comprobante(
                usuario=usuario,
                nombre=nombre,
                valor=valor,
                cantidad=cantidad,
                total=total,
                fecha=datetime.date.today()
            )
            comprobante.save()
            suma=suma+int(total)  
        mensaje="Grabado"
        request.session["carritox"] = []
    except:
        mensaje="error al grabar"            
    return render(request,'core/carro.html',{'x':x,'total':suma,'mensaje':mensaje})

@login_required(login_url='/login/')
def carro_compras(request,id):
    f=Flores.objects.get(name=id)
    x=request.session["carritox"]
    el=elemento(1,f.name,f.valor,1)
    sw=0
    suma=0
    clon=[]
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==f.name:
            sw=1
            cantidad=int(cantidad)+1
        ne=elemento(1,item["nombre"],item["valor"],cantidad)
        suma=suma+int(ne.total())
        clon.append(ne.toString())
    if sw==0:
        clon.append(el.toString())
    x=clon    
    request.session["carritox"]=x
    flores=Flores.objects.all()    
    return render(request,'core/galeria.html',{'listaflores':flores,'total':suma})

@login_required(login_url='/login/')
def carro_compras_mas(request,id):
    f=Flores.objects.get(name=id)
    x=request.session["carritox"]
    suma=0
    clon=[]
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==f.name:
            cantidad=int(cantidad)+1
        ne=elemento(1,item["nombre"],item["valor"],cantidad)
        suma=suma+int(ne.total())
        clon.append(ne.toString())
    x=clon    
    request.session["carritox"]=x
    x=request.session["carritox"]        
    return render(request,'core/carro.html',{'x':x,'total':suma})

@login_required(login_url='/login/')
def carro_compras_menos(request,id):
    f=Flores.objects.get(name=id)
    x=request.session["carritox"]
    clon=[]
    suma=0
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==f.name:
            cantidad=int(cantidad)-1
        ne=elemento(1,item["nombre"],item["valor"],cantidad)
        suma=suma+int(ne.total())
        clon.append(ne.toString())
    x=clon    
    request.session["carritox"]=x
    x=request.session["carritox"]    
    return render(request,'core/carro.html',{'x':x,'total':suma})


#--------------------- procesos de galería ----------------------#

@login_required(login_url='/login/')
def galeria(request):
    flores=Flores.objects.all()
    return render(request, 'core/galeria.html',{'listaflores':flores})


@login_required(login_url='/login/')
def eliminar_flores(request,id):
    flor=Flores.objects.get(name=id)
    mensaje=''
    try:
        flor.delete()
        mensaje='Elimino la flor'
    except:
        mensaje='No se logro completar el proceso'
    
    flores=Flores.objects.all()
    return render(request,'core/galeria.html',{'listaflores':flores,'msg':mensaje})


@login_required(login_url='/login/')
def formulario(request):
    esta=Estado.objects.all()
    if request.POST:
        nombre=request.POST.get("txtNombre")
        valor=request.POST.get("txtValor")
        descripcion=request.POST.get("txtDescripcion")
        estado=request.POST.get("cboEstado")
        stock=request.POST.get("txtStock")
        obj_estado=Estado.objects.get(name=estado)
        imagen=request.FILES.get("txtImagen")

        flores=Flores(
            name=nombre,
            valor=valor,
            descripcion=descripcion,
            estado=obj_estado,
            stock=stock,
            fotografia=imagen
        )
        flores.save()
        #obtener dispositivos
        dispositivo = FCMDevice.objects.filter(active=True)
        dispositivo.send_message(
            title="Pelicula agregada!!!", 
            body="Se ha agregado :" + formulario.cleaned_data['name'],
            icon="/static/core/img/logo.png"
        )
        return render(request,'core/productos.html',{'lista':esta,'msg':'grabo','sw':True})
    return render(request,'core/productos.html',{'lista':esta})

#------------------------------------------------------------------------------------#

def isset(variable):
	return variable in locals() or variable in globals()

#-------------------------------------------------------------------------------------#

class FloresViewSet(viewsets.ModelViewSet):
    queryset = Flores.objects.all()
    serializer_class = FloresSerializer
