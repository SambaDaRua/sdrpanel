# Generated by Django 2.1.5 on 2019-02-28 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actuaciones', '0003_auto_20190204_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='samberos',
            name='notification_email',
            field=models.BooleanField(default=True, help_text='Recibir correos de notificación de las actuaciones'),
        ),
    ]
