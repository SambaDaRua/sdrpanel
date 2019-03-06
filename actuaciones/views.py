# coding=utf8
# Create your views here.
from django.template import loader
from django.http import HttpResponse
from datetime import datetime
from actuaciones.models import actuaciones, samberos, contactos, instrumentos, relaciones
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

CHECKBOX_MAPPING = {'True':True,
                    'False':False,}


@login_required
def index(request):
    if (('user' in request.POST) and (request.user.is_staff) and samberos.objects.get(id=request.POST.get('user'))):
        user_id = request.POST.get('user')
    else:
        user_id = request.user.id
    if (('instrumento' in request.POST) and ('id_actuacion' in request.POST)):
        actualiza_instrumento_actuacion(int(request.POST.get('id_actuacion')), user_id, int(request.POST.get('instrumento')))
    if ('coche' in request.POST):
        actualiza_coche_actuacion(request.POST.get('id_actuacion'), user_id)
    lista_proximas_actuaciones = actuaciones.objects.filter(fecha__gt=datetime.now()).order_by('fecha')
    lista_instrumentos = instrumentos.objects.all().order_by('id')
    lista_samberos = samberos.objects.filter(is_active=True).order_by('username')
    c = {
        'lista_proximas_actuaciones': lista_proximas_actuaciones,
        'lista_instrumentos': lista_instrumentos,
        'lista_samberos': lista_samberos,
        'usuario': samberos.objects.get(id=request.user.id),
    }
    return render(request, 'actuaciones.html', c)


@login_required
def listado_contactos(request):
    lista_contactos = contactos.objects.all()
    c = {
        'lista_contactos': lista_contactos,
        'usuario': samberos.objects.get(id=request.user.id),
    }
    return render(request, 'contactos.html', c)


@login_required
def listado_samberos(request):
    lista_samberos = samberos.objects.filter(is_active=True,backstage=False)
    lista_samberos_backstage = samberos.objects.filter(is_active=True,backstage=True)
    lista_samberos_antiguos = samberos.objects.filter(is_active=False)
    c = {
        'lista_samberos': lista_samberos,
        'lista_samberos_backstage': lista_samberos_backstage,
        'lista_samberos_antiguos': lista_samberos_antiguos,
        'usuario': samberos.objects.get(id=request.user.id),
    }
    return render(request, 'samberos.html', c)


@login_required
def datos_sambero(request, username):
    sambero = samberos.objects.get(username=username)
    c = {
        'sambero': sambero,
    }
    return render(request, 'datos_sambero.html', c)


@login_required
def datos_contacto(request, id):
    contacto = contactos.objects.get(id=id)
    c = {
        'contacto': contacto,
    }
    return render(request, 'datos_contacto.html', c)


def actualiza_instrumento_actuacion(id_actuacion, id_sambero, id_instrumento):
    actu = actuaciones.objects.get(id=id_actuacion)
    if (actuaciones.objects.filter(id=id_actuacion).filter(samberos__sambero__id=id_sambero)):
        relac = actu.samberos.get(sambero__id=id_sambero)
        actu.samberos.remove(relac)
    if (id_instrumento > 0):
        actu.samberos.add(crear_relacion(id_sambero,id_instrumento))
        actu.save()


def crear_relacion(id_sambero, id_instrumento):
    if (relaciones.objects.filter(sambero__id=id_sambero).filter(instrumento__id=id_instrumento)):
        relacion = relaciones.objects.get(sambero__id=id_sambero, instrumento__id=id_instrumento)
    else:
        inst = instrumentos.objects.get(id=id_instrumento)
        samb = samberos.objects.get(id=id_sambero)
        relacion = relaciones(sambero=samb, instrumento=inst)
        relacion.save()
    return relacion.id


def actualiza_coche_actuacion(id_actuacion, id_sambero):
    actu = actuaciones.objects.get(id=id_actuacion)
    samb = samberos.objects.get(id=id_sambero)
    if (actuaciones.objects.filter(id=id_actuacion).filter(coches__id=id_sambero)):
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
    c = {
        'lista_samberos': lista_samberos,
        'lista_samberos_backstage': lista_samberos_backstage,
        'lista_samberos_antiguos': lista_samberos_antiguos,
        'usuario': samberos.objects.get(id=request.user.id),
    }
    response.write(t.render(c))
    return response


@login_required
def cambio_datos(request):
    error = ""
    sambero = samberos.objects.get(id=request.user.id)
    if request.POST:
        if ('username' in request.POST and request.POST.get('username') != sambero.username):
            error='El nombre de usuario no se puede cambiar'
        if ('first_name' in request.POST and request.POST.get('first_name') != ""):
            sambero.first_name=request.POST.get('first_name')
            sambero.save()
        if ('last_name' in request.POST and request.POST.get('last_name') != ""):
            sambero.last_name=request.POST.get('last_name')
            sambero.save()
        if 'dni' in request.POST:
            sambero.dni=request.POST.get('dni','')
            sambero.save()
        if 'phone' in request.POST:
            sambero.phone=request.POST.get('phone','')
            sambero.save()
        if 'movil' in request.POST:
            sambero.movil=request.POST.get('movil','')
            sambero.save()
        if ('email' in request.POST and request.POST.get('email') != ""):
            sambero.email=request.POST.get('email')
            sambero.save()
        if ('notification_email' in request.POST and request.POST.get('notification_email') != ""):
            sambero.notification_email=CHECKBOX_MAPPING.get(request.POST.get('notification_email'))
        else:
            sambero.notification_email=False
        sambero.save()
        print(sambero.notification_email)
        if 'instrumento' in request.POST:
            inst_id = 0
            inst_id = request.POST.get('instrumento')
            if inst_id:
                instru = instrumentos.objects.get(id=inst_id)
                sambero.instrumento = instru
                sambero.save()
        if ('old_password' in request.POST and request.POST.get('old_password') != ""):
            old_pwd = request.POST.get('old_password', None).decode('ascii')
            if sambero.check_password(old_pwd):
                if ('new_password' in request.POST and 'new_password2' in request.POST and request.POST.get('new_password', None) == request.POST.get('new_password2', None)):
                    passwd = request.POST.get('new_password', None).decode('ascii')
                    if (passwd != ""):
                        sambero.set_password(passwd)
                        sambero.save()
                    else:
                        error = 'La nueva contraseña no puede estar en blanco'
                else:
                    error = 'La nueva contraseña tiene que ser igual en los dos campos'
            else:
                error = 'La contraseña es incorrenta'
    lista_instrumentos = instrumentos.objects.all().order_by('id')
    c = {
        'usuario': samberos.objects.get(id=request.user.id),
        'lista_instrumentos': lista_instrumentos,
        'error': error,
    }
    return render(request, 'cambio_datos.html', c)
