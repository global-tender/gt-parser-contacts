from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView

from gt_parser_contacts import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),

	url(r'^logout/?$', views.sign_out, name='sign_out'),

	url(r'^robots\.txt$', RedirectView.as_view(url='/static/robots.txt')),
)