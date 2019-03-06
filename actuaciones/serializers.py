from rest_framework import serializers, viewsets
from django.utils import timezone
from actuaciones.models import actuaciones, contactos, samberos, instrumentos, relaciones
from collections import OrderedDict


class NotNullFieldsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        result = super().to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class ContactosSerializer(NotNullFieldsSerializer):

    class Meta:
        model = contactos
        fields = ('id', 'name', 'phone', 'movil', 'mail')


class InstrumentosSerializer(serializers.ModelSerializer):

    class Meta:
        model = instrumentos
        fields = ('nombre')


class SamberosSerializer(NotNullFieldsSerializer):

    class Meta:
        model = samberos
        fields = ('username', 'email', 'phone', 'movil', 'instrumento')


class RelacionesSerializer(serializers.HyperlinkedModelSerializer):
    sambero = serializers.StringRelatedField(many=False)
    instrumento = serializers.StringRelatedField(many=False)

    class Meta:
        model = relaciones
        fields = ('sambero', 'instrumento')


class ActuacionesSerializer(serializers.HyperlinkedModelSerializer):
    contacto = ContactosSerializer(many=True, read_only=True)
    coches = serializers.StringRelatedField(many=True)
    formacion = RelacionesSerializer(read_only=True, many=True, source='samberos')

    class Meta:
        model = actuaciones
        fields = ('id', 'titulo', 'fecha', 'descripcion', 'lugar', 'confirmada', 'contacto', 'coches', 'formacion')

#    def to_representation(self, obj):
#        #print(obj.samberos.all())
#        ret = super().to_representation(obj)
#        formacion={}
#        for instru in obj.samberos.all().values('instrumento').order_by('instrumento__numero').distinct():
#            formacion[instrumentos.objects.get(id=list(instru.values())[0]).nombre]=obj.samberos.filter(instrumento__in=instru.values())
#        print(formacion)
#
#        ret['samberos']=formacion
#
#        return ret

class ActuacionesViewSet(viewsets.ModelViewSet):
    queryset = actuaciones.objects.filter(fecha__gte=timezone.now())
    serializer_class = ActuacionesSerializer
