# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=15)),
                ('texto', models.TextField()),
                ('enviado', models.BooleanField()),
                ('respuesta', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='sms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('numeros', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
