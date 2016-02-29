# -*- coding: utf-8 -*-
import json, time
import string
import os
import xlsxwriter
import pytz

from django.conf import settings
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

from org_manager.models import Organizations
from org_manager.models import Contacts_223_FZ
from org_manager.models import Contacts_44_FZ
from org_manager.models import Regions


@csrf_exempt
def index(request):
	errors = []
	xlsx_file = None
	regions = None

	selected_region = None
	selected_fz = None
	selected_level = None
	amount_orgs = 0


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

		if request.method == 'GET':
			regions = Regions.objects.exclude(date_completed__isnull=True)

		else: # POST
			region_value = request.POST.get('region', '')
			fz_value = request.POST.get('fz', '')
			org_level_value = request.POST.get('org_level', '')


			if fz_value == 'FZ_223':

				if org_level_value and org_level_value != 'any':
					orgs = Organizations.objects.filter(org_region=region_value,works_with_223=True,org_level_223=org_level_value)
				else:
					orgs = Organizations.objects.filter(org_region=region_value,works_with_223=True)

			else: #'FZ_94':

				if org_level_value and org_level_value != 'any':
					orgs = Organizations.objects.filter(org_region=region_value,works_with_44=True,org_level_44=org_level_value)
				else:
					orgs = Organizations.objects.filter(org_region=region_value,works_with_44=True)

			amount_orgs = len(orgs)

			selected_region = Regions.objects.filter(region_code=region_value).first()

			custLev_list = {
				'F': u'Федеральный уровень',
				'S': u'Уровень субъекта РФ',
				'M': u'Муниципальный уровень',
				'NOT_FSM': u'Иное',
				'any': u'Любой',
			}

			fz_list = {
				'FZ_223': u'223-ФЗ',
				'FZ_94': u'44-ФЗ',
			}

			selected_fz = fz_list[fz_value]
			selected_level = custLev_list[org_level_value]

			##############################
			##############################
			local_tz = pytz.timezone('Europe/Moscow')
			t = time.localtime( time.time() )
			t = time.strftime( '%Y-%m-%dT%H-%M-%S', t )

			xlsx_file = 'zakupki_' + t + '.xlsx'
			fullpath = os.getcwd() + os.sep + 'org_manager/static/xlsx/' + xlsx_file

			workbook = xlsxwriter.Workbook(fullpath)
			worksheet = workbook.add_worksheet()

			bold = workbook.add_format({'bold': True})


			worksheet.write(0, 0, u"" + selected_region.region_name, bold)
			worksheet.write(0, 1, u"" + selected_fz, bold)

			worksheet.write(0, 3, u"Дата обновления контактов по региону:"),
			worksheet.write(0, 4, str(selected_region.date_completed.replace(tzinfo=pytz.utc).astimezone(local_tz)).split('.')[0], bold)

			worksheet.write(2, 0, u"Имя организации", bold)
			worksheet.write(2, 1, u"ФЗ", bold)
			worksheet.write(2, 2, u"Уровень организации", bold)

			worksheet.write(2, 3, u"Контактное лицо", bold)
			worksheet.write(2, 4, u"Телефон", bold)
			worksheet.write(2, 5, u"Контактный E-Mail", bold)
			worksheet.write(2, 6, u"Дополнительный E-Mail", bold)

			worksheet.write(2, 7, u"Сайт организации", bold)

			worksheet.write(2, 8, u"Факс", bold)
			worksheet.write(2, 9, u"Почтовый адрес", bold)

			worksheet.write(2, 10, u"Страница на zakupki.gov.ru", bold)

			worksheet.write(2, 11, u"Дополнительные контакты", bold)
			worksheet.write(2, 12, u"Дата получения контактов", bold)

			worksheet.set_column(0, 0, 50)
			worksheet.set_column(1, 1, 10)
			worksheet.set_column(2, 2, 25)
			worksheet.set_column(3, 3, 40)
			worksheet.set_column(4, 4, 20)
			worksheet.set_column(5, 5, 30)
			worksheet.set_column(6, 6, 30)
			worksheet.set_column(7, 7, 25)
			worksheet.set_column(8, 8, 30)
			worksheet.set_column(9, 9, 20)
			worksheet.set_column(10, 10, 30)
			worksheet.set_column(11, 11, 20)
			worksheet.set_column(12, 12, 20)


			row = 4
			for org in orgs:

				if fz_value == 'FZ_223':
					contacts_obj = Contacts_223_FZ
					custLev = org.org_level_223
				elif fz_value == 'FZ_94':
					contacts_obj = Contacts_44_FZ
					custLev = org.org_level_44


				contacts = contacts_obj.objects.filter(org_id=org.id).first()

				worksheet.write(row, 0, u"" + org.org_name)
				worksheet.write(row, 1, u"" + selected_fz)
				worksheet.write(row, 2, u"" + custLev_list[custLev])
				worksheet.write(row, 3, u"" + contacts.fio)
				worksheet.write(row, 4, u"" + contacts.phone)
				worksheet.write(row, 5, u"" + contacts.email_1)
				worksheet.write(row, 6, u"" + contacts.email_2)
				worksheet.write(row, 7, u"" + contacts.company_url)
				worksheet.write(row, 8, u"" + contacts.fax)
				worksheet.write(row, 9, u"" + contacts.address)
				worksheet.write(row, 10, u"" + contacts.org_url)
				worksheet.write(row, 11, u"" + contacts.additional_contact)
				worksheet.write(row, 12, str(contacts.date_modified.replace(tzinfo=pytz.utc).astimezone(local_tz)).split('.')[0])

				row = row + 1

			worksheet.set_zoom(75)
			workbook.close()


	template = loader.get_template('index.html')
	template_args = {
		'content': 'index_content.html',
		'request': request,
		'errors': errors,
		'xlsx_file': xlsx_file,
		'regions': regions,
		'selected_region': selected_region,
		'selected_fz': selected_fz,
		'selected_level': selected_level,
		'amount_orgs': amount_orgs,
	}
	return StreamingHttpResponse(template.render(template_args, request))

def sign_out(request):
	if request.user.is_authenticated():
		logout(request)
	return HttpResponseRedirect('/')

def clear(request):
	return HttpResponseRedirect('/')