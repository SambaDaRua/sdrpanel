from actuaciones.models import samberos, contactos, instrumentos, actuaciones
from django.contrib import admin
from django.contrib.auth.models import Group
from rangefilter.filter import DateRangeFilter


class actuacionesAdmin(admin.ModelAdmin):
    exclude = ['samberos']
    fields = ['titulo', 'fecha', 'descripcion', 'lugar', 'organizador', 'contacto', 'confirmada']
    list_display = ('fecha', 'titulo', 'lugar', 'confirmada')


class samberosAdmin(admin.ModelAdmin):
    exclude = ['user_permissions', 'groups', 'last_login', 'date_joined']
    list_display = (
                        'username', 'first_name', 'last_name',
                        'email', 'movil', 'instrumento',
                        'is_superuser', 'backstage', 'notification_email', 'is_active',
                        'last_login'
                    )
    list_filter = ('instrumento', 'is_active', 'backstage', ('last_login', DateRangeFilter))
    search_fields = ['username', 'first_name', 'last_name', 'email', 'movil', 'phone', 'instrumento__nombre']


admin.site.unregister(Group)
admin.site.register(contactos)
admin.site.register(samberos, samberosAdmin)
admin.site.register(instrumentos)
admin.site.register(actuaciones, actuacionesAdmin)
