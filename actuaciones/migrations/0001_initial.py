# -*- coding: utf-8 -*-


from django.db import models, migrations
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='samberos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('backstage', models.BooleanField(default=False, help_text=b'Si el sambero esta activo, pero no tocando instrumentos ... ')),
                ('dni', models.CharField(max_length=10, null=True, blank=True)),
                ('phone', models.CharField(max_length=9, null=True, blank=True)),
                ('movil', models.CharField(help_text=b'Este es el numero para los SMS', max_length=9, null=True, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
            ],
            options={
                'ordering': ['username'],
                'verbose_name': 'samberos',
                'verbose_name_plural': 'samberos',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='actuaciones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=80)),
                ('fecha', models.DateTimeField()),
                ('descripcion', models.TextField()),
                ('lugar', models.CharField(max_length=200)),
                ('confirmada', models.BooleanField(default=False)),
                ('coches', models.ManyToManyField(related_name='actuaciones_coches', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['-fecha'],
                'verbose_name': 'actuacion',
                'verbose_name_plural': 'actuaciones',
            },
        ),
        migrations.CreateModel(
            name='contactos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=9, null=True, blank=True)),
                ('movil', models.CharField(max_length=9, null=True, blank=True)),
                ('mail', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'contactos',
                'verbose_name_plural': 'contacto',
            },
        ),
        migrations.CreateModel(
            name='instrumentos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=10)),
                ('numero', models.PositiveSmallIntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'instrumentos',
                'verbose_name_plural': 'instrumento',
            },
        ),
        migrations.CreateModel(
            name='relaciones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instrumento', models.ForeignKey(to='actuaciones.instrumentos', on_delete=models.CASCADE)),
                ('sambero', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='actuaciones',
            name='contacto',
            field=models.ManyToManyField(to='actuaciones.contactos'),
        ),
        migrations.AddField(
            model_name='actuaciones',
            name='organizador',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='actuaciones',
            name='samberos',
            field=models.ManyToManyField(to='actuaciones.relaciones', blank=True),
        ),
        migrations.AddField(
            model_name='samberos',
            name='instrumento',
            field=models.ForeignKey(to='actuaciones.instrumentos', null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='samberos',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
