from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'graph_query_api.views.home', name='home'),
    # url(r'^graph_query_api/', include('graph_query_api.foo.urls')),
    url(r'^graph_query/',include('nlquery.urls')),
    #url(r'^graph_viz/',include('vizquery.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
