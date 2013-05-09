from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from bushlog.apps.wildlife.models import Species

register = template.Library()


@register.filter
def humanize_measurement(measurement, unit):
    return "%s%s" % (intcomma(float(measurement) / 1000.0), unit)


@register.simple_tag
def species_count():
    return intcomma(Species.objects.all().count())
