from django.conf.urls import patterns, include, url
from graph_query_api import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Backend.views.home', name='home'),
    url(r'nlquery/',include('nlquery.urls')),
)
