from django.conf.urls import patterns, url
from webint import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
		url(r'^manifesty/', views.manifest, name ='manifest'),
		url(r'^customquerry/', views.customquerry, name ='customquerry'),
		url(r'^test/', views.test_view, name ='test'),
		url(r'^docs/', views.docs, name ='docs'),
		url(r'^login/', views.mylogin, name = 'login'),
		url(r'^logout/',views.mylogout, name = 'logout'))