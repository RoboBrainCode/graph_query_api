from django.conf.urls import patterns, url
from graph_query_api.nlquery import views

urlpatterns = patterns('',
    url(r'langquery/', views.return_nlquery_result, name='nlquery'),
)
