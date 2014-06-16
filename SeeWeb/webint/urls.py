from django.conf.urls import patterns, url
from webint import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
		url(r'^customquerry/', views.customquerry, name ='customquerry'),
		url(r'^test/', views.test_view, name ='test'),
		url(r'^docs/', views.docs, name ='docs'),
		url(r'^login/', views.mylogin, name = 'login'),
		url(r'^logout/',views.mylogout, name = 'logout'),
		url(r'^not_logged_in/',views.not_logged_in, name ='not_logged_in'),
		url(r'^manifestID/(?P<manifestID>\w*-\w*-\w*-\w*-\w*)/$', views.single_manifest_details, name='single_manifest_details'),
		url(r'^ajax/id/(?P<manifestID>\w*-\w*-\w*-\w*-\w*)/page/(?P<pagenumber>\d+)/$',views.ajax_bills_per_manifest , name='ajaxbills'),
		url(r'^ajax/cont/(?P<manifestID>\w*-\w*-\w*-\w*-\w*)/page/(?P<pagenumber>\d+)/$',views.ajax_conts_per_manifest , name='ajaxcont'),
		url(r'^page/(?P<pagenumber>\d+)/$', views.test_ajax, name='ajaxtest'),)