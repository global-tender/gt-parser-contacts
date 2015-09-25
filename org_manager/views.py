# -*- coding: utf-8 -*-
import json, time
import random, string
import os
import ast
from subprocess import Popen, PIPE

from django.conf import settings
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

from org_manager import utility

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

	accessible = True
	# try:
	# 	st = urllib2.urlopen('http://zakupki.gov.ru/223/ppa/public/organization/organization.html').read()
	# except:
	# 	accessible = False

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

			# Generated dictionary to json file
			t = time.localtime( time.time() )
			t = time.strftime( '%Y-%m-%dT%H-%M-%S', t )

			def randomword(length):
				return ''.join(random.choice(string.lowercase) for i in range(length))

			json_obj = json.dumps(contacts, indent=4)
			fn = os.getcwd() + os.sep + 'org_manager/static/json/' + t + randomword(5) + '.json'
			fo = open(fn, "w")
			fo.write(json_obj)
			fo.close()

			# Process json file with python3
			script = os.getcwd() + os.sep + 'org_manager/scripts/proc_contacts.py'
			command = "python3 %s %s" % (script, fn)
			proc = Popen(command.split(), stdout=PIPE).communicate()

			if proc[0] == "error":
				xlsx_errors.append('Failed to create xlsx file.')
			else:
				xlsx_file = proc[0]

	template = loader.get_template('index.html')
	template_args = {
		'content': 'index_content.html',
		'request': request,
		'title': '',
		'accessible': accessible,
		'regions': regions,
		'errors': errors,
		'pages': pages,
		'pages_errors': pages_errors,
		'xlsx_file': xlsx_file,
		'xlsx_errors': xlsx_errors,
		'contact_errors': contact_errors,
	}
	context = RequestContext(request, template_args)
	return StreamingHttpResponse(template.render(context))

def sign_out(request):
	if request.user.is_authenticated():
		logout(request)
	return HttpResponseRedirect('/')

def clear(request):
	return HttpResponseRedirect('/')