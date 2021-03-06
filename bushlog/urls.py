from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views import generic

from bushlog.sitemap import sitemaps

# set admin to autodiscover registered admin classes
admin.autodiscover()

# static url patterns
urlpatterns = patterns('bushlog.views',
    url(r'^$', generic.TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^about/$', generic.TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^affiliates/$', generic.TemplateView.as_view(template_name="affiliates.html"), name='affiliates'),
    url(r'^legal/$', generic.TemplateView.as_view(template_name="legal.html"), name='legal'),
    url(r'^press/$', generic.TemplateView.as_view(template_name="press.html"), name='press'),
    url(r'^support/$', 'support', name='support'),
    url(r'^researchers/$', generic.TemplateView.as_view(template_name="researchers.html"), name='researchers')
)

# admin url patterns
urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls))
)

# like url patterns
urlpatterns += patterns('',
    url(r'^action/', include('bushlog.apps.action.urls', namespace='like'))
)

# user profile url patterns
urlpatterns += patterns('',
    url(r'^profile/', include('bushlog.apps.profile.urls', namespace='profile'))
)

# reserve url patterns
urlpatterns += patterns('',
    url(r'^reserve/', include('bushlog.apps.reserve.urls', namespace='reserve'))
)

# sighting url patterns
urlpatterns += patterns('',
    url(r'^sighting/', include('bushlog.apps.sighting.urls', namespace='sighting'))
)

# wildlife url patterns
urlpatterns += patterns('',
    url(r'^wildlife/', include('bushlog.apps.wildlife.urls', namespace='wildlife'))
)

# social auth url patterns
urlpatterns += patterns('',
    url(r'social/', include('social_auth.urls'))
)

# api url patterns
urlpatterns += patterns('',
    url(r'^api/', include('bushlog.api.urls', namespace='api')),
)

# sso related url patterns
urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)

# serves static file in development
urlpatterns += staticfiles_urlpatterns()

# serves media files in development
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^templates\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.TEMPLATE_DIRS[0]})
    )
