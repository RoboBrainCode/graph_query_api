from django.conf.urls import patterns, url
from vizquery import views

urlpatterns = patterns('',
    url(r'get_node/', views.get_node, name='get_node'),
)
