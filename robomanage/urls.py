from django.conf.urls import patterns, url

from robomanage import views

urlpatterns = patterns('',
    url(r'^(?P<page>\d)$', views.index_view, name='index_view'),
    url(r'^$', views.index_view, name='index_view'),

    url(r'^login/', views.login_view, name='login_view'),
    url(r'^logout/', views.logout_view, name='logout_view'),

    url(r'^in/', views.clock_in_view, name='clock_in_view'),
    url(r'^out/', views.clock_out_view, name='clock_out_view'),

    url(r'^nfc/toggle/', views.toggle_clocked_in, name='toggle_clocked_in'),
    url(r'^nfc/check/', views.check_if_clocked_in, name='check_if_clocked_in'),

    url(r'^history/$', views.history_view, name='history_view'),
    url(r'^history/(?P<username>\w.{1,50})/$', views.history_view, name='history_view'),

    url(r'^supervisor/$', views.supervisor_view, name='supervisor_view'),
    url(r'^supervisor/out/', views.supervisor_clock_all_out, name='supervisor_clock_all_out'),
    url(r'^supervisor/all/', views.supervisor_all_users_view, name='supervisor_all_users_view')
)