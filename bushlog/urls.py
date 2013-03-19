from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views import generic

# set admin to autodiscover registered admin classes
admin.autodiscover()

# static url patterns
urlpatterns = patterns('',
    url(r'^$', generic.TemplateView.as_view(template_name="index.html"), name='index')
)

# admin url patterns
urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls))
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

# comments framework patterns
urlpatterns += patterns('',
    url(r'^comments/', include('django.contrib.comments.urls', namespace='comments'))
)

# social auth urls
urlpatterns += patterns('',
    url(r'social/', include('social_auth.urls'))
)

# serves static file in development
urlpatterns += staticfiles_urlpatterns()

# serves media files in development
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^templates\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.TEMPLATE_DIRS[0]})
    )
