from .models import samberos
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings


def send_notification_emails(actuacion):
    from_email = settings.DEFAULT_FROM_EMAIL
    if settings.EMAIL_RECIPIENT_DELIMITER:
        DEFAULT_FROM_EMAIL_USERNAME, DEFAULT_FROM_EMAIL_DOMAIN = settings.DEFAULT_FROM_EMAIL.split('@')
        from_email = "{}{}{}@{}".format(DEFAULT_FROM_EMAIL_USERNAME, settings.EMAIL_RECIPIENT_DELIMITER, actuacion.id,
                                        DEFAULT_FROM_EMAIL_DOMAIN)

    for sambero in samberos.objects.filter(
                                is_active=True,
                                backstage=False,
                                notification_email=True
                                ):

        subject = "{} Nueva Actuacion - {} - {}".format(
            settings.EMAIL_SUBJECT_PREFIX,
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
