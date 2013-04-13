from django.contrib.sitemaps import GenericSitemap

from bushlog.apps.profile.models import UserProfile
from bushlog.apps.reserve.models import Reserve
from bushlog.apps.sighting.models import Sighting
from bushlog.apps.wildlife.models import Species


sitemaps = {
    'profiles': GenericSitemap({
        'queryset': UserProfile.objects.filter(user__is_active=True),
        'date_field': 'last_login'
    }, priority=0.6),
    'reserves': GenericSitemap({
        'queryset': Reserve.objects.all()
    }, priority=0.6),
    'sightings': GenericSitemap({
        'queryset': Sighting.objects.all(),
        'date_field': 'date_added'
    }, priority=0.8),
    'reserves': GenericSitemap({
        'queryset': Species.objects.all()
    }, priority=0.6),
}
