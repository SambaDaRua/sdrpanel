from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class instrumentos(models.Model):
    nombre = models.CharField(max_length=10)
    numero = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['id']
        verbose_name_plural = "instrumento"
        verbose_name = "instrumentos"


class samberos(AbstractUser):
    objects = UserManager()
    backstage = models.BooleanField(default=False,
                                    help_text="Si el sambero esta activo, pero no tocando instrumentos ... ")
    dni = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=9, blank=True, null=True)
    movil = models.CharField(max_length=9, blank=True, null=True,
                             help_text="Este es el numero para los SMS")
    instrumento = models.ForeignKey(instrumentos, null=True, on_delete=models.SET_NULL)
    notification_email = models.BooleanField(default=True,
                                             help_text="Recibir correos de notificación de las actuaciones")

    def url(self):
        return '<a href="/samberos/{0}/" title="{0}" rel="gb_page_center[400, 210]">{0}</a>'.format(self.username)

    class Meta:
        ordering = ['username']
        verbose_name_plural = "samberos"
        verbose_name = "samberos"


class contactos(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=9, blank=True, null=True)
    movil = models.CharField(max_length=9, blank=True, null=True)
    mail = models.CharField(max_length=30, blank=True, null=True)

    def url(self):
        return '<a href="/contactos/{0}/" title="{1}" rel="gb_page_center[400, 150]">{1}</a>'.format(self.id, self.name)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "contacto"
        verbose_name = "contactos"


class relaciones(models.Model):
    sambero = models.ForeignKey(samberos, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(instrumentos, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s => %s' % (self.sambero, self.instrumento)

    def get_ids(self):
        return self.pk


class actuaciones(models.Model):
    titulo = models.CharField(max_length=80)
    fecha = models.DateTimeField()
    descripcion = models.TextField()
    lugar = models.CharField(max_length=200)
    organizador = models.ManyToManyField(samberos)
    coches = models.ManyToManyField(samberos, blank=True, related_name='actuaciones_coches')
    samberos = models.ManyToManyField(relaciones, blank=True,)
    confirmada = models.BooleanField(default=False)
    contacto = models.ManyToManyField(contactos)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha']
        verbose_name_plural = "actuaciones"
        verbose_name = "actuacion"
