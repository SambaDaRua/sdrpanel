import os

from django.urls import re_path, path, include
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles import views as static_views
from django.contrib.auth import views as auth_views
from actuaciones import views as actuaciones_views
from actuaciones.feeds import ActuacionesFeed
from django.views.static import serve
from sdrpanel.views import CustomLogoutView


urlpatterns = [
        re_path(r'^admin/', admin.site.urls),
        path('', include('django.contrib.auth.urls')),
        re_path(r'^$', actuaciones_views.index),
        re_path(r'^actuaciones/$', actuaciones_views.index),
        re_path(r'^actuaciones/actuaciones.ics$', ActuacionesFeed()),
        re_path(r'^samberos/$', actuaciones_views.listado_samberos),
        re_path(r'^samberos/csv/$', actuaciones_views.samberos_csv),
        re_path(r'^samberos/(?P<username>\w+)/$', actuaciones_views.datos_sambero),
        re_path(r'^contactos/$', actuaciones_views.listado_contactos),
        re_path(r'^contactos/(?P<id>\d+)/$', actuaciones_views.datos_contacto),
        re_path(r'^cambio_datos/$', actuaciones_views.cambio_datos),
        re_path(r'^login/$', auth_views.LoginView.as_view(), name='sdrlogin'),
        re_path(r'^sdrout/$', CustomLogoutView.as_view(), name='sdrlogout'),
        re_path(r'^logout/$', CustomLogoutView.as_view(), name='sdrlogout'),
        re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
        re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
        re_path(r'^borrar_cuenta/$', actuaciones_views.account_remove_delete),

]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^css/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'css')}),
        re_path(r'^js/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'js')}),
        re_path(r'^images/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'images')}),
        re_path(r'^greybox/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'greybox')}),
        re_path(r'^static/(?P<path>.*)$', static_views.serve)
    ]

admin.site.site_header = "Administración de SDRPANEL"
admin.site.site_title = "Administración de SDRPANEL"
