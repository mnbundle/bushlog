from django.contrib import sitemaps
from django.core.urlresolvers import reverse_lazy

from bushlog.apps.profile.models import UserProfile
from bushlog.apps.reserve.models import Reserve
from bushlog.apps.sighting.models import Sighting
from bushlog.apps.wildlife.models import Species


class StaticViewSitemap(sitemaps.Sitemap):

    def items(self):
        return ['index', 'about', 'affiliates', 'legal', 'press', 'support', 'reserve:list']

    def location(self, item):
        return reverse_lazy(item)

    def priority(self, item):
        priority_map = {
            'index': 1.0,
            'about': 0.8,
            'press': 0.8,
            'support': 0.7,
            'reserve:list': 0.8
        }
        return priority_map.get(item, 0.6)

    def changefreq(self, item):
        changefreq_map = {
            'index': 'daily'
        }
        return changefreq_map.get(item, 'monthly')


class SightingComboViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        items = []
        for reserve in Reserve.objects.all():
            items += ["%s|%s" % (reserve.slug, species.slug) for species in reserve.species.all()]
        return items

    def location(self, item):
        return reverse_lazy('sighting:list', args=item.split('|'))


sitemaps = {
    'static': StaticViewSitemap,
    'sighting_combo': SightingComboViewSitemap,
    'profiles': sitemaps.GenericSitemap({
        'queryset': UserProfile.objects.filter(user__is_active=True),
    }, priority=0.4, changefreq='weekly'),
    'reserves': sitemaps.GenericSitemap({
        'queryset': Reserve.objects.all()
    }, priority=0.7, changefreq='daily'),
    'species': sitemaps.GenericSitemap({
        'queryset': Species.objects.all()
    }, priority=0.7, changefreq='daily'),
    'sightings': sitemaps.GenericSitemap({
        'queryset': Sighting.objects.active().public(),
        'date_field': 'date_added'
    }, priority=0.3, changefreq='never'),
}
