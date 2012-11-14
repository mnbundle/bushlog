from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def humanize_measurement(measurement, unit):
    return "%s%s" % (intcomma(float(measurement) / 1000.0), unit)
