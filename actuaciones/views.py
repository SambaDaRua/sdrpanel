# coding=utf8
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from datetime import datetime
from actuaciones.models import actuaciones, samberos, contactos, instrumentos, relaciones
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
import csv

@login_required
def index(request):
    if ((request.POST.has_key('user')) and (request.user.is_staff) and samberos.objects.get(id=request.POST.get('user'))):
        user_id = request.POST.get('user')
    else:
        user_id = request.user.id
    if ((request.POST.has_key('instrumento')) and (request.POST.has_key('id_actuacion'))):
        actualiza_instrumento_actuacion(request.POST.get('id_actuacion'), user_id, request.POST.get('instrumento'))
    if (request.POST.has_key('coche')):
        actualiza_coche_actuacion(request.POST.get('id_actuacion'), user_id)
    lista_proximas_actuaciones = actuaciones.objects.filter(fecha__gt=datetime.now()).order_by('fecha')
    lista_instrumentos = instrumentos.objects.all().order_by('id')
    lista_samberos = samberos.objects.filter(is_active=True).order_by('username')
    t = loader.get_template('actuaciones.html')
    c = Context({
        'lista_proximas_actuaciones': lista_proximas_actuaciones,
        'lista_instrumentos': lista_instrumentos,
        'lista_samberos': lista_samberos,
        'usuario': samberos.objects.get(id = request.user.id),
    })
    return HttpResponse(t.render(c))

@login_required
def listado_contactos(request):
    lista_contactos = contactos.objects.all()
    t = loader.get_template('contactos.html')
    c = Context({
        'lista_contactos': lista_contactos,
        'usuario': samberos.objects.get(id = request.user.id),
    })
    return HttpResponse(t.render(c))

@login_required
def listado_samberos(request):
    lista_samberos = samberos.objects.filter(is_active=True,backstage=False)
    lista_samberos_backstage = samberos.objects.filter(is_active=True,backstage=True)
    lista_samberos_antiguos = samberos.objects.filter(is_active=False)
    t = loader.get_template('samberos.html')
    c = Context({
        'lista_samberos': lista_samberos,
        'lista_samberos_backstage': lista_samberos_backstage,
        'lista_samberos_antiguos': lista_samberos_antiguos,
        'usuario': samberos.objects.get(id = request.user.id),
    })
    return HttpResponse(t.render(c))

@login_required
def datos_sambero(request, username):
    sambero = samberos.objects.get(username = username)
    t = loader.get_template('datos_sambero.html')
    c = Context({
        'sambero': sambero,
    })
    return HttpResponse(t.render(c))

@login_required
def datos_contacto(request, id):
    contacto = contactos.objects.get(id = id)
    t = loader.get_template('datos_contacto.html')
    c = Context({
        'contacto': contacto,
    })
    return HttpResponse(t.render(c))

def actualiza_instrumento_actuacion(id_actuacion, id_sambero, id_instrumento):
    actu = actuaciones.objects.get(id = id_actuacion)
    if (actuaciones.objects.filter(id = id_actuacion).filter(samberos__sambero__id = id_sambero)):
        relac = actu.samberos.get(sambero__id = id_sambero)
        actu.samberos.remove(relac)
    if (id_instrumento > 0):
        actu.samberos.add(crear_relacion(id_sambero,id_instrumento))
        actu.save()

def crear_relacion(id_sambero, id_instrumento):
    if (relaciones.objects.filter(sambero__id = id_sambero).filter(instrumento__id = id_instrumento)):
        relacion = relaciones.objects.get(sambero__id = id_sambero, instrumento__id = id_instrumento)
    else:
        inst = instrumentos.objects.get(id = id_instrumento)
        samb = samberos.objects.get(id = id_sambero)
        relacion = relaciones(sambero = samb, instrumento = inst)
        relacion.save()
    return relacion.id

def actualiza_coche_actuacion(id_actuacion, id_sambero):
    actu = actuaciones.objects.get(id = id_actuacion)
    samb = samberos.objects.get(id = id_sambero)
    if (actuaciones.objects.filter(id = id_actuacion).filter(coches__id=id_sambero)):
        actu.coches.remove(samb)
    else:
        actu.coches.add(samb)

@login_required
def samberos_csv(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=samberos.csv'
    lista_samberos = samberos.objects.filter(is_active=True,backstage=False)
    lista_samberos_backstage = samberos.objects.filter(is_active=True,backstage=True)
    lista_samberos_antiguos = samberos.objects.filter(is_active=False)
    t = loader.get_template('samberos-csv.html')
    c = Context({
        'lista_samberos': lista_samberos,
        'lista_samberos_backstage': lista_samberos_backstage,
        'lista_samberos_antiguos': lista_samberos_antiguos,
        'usuario': samberos.objects.get(id = request.user.id),
    })
    response.write(t.render(c))
    return response

@login_required
def cambio_datos(request):
    error = ""
    sambero = samberos.objects.get(id = request.user.id)
    if request.POST:
        if (request.POST.has_key('username') and request.POST.get('username') != sambero.username):
            error=u'El nombre de usuario no se puede cambiar'
        if (request.POST.has_key('first_name') and request.POST.get('first_name') != ""):
            sambero.first_name=request.POST.get('first_name')
            sambero.save()
        if (request.POST.has_key('last_name') and request.POST.get('last_name') != ""):
            sambero.last_name=request.POST.get('last_name')
            sambero.save()
        if (request.POST.has_key('dni') and request.POST.get('dni')):
            sambero.dni=request.POST.get('dni')
            sambero.save()
        if (request.POST.has_key('phone') and request.POST.has_key('phone')):
            sambero.phone=request.POST.get('phone')
            sambero.save()
        if request.POST.has_key('movil') and request.POST.has_key('movil'):
            sambero.movil=request.POST.get('movil')
            sambero.save()
        if (request.POST.has_key('email') and request.POST.get('email') != ""):
            sambero.email=request.POST.get('email')
            sambero.save()
        if request.POST.has_key('instrumento'):
            inst_id = 0
            inst_id = request.POST.get('instrumento')
            if inst_id:
                instru = instrumentos.objects.get(id = inst_id)
                sambero.instrumento = instru
                sambero.save()
        if (request.POST.has_key('old_password') and request.POST.get('old_password') != ""):
            old_pwd = request.POST.get('old_password', None).decode('ascii')
            if sambero.check_password(old_pwd):
                if (request.POST.has_key('new_password') and request.POST.has_key('new_password2') and request.POST.get('new_password', None) == request.POST.get('new_password2', None)):
                    passwd = request.POST.get('new_password', None).decode('ascii')
                    if (passwd != ""):
                        sambero.set_password(passwd)
                        sambero.save()
                    else:
                        error = u'La nueva contraseña no puede estar en blanco'
                else:
                    error = u'La nueva contraseña tiene que ser igual en los dos campos'
            else:
                error = u'La contraseña es incorrenta'
    lista_instrumentos = instrumentos.objects.all().order_by('id')
    t = loader.get_template('cambio_datos.html')
    c = Context({
        'usuario': samberos.objects.get(id = request.user.id),
        'lista_instrumentos': lista_instrumentos,
        'error': error,
    })
    return HttpResponse(t.render(c))

