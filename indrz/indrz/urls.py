from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import javascript_catalog


from maps.views import view_map

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('maps', 'poi_manager', ),
}


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', view_map),  # homepage start page url
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    url(r'^api/v1/', include('api.urls')),
    url(r'^map/', include('maps.urls')),
    url(r'^poi/', include('poi_manager.urls')),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict,
        name='javascript-catalog'),

]


urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^rosetta/', include('rosetta.urls')),
    ]

if 'rest_framework_swagger' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^api/v1/docs/', include('rest_framework_swagger.urls')),
    ]
