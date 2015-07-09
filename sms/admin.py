from sdrpanel.sms.models import log, sms
from django.contrib import admin

class smssms(admin.ModelAdmin):
	list_display = ('fecha', 'texto')
class smslog(admin.ModelAdmin):
	list_display = ('fecha', 'numero', 'texto', 'enviado')
	

admin.site.register(sms, smssms)
admin.site.register(log, smslog)
