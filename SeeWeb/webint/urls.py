from django.conf.urls import patterns, url
from webint import views

urlpatterns = patterns('',
                       url(r'^$', views.manifests_no_ajax, name='no_ajax'),
                       url(r'^containers/status/$', views.update_status, name="update_status"),
                       url(r'^manifest_no_ajax/', views.manifests_no_ajax, name='no_ajax'),
                       url(r'^manifests_datatables/', views.manifests_datatables, name='manifests_datatables'),
                       url(r'^containers_datatables/', views.containers_datatables, name='containers_datatables'),
                       url(r'^bills_datatables/', views.bills_datatables, name='bills_datatables'),
                       url(r'^bills_per_cont_datatables/(?P<containerID>\w*)/$', views.bills_per_cont_datatables,
                           name='bills_per_cont_datatables'),
                       url(r'^containers_with_status_datatables/', views.containers_with_status_datatables,
                           name='containers_with_status_datatables'),
                       url(r'^customquerry/', views.customquerry, name='customquerry'),
                       url(r'^test/', views.test_view, name='test'),
                       url(r'^docs/', views.docs, name='docs'),
                       url(r'^login/', views.mylogin, name='login'),
                       url(r'^logout/', views.mylogout, name='logout'),
                       url(r'^containers/', views.containers_view, name='containers_view'),
                       url(r'^bills/', views.bills_view, name='bills_view'),
                       url(r'^not_logged_in/', views.not_logged_in, name='not_logged_in'),
                       url(r'^bills_per_cont/(?P<containerID>\w*)/$', views.bills_per_cont, name='bills_per_cont'),
                       url(r'^manifestID/(?P<manifestID>\w*-\w*-\w*-\w*-\w*)/$', views.single_manifest_details,
                           name='single_manifest_details'),
                       url(r'^unbreference/(?P<unbRef>\w*)/$', views.unb_single_manifest_details,
                           name='unb_single_manifest_details'),
                       url(r'^ajax/id/(?P<manifestID>\w*-\w*-\w*-\w*-\w*)/page/(?P<pagenumber>\d+)/$',
                           views.ajax_bills_per_manifest, name='ajaxbills'),
                       url(r'^ajax/cont/(?P<manifestID>\w*-\w*-\w*-\w*-\w*)/page/(?P<pagenumber>\d+)/$',
                           views.ajax_conts_per_manifest, name='ajaxcont'),
                       url(r'^page/(?P<pagenumber>\d+)/$', views.test_ajax, name='ajaxtest')
                       )
