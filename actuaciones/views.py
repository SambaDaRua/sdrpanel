# Create your views here.
from django.template import loader
from django.http import HttpResponse
from datetime import datetime
from actuaciones.models import actuaciones, samberos, contactos, instrumentos, relaciones
from actuaciones.forms import samberoForm, RemoveDisableAccountForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

CHECKBOX_MAPPING = {'True': True,
                    'False': False, }


@login_required
def index(request):
    if (('user' in request.POST) and (request.user.is_staff) and samberos.objects.get(id=request.POST.get('user'))):
        user_id = request.POST.get('user')
    else:
        user_id = request.user.id
    if (('instrumento' in request.POST) and ('id_actuacion' in request.POST)):
        actualiza_instrumento_actuacion(
            int(request.POST.get('id_actuacion')),
            user_id,
            int(request.POST.get('instrumento'))
        )
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
        'domain': request.get_host(),
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
    lista_samberos = samberos.objects.filter(is_active=True, backstage=False)
    lista_samberos_backstage = samberos.objects.filter(is_active=True, backstage=True)
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
        actu.samberos.add(crear_relacion(id_sambero, id_instrumento))
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
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=samberos.csv'
    lista_samberos = samberos.objects.filter(is_active=True, backstage=False)
    lista_samberos_backstage = samberos.objects.filter(is_active=True, backstage=True)
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
    # error = ""
    sambero = request.user
    if sambero:
        form = samberoForm(instance=sambero)

    if request.POST:
        form = samberoForm(request.POST, request=request, instance=sambero)
        if form.has_changed() and form.is_valid():
            if 'oldpassword' in form.changed_data and 'newpassword1' in form.changed_data:
                form.instance.set_password(form.cleaned_data['newpassword1'])
            form.save()
    c = {
        'usuario': request.user,
        'sambero_form': form,
    }
    return render(request, 'cambio_datos.html', c)


@login_required
def account_remove_delete(request):
    sambero = request.user
    if sambero:
        form = RemoveDisableAccountForm()
    if request.POST:
        form = RemoveDisableAccountForm(request.POST)
        if form.is_valid():
            if 'remove_account' in form.cleaned_data and form.cleaned_data['remove_account'] is True:
                sambero.delete()
                return redirect('logout')
            elif 'disable_account' in form.cleaned_data and form.cleaned_data['disable_account'] is True:
                sambero.is_active = False
                sambero.save()
                return redirect('logout')
    c = {
        'usuario': request.user,
        'borrar_cuenta_form': form,
    }
    return render(request, 'borrar_cuenta.html', c)
