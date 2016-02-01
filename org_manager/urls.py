from django.conf.urls import url, include
from django.http import StreamingHttpResponse

from org_manager import views

urlpatterns = [
	url(r'^$', views.index, name='index'),

	url(r'^logout/?$', views.sign_out, name='sign_out'),
	url(r'^clear/?$', views.clear, name='clear'),

	url(r'^robots.txt$', lambda r: StreamingHttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
]