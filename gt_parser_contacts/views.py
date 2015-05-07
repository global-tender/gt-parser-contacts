# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
	errors = []

	if request.POST.get('username', "").strip() != "" and request.POST.get('password', "").strip() != "":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				errors.append("Пользователь неактивен.")
		else:
			errors.append("Неверное имя пользователя или пароль.")

	template = loader.get_template('index.html')
	template_args = {
		'content': 'index_content.html',
		'request': request,
		'title': '',
		'errors': errors,
	}
	context = RequestContext(request, template_args)
	return StreamingHttpResponse(template.render(context))

def sign_out(request):
	if request.user.is_authenticated():
		logout(request)
	return HttpResponseRedirect('/')