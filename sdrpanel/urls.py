#from django.conf.urls.defaults import *

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles import views

from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from actuaciones import views as actuaciones_views
from sms import views as sms_views
import os

from django.views.static import serve



#from django.contrib import admin
#import django.contrib.auth.views
#admin.autodiscover()

urlpatterns = [
        url(r'^$', actuaciones_views.index),
        url(r'^actuaciones/$', actuaciones_views.index),
        url(r'^samberos/$', actuaciones_views.listado_samberos),
        url(r'^samberos/csv/$', actuaciones_views.samberos_csv),
        url(r'^samberos/(?P<username>\w+)/$', actuaciones_views.datos_sambero),
        url(r'^contactos/$', actuaciones_views.listado_contactos),
        url(r'^contactos/(?P<id>\d+)/$', actuaciones_views.datos_contacto),
        url(r'^cambio_datos/$', actuaciones_views.cambio_datos),
        url(r'^login/$', login, name='sdrlogin'),
        url(r'^logout/$', logout, name='sdrlogout'),
        url(r'^sms/$', sms_views.index),
        url('^admin/', include(admin.site.urls)),
        url(r'^password_reset/$', password_reset, name='password_reset'),
        url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
        url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
        url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^css/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR,'css')}),
        url(r'^js/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR,'js')}),
        url(r'^images/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR,'images')}),
        url(r'^greybox/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR,'greybox')}),
        url(r'^static/(?P<path>.*)$', views.serve),
   ]
