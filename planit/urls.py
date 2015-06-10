from django.conf.urls import patterns, url
from planit import views

urlpatterns = patterns('',
    # url(r'getHeatMap/', views.getNode, name='getHeatMap'),
    url(r'uploadFile/', views.upload_form, name='uploadFile'), 
    url(r'showHeatMap/', views.showHeatMap, name='showHeatMap'), 
    # url(r'list/', views.list, name='list'),    
)
