from django_ical.views import ICalFeed
from actuaciones.models import actuaciones


class ActuacionesFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = '-//sdrpanel//actuaciones//ES'
    timezone = 'UTC'
    file_name = "actuaciones.ics"

    def items(self):
        return actuaciones.objects.all().order_by('-fecha')

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
        return item.descripcion

    def item_start_datetime(self, item):
        return item.fecha

    def item_link(self, item):
        return "/#id%s" % (item.id)

    def item_class(self, item):
        if item.confirmada:
            return "PUBLIC"
        return "PRIVATE"

    def item_status(self, item):
        if item.confirmada:
            return "CONFIRMED"
        return "TENTATIVE"

    def item_location(self, item):
        return item.lugar

    def item_created(self, item):
        return item.created_at

    def item_updateddate(self, item):
        return item.updated_at

    def item_organizer(self, item):
        return ', '.join([str(i) for i in item.organizador.all()])

