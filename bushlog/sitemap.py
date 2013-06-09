from django.contrib import sitemaps
from django.core.urlresolvers import reverse

from bushlog.apps.profile.models import UserProfile
from bushlog.apps.reserve.models import Reserve
from bushlog.apps.sighting.models import Sighting
from bushlog.apps.wildlife.models import Species


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.4
    changefreq = 'monthly'

    def items(self):
        return ['index', 'about', 'affiliates', 'legal', 'press', 'support', 'researchers']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'static': StaticViewSitemap,
    'profiles': sitemaps.GenericSitemap({
        'queryset': UserProfile.objects.filter(user__is_active=True),
        'changefreq': 'weekly'
    }, priority=0.7),
    'reserves': sitemaps.GenericSitemap({
        'queryset': Reserve.objects.all(),
        'changefreq': 'daily'
    }, priority=0.6),
    'species': sitemaps.GenericSitemap({
        'queryset': Species.objects.all(),
        'changefreq': 'daily'
    }, priority=0.6),
    'sightings': sitemaps.GenericSitemap({
        'queryset': Sighting.objects.active().public(),
        'date_field': 'date_added',
        'changefreq': 'never'
    }, priority=0.8),
}
