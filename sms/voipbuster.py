# -*- coding: utf-8 -*-
from django.conf import settings
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse

def send_sms(numero, texto, smsuser = settings.SMSUSER , smspwd = settings.SMSPWD):
	url = 'https://www.voipbusterpro.com/myaccount/sendsms.php'
	values = {'username': smsuser,
		'password': smspwd,
		'to': numero,
		'text': texto.encode('utf-8')
 }
	uri = urllib.parse.urlencode(values)
	return urllib.request.urlopen(url, uri).read().replace("\t","").replace("\r","").replace("\n","").strip()
