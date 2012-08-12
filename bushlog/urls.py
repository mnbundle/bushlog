from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import FormView

# set admin to autodiscover registered admin classes
admin.autodiscover()

# static url patterns
urlpatterns = patterns('',
    url(r'^$', FormView.as_view(template_name="index.html", form_class=AuthenticationForm), name='index'),
)

# admin url patterns
urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# auth url patterns
urlpatterns += patterns('',
    url(r'^profile/', include('bushlog.apps.profile.urls', namespace='profile')),
)

# serves static file while DEBUG is true
urlpatterns += staticfiles_urlpatterns()

# serves media files in development
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
