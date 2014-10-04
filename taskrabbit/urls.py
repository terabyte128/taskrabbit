from django.conf.urls import patterns, url

from taskrabbit import views

urlpatterns = patterns('',
    # universal patterns
    url(r'^$', views.index, name='index'),

    url(r'^teams/$', views.teams, name='teams'),
    url(r'^teams/(?P<team_id>[0-9]+)/$', views.teams, name='teams'),

    url(r'^claim/$', views.claim_task, name='claim_task'),

    url(r'^add/$', views.add_task, name='add_task'),
)