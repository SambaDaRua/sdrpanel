# coding=utf8
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from datetime import datetime
from actuaciones.models import actuaciones, samberos
from sms.models import sms,log
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse


@login_required
def index(request):
	if ('texto' in request.POST and request.POST.get('texto')) :
		mensaje = sms(texto=request.POST.get('texto'))
		mensaje.save()
		for sambero in samberos.objects.filter(is_active=True):
			mensaje.numeros.add(sambero)
		mensaje.save()
		mensaje.envia()
		mensaje.save()
	lista_sms = sms.objects.order_by('-fecha')[0:10]
	t = loader.get_template('sms.html')
	c = Context({
		'lista_sms': lista_sms,
		'usuario': samberos.objects.get(id = request.user.id),
	})
	return HttpResponse(t.render(c))

