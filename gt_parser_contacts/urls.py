from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView

from gt_parser_contacts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)