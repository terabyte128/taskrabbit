from django.conf.urls import patterns, url

from taskrabbit import views

urlpatterns = patterns('',
    # universal patterns
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.log_out, name='log_out'),

    url(r'^teams/$', views.teams, name='teams'),
    url(r'^teams/(?P<team_id>[0-9]+)/$', views.teams, name='teams'),

    url(r'^claim/$', views.claim_task, name='claim_task'),

    url(r'^add/$', views.add_task, name='add_task'),

    url(r'^task/$', views.view_task, name='view_task'),
    url(r'^task/(?P<task_id>[0-9]+)/$', views.view_task, name='view_task')
)