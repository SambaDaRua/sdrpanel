# Generated by Django 2.1.7 on 2019-10-04 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actuaciones', '0004_samberos_notification_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samberos',
            name='backstage',
            field=models.BooleanField(default=False, help_text='Estoy en activo, pero no tocando instrumentos.\n                                    <br/>No recibirás correos de notificación de actuaciones'),
        ),
        migrations.AlterField(
            model_name='samberos',
            name='instrumento',
            field=models.ForeignKey(help_text='Instrumento principal', null=True, on_delete=django.db.models.deletion.SET_NULL, to='actuaciones.instrumentos'),
        ),
        migrations.AlterField(
            model_name='samberos',
            name='movil',
            field=models.CharField(blank=True, max_length=9, null=True, verbose_name='Móvil'),
        ),
        migrations.AlterField(
            model_name='samberos',
            name='notification_email',
            field=models.BooleanField(default=True, help_text='Recibir correos de notificación de las actuaciones\n                                             <br/>Se enviarán correos de actuaciones nuevas o\n                                             <br/>cuando cambie la fecha de las actuaciones.', verbose_name='Emails de notificación'),
        ),
        migrations.AlterField(
            model_name='samberos',
            name='phone',
            field=models.CharField(blank=True, max_length=9, null=True, verbose_name='Télefono'),
        ),
    ]