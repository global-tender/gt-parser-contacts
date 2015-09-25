from django.conf.urls import patterns, url, include
from django.http import StreamingHttpResponse

from gt_parser_contacts import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),

	url(r'^logout/?$', views.sign_out, name='sign_out'),
	url(r'^clear/?$', views.clear, name='clear'),

	url(r'^robots.txt$', lambda r: StreamingHttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
)