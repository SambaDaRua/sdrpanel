from datetime import timedelta as td
from django.utils import timezone
from django.conf import settings
from dateutil.parser import parse
from actuaciones.models import samberos


def LastUserActivityMiddleware(get_response):
    def middleware(request):
        KEY = "last-activity"
        if request.user.is_authenticated:
            last_activity = request.session.get(KEY)
            too_old_time = timezone.now() - td(seconds=settings.LAST_ACTIVITY_INTERVAL_SECS)
            if not last_activity or parse(last_activity) < too_old_time:
                samberos.objects.filter(pk=request.user.pk).update(
                    last_login=timezone.now(),
                )
                request.session[KEY] = timezone.now().isoformat()
        response = get_response(request)
        return response
    return middleware
