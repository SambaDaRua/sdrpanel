from .models import samberos
from django.template.loader import render_to_string
from django.utils import timezone


def send_notification_emails(actuacion):
    from_email = "panel+{}@test.sambadarua.org".format(actuacion.id)
    for sambero in samberos.objects.filter(
                                is_active=True,
                                backstage=False,
                                notification_email=True
                                ):

        subject = "[SDRPANEL] Nueva Actuacion - {} - {}".format(
            timezone.datetime.strftime(actuacion.fecha, '%d-%m-%y %H:%M'),
            actuacion.titulo
        )
        context = {
            'actuacion': actuacion,
            'sambero': sambero
        }
        html_message = render_to_string('notification_email.html', context)
        message = render_to_string('notification_email.txt', context)
        sambero.email_user(subject, message, from_email, html_message=html_message)
