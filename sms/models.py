from django.db import models
from actuaciones.models import samberos
from sms.voipbuster import send_sms
from xml.dom import minidom
import re
import threading

sem = threading.Semaphore(5)

# Create your models here.
class sms(models.Model):
	texto = models.TextField()
	numeros = models.ManyToManyField(samberos)
	fecha = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.texto
	def envia(self):
		for numero in self.numeros.all():
			newlog = log(numero = '+34' + numero.movil, texto = self.texto, enviado=False)
			envio = sms_multi(self.texto,numero.movil,newlog)
			envio.start()
		return True
			
	
class log(models.Model):
	numero = models.CharField(max_length=15)
	texto = models.TextField()
	enviado = models.BooleanField()
	respuesta = models.TextField()
	fecha = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return '%s\t%s\t%s\t%s' % (self.fecha, self.numero, self.texto, self.enviado)

class sms_multi(threading.Thread):
	texto = None
	numero = None
	newlog = None
	def __init__ (self,texto,numero,newlog):
		threading.Thread.__init__(self)
		self.texto = texto
		self.numero = numero
		self.newlog = newlog

	def run(self):
		sem.acquire()
		if re.match("^6\d{8}", self.numero):
			print('Enviando a ' '+34' + self.numero)
			resultado = send_sms ('+34' + self.numero, self.texto)
			self.newlog.respuesta = resultado
			dom = minidom.parseString(resultado)
			if dom.getElementsByTagName('result')[0].firstChild.data == '1':
				self.newlog.enviado = True
#			if dom.getElementsByTagName('description')[0].firstChild.data == u'Sorry, you do not have enough credit to send this sms. Go to your accountpage to buy credit!':
#				self.newlog.enviado = False
		else:
			self.newlog.resultado = "El numero es incorrecto o no es un movil."
		self.newlog.save()
		sem.release()

