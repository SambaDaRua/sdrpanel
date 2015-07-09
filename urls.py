from django.conf.urls.defaults import *
from django.contrib import admin
import django.contrib.auth.views
admin.autodiscover()

urlpatterns = patterns('',
	# Example:
	# (r'^sdrpanel/', include('sdrpanel.foo.urls')),
	(r'^$', 'sdrpanel.actuaciones.views.index'),

	(r'^actuaciones/$', 'sdrpanel.actuaciones.views.index'),

	(r'^samberos/$', 'sdrpanel.actuaciones.views.listado_samberos'),
	(r'^samberos/csv/$', 'sdrpanel.actuaciones.views.samberos_csv'),
	(r'^samberos/(?P<username>\w+)/$', 'sdrpanel.actuaciones.views.datos_sambero'),

	(r'^contactos/$', 'sdrpanel.actuaciones.views.listado_contactos'),
	(r'^contactos/(?P<id>\d+)/$', 'sdrpanel.actuaciones.views.datos_contacto'),

	(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/sdrpanel/css'}),
	(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/sdrpanel/js'}),
	(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/sdrpanel/images'}),
	(r'^greybox/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/sdrpanel/greybox'}),
	
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^logout/$', 'django.contrib.auth.views.logout'),
	(r'^cambio_datos/$', 'sdrpanel.actuaciones.views.cambio_datos'),
	(r'^sms/$', 'sdrpanel.sms.views.index'),
	    
	
	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	# Uncomment the next line to enable the admin:
	(r'^admin/(.*)', admin.site.root),
	(r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
	(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
	(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
	(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
)
