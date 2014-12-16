from django.conf.urls import patterns, url
from webint import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^$', views.manifests, name='no_ajax'),
                       url(r'^alerts/$', views.alerts, name='alerts'),
					   url(r'^choose_rules/$', views.choose_rules, name='choose_rule'),
                       url(r'^containers/status/$', views.update_status, name="update_status"),
                       url(r'^containers/assignee/$', views.update_assignee, name="update_assignee"),
                       url(r'^manifests/', views.manifests, name='no_ajax'),
                       url(r'^manifests_datatables/', views.manifests_datatables, name='manifests_datatables'),
                       url(r'^containers_datatables/', views.containers_datatables, name='containers_datatables'),
                       url(r'^bills_datatables/', views.bills_datatables, name='bills_datatables'),
                       url(r'^bills_per_cont_datatables/(?P<containerID>\w*)/$', views.bills_per_cont_datatables,
                           name='bills_per_cont_datatables'),
                       url(r'^containers_with_status_datatables/', views.containers_with_status_datatables,
                           name='containers_with_status_datatables'),
                       url(r'^docs/', views.docs, name='docs'),
                       url(r'^login/', views.user_login, name='login'),
                       url(r'^logout/', views.user_logout, name='logout'),
                       url(r'^containers/', views.containers_view, name='containers_view'),
                       url(r'^bills/', views.bills_view, name='bills_view'),
                       url(r'^not_logged_in/', views.not_logged_in, name='not_logged_in'),
                       url(r'^bills_per_cont/(?P<containerID>\w*)/$', views.bills_per_cont, name='bills_per_cont'),
                       url(r'^usernames/$', views.get_usernames, name='get_usernames')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
