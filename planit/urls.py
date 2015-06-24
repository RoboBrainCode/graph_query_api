from django.conf.urls import patterns, url
from planit import views

urlpatterns = patterns('',
    url(r'uploadFile/', views.upload_form, name='uploadFile'), 
    url(r'showHeatMap/', views.showHeatMap, name='showHeatMap'), 
    url(r'getTraj/', views.returnTraj, name='returnTraj'),    
    url(r'getLog/', views.returnLog, name='returnLog'),    
)
