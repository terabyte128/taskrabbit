from django.conf.urls import patterns, url

from taskrabbit import views

urlpatterns = patterns('',
    # universal patterns
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.log_out, name='log_out'),
    url(r'^search/$', views.search, name='search'),
    url(r'^all/$', views.all_tasks, name='all_tasks'),

    # sort by teams page
    url(r'^teams/$', views.teams, name='teams'),
    url(r'^teams/(?P<team_id>[0-9]+)/$', views.teams, name='teams'),

    url(r'^status/$', views.statuses, name='statuses'),
    url(r'^status/(?P<status_id>[0-9]+)/$', views.statuses, name='statuses'),

    url(r'^claim/$', views.claim_task, name='claim_task'),


    url(r'^task/$', views.view_task, name='view_task'),
    url(r'^task/(?P<task_id>[0-9]+)/$', views.view_task, name='view_task'),


    # get things as json
    url(r'^json/statuses/$', views.get_statuses, name='get_statuses_as_json'),
    url(r'^json/users/$', views.get_users, name='get_users_as_json'),

    # updates db objects
    url(r'^update/task/$', views.update_task, name='update_task'),

    #add things
    url(r'^add/task/$', views.add_task, name='add_task'),
    url(r'^add/note/$', views.add_note, name='add_note'),
)