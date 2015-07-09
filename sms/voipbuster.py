from django.conf import settings
import urllib
import urllib2

def send_sms(numero, texto, smsuser = settings.SMSUSER , smspwd = settings.SMSPWD):
	url = 'https://myaccount.voipbuster.com/clx/sendsms.php'
	values = {'username': smsuser,
		'password': smspwd,
		'to': numero,
		'text': texto.encode('utf-8') }
	uri = urllib.urlencode(values)
	return urllib2.urlopen(url, uri).read().replace("\t","").replace("\r","").replace("\n","").strip()
