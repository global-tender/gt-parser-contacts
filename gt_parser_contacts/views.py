# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

from gt_parser_contacts import utility

@csrf_exempt
def index(request):
	errors = []
	pages_errors = []
	contact_errors = []
	xlsx_errors = []

	regions = []
	pages = 0
	contacts = None
	xlsx_file = None

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

	if request.user.is_authenticated():
		if request.POST.get('request_contacts_of_region', "").strip() == "":
			regions, errors = utility.getRegionList()
		else:
			fz = request.POST.get('fz', "")
			region = request.POST.get('region', "")
			pageNumber = '1'
			perPage = '10'

			pages, pages_errors = utility.getAmountPages(fz, region, pageNumber, perPage)


			all_links = {}

			for page in range(pages):
				pg = page+1

				res, errors = utility.getCompanyList(fz, region, pg, perPage)

				all_links = dict(list(all_links.items()) + list(res.items()))

			contacts = {}
			for org_url, org_name in all_links.iteritems():
				parsed_details, contact_errors = utility.getOrganizationContacts(org_url, org_name)

				contacts[org_url] = parsed_details
			#xlsx_file, xlsx_errors = utility.createXLSX(contacts)

	template = loader.get_template('index.html')
	template_args = {
		'content': 'index_content.html',
		'request': request,
		'title': '',
		'regions': regions,
		'errors': errors,
		'pages': pages,
		'pages_errors': pages_errors,
		'xlsx_file': xlsx_file,
		'xlsx_errors': xlsx_errors,
		'contact_errors': contact_errors,
		'contacts': contacts,
	}
	context = RequestContext(request, template_args)
	return StreamingHttpResponse(template.render(context))

def sign_out(request):
	if request.user.is_authenticated():
		logout(request)
	return HttpResponseRedirect('/')

def clear(request):
	return HttpResponseRedirect('/')