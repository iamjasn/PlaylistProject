from django.conf.urls import patterns, url
from gen_playlists import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    )