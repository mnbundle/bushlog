from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import DetailView, ListView, TemplateView

# set admin to autodiscover registered admin classes
admin.autodiscover()

# static url patterns
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
)

# admin url patterns
urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# media url required for development
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/media' % settings.PROJECT_PATH}),
    )
