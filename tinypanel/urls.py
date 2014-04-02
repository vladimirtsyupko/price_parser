from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from airlines_parser import views as airlines_views
from tinypanel import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', airlines_views.index, name='index'),
    url(r'^flight_list/$', airlines_views.flight_list, name="flight_list"),
    url(r'^parse_flight/$', airlines_views.parse_flight, name="parse_flight"),
    url(r'^flight/$', airlines_views.flight_detail, name="flight_detail"),
    url(r'^get_flight_info/$', airlines_views.get_flight_info),
    url(r'^get_flight_info_by_date/$', airlines_views.get_flight_info_by_date),
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)