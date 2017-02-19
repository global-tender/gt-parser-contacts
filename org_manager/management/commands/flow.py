# -*- coding: utf-8 -*-
import time
import random
from django.conf import settings
from django.utils import timezone
from django.core import mail

from org_manager.models import Organizations
from org_manager.models import Contacts_223_FZ
from org_manager.models import Contacts_44_FZ
from org_manager.models import Regions

from org_manager import utility

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

	def add_arguments(self, parser):
		# Positional arguments
		parser.add_argument('region_id', nargs='+', type=str)
		parser.add_argument('fz', nargs='+', type=str)
		parser.add_argument('sorting', nargs='+', type=str)
		parser.add_argument('sortDirection', nargs='+', type=str)
		parser.add_argument('custLev', nargs='+', type=str)


	def handle(self, *args, **options):
		self.flow(options)

	def flow(self, options):

		# regions, errors = utility.getRegionList()
		# if errors:
		# 	for error in errors:
		# 		print(error)
		# 	print('Exiting...')
		# 	return False

		# for region in regions:

		# 	reg_obj = Regions.objects.filter(region_code=region[1])
		# 	if not reg_obj:
		# 		reg_transac = Regions(
		# 			region_name = region[0],
		# 			region_code = region[1],
		# 		)
		# 		reg_transac.save()
		# print(u"\nЗакончен сбор и добавление регионов. Количество: %s\n" % len(regions))

		######################################################

		list_regions = Regions.objects.filter(id=options['region_id'][0])

		placeOfSearch_info = {
			'fz94': u'44-ФЗ',
			'fz223': u'223-ФЗ',
		}
		placeOfSearch_list = options['fz']

		sorting_info = {
			'PO_NAZVANIYU': u'По названию',
			'PO_RELEVANTNOSTI': u'По релевантности',
		}
		sorting_list = options['sorting']

		sortDirection_info = {
			'true': u'По возрастанию',
			'false': u'По убыванию',
		}
		sortDirection_list = options['sortDirection']

		# Уровень организации
		custLev_info = {
			'F': u'Федеральный уровень',
			'S': u'Уровень субъекта РФ',
			'M': u'Муниципальный уровень',
			'NOT_FSM': u'Иное',
		}
		custLev_list = options['custLev']

		recordsPerPage = '_10'
		pageNumber = '1'


		for region_obj in list_regions:

			Regions.objects.filter(region_code=region_obj.region_code).update(date_checked=timezone.now())

			print(u"Выбран регион для обработки: %s" % region_obj.region_name)

			for sorting_type in sorting_list:

				print(u"\tПереключение на тип сортировки: %s" % sorting_info[sorting_type])

				for sortDirection_type in sortDirection_list:

					print(u"\t\tПереключение на сортировку %s" % sortDirection_info[sortDirection_type])

					for placeOfSearch in placeOfSearch_list:

						print(u"\t\t\tПереключение на фильтр по ФЗ: %s" % placeOfSearch_info[placeOfSearch])

						for custLev in custLev_list:

							print(u"\t\t\t\tПереключение на фильтр по Уровню организации: %s" % custLev_info[custLev])

							pages, errors = utility.getAmountPages(region_obj.region_code, placeOfSearch, custLev, sorting_type, sortDirection_type, pageNumber, recordsPerPage)

							if errors:
								print('Errors, while fetching list of pages:')
								for error in errors:
									print(error)
								errors = []
								continue

							if pages == 0:
								print(u"\t\t\t\t\t\tнет данных\n")

							for page in range(pages):
								pg = page+1

								res, errors = utility.getCompanyList(region_obj.region_code, placeOfSearch, custLev, sorting_type, sortDirection_type, pg, recordsPerPage)

								if errors:
									print('Errors, while fetching list of companies from page %s' % pg)
									for error in errors:
										print(error)
									errors = []
									continue

								for org_url, org_name in res.iteritems():

									print("\n")
									print("\t\t\t\t\t\t" + org_name)

									Organizations.objects.filter(org_name=org_name, org_region=region_obj.region_code).update(date_checked=timezone.now())

									parsed_details, errors = utility.getOrganizationContacts(org_url, org_name)

									if errors:
										print('Errors, while fetching contact details for company: %s' % org_name)
										for error in errors:
											print(error)
										errors = []
										continue

									uid = 0
									org_obj = Organizations.objects.filter(org_name=org_name, org_region=region_obj.region_code)
									if org_obj:
										org_foreign_obj = org_obj[0]

										if placeOfSearch == 'fz223':
											Organizations.objects.filter(org_name=org_name, org_region=region_obj.region_code).update(works_with_223=True)
											Organizations.objects.filter(org_name=org_name, org_region=region_obj.region_code).update(org_level_223=custLev)

										if placeOfSearch == 'fz94':
											Organizations.objects.filter(org_name=org_name, org_region=region_obj.region_code).update(works_with_44=True)
											Organizations.objects.filter(org_name=org_name, org_region=region_obj.region_code).update(org_level_44=custLev)

										Organizations.objects.filter(org_name=org_name, org_region=region_obj.region_code).update(date_modified=timezone.now())
										print(u"\t\t\t\t\t\t\tданные организации обновлены - " + str(timezone.now()))
									else:

										if_223 = False
										if_44 = False
										org_level_223 = ""
										org_level_44 = ""
										if placeOfSearch == 'fz223':
											if_223 = True
											org_level_223 = custLev
										if placeOfSearch == 'fz94':
											if_44 = True
											org_level_44 = custLev

										org_transac = Organizations(
											org_name = org_name,
											org_region = region_obj.region_code,
											org_level_44 = org_level_44,
											org_level_223 = org_level_223,
											works_with_44 = if_44,
											works_with_223 = if_223,
											date_modified = timezone.now(),
											date_checked = timezone.now(),
										)
										org_transac.save()
										org_foreign_obj = org_transac
										print(u"\t\t\t\t\t\t\tорганизация добавлена - " + str(timezone.now()))

									if placeOfSearch == 'fz223':
										contacts_obj_name = Contacts_223_FZ
									elif placeOfSearch == 'fz94':
										contacts_obj_name = Contacts_44_FZ

									contacts_obj = contacts_obj_name.objects.filter(org_id=org_foreign_obj)
									if contacts_obj:
										contacts_obj_name.objects.filter(org_id=org_foreign_obj).update(org_url=org_url)
										contacts_obj_name.objects.filter(org_id=org_foreign_obj).update(email_1="" if u'Контактный адрес электронной почты' not in parsed_details else parsed_details[u'Контактный адрес электронной почты'])
										contacts_obj_name.objects.filter(org_id=org_foreign_obj).update(email_2="" if u'Адрес электронной почты для системных уведомлений' not in parsed_details else parsed_details[u'Адрес электронной почты для системных уведомлений'])
										contacts_obj_name.objects.filter(org_id=org_foreign_obj).update(fio="" if u'Контактное лицо' not in parsed_details else parsed_details[u'Контактное лицо'])
										contacts_obj_name.objects.filter(org_id=org_foreign_obj).update(phone="" if u'Телефон' not in parsed_details else parsed_details[u'Телефон'])
										contacts_obj_name.objects.filter(org_id=org_foreign_obj).update(fax="" if u'Факс' not in parsed_details else parsed_details[u'Факс'])
										contacts_obj_name.objects.filter(org_id=org_foreign_obj).update(address="" if u'Почтовый адрес' not in parsed_details else parsed_details[u'Почтовый адрес'])
										contacts_obj_name.objects.filter(org_id=org_foreign_obj).update(company_url="" if u'Адрес организации в сети Интернет' not in parsed_details else parsed_details[u'Адрес организации в сети Интернет'])
										contacts_obj_name.objects.filter(org_id=org_foreign_obj).update(additional_contact="" if u'Дополнительная контактная информация' not in parsed_details else parsed_details[u'Дополнительная контактная информация'])
										contacts_obj_name.objects.filter(org_id=org_foreign_obj).update(date_modified=timezone.now())
										print(u"\t\t\t\t\t\t\tобновил контактные данные организации по ФЗ: %s" % placeOfSearch)
									else:
										contacts_transac = contacts_obj_name(
											org_id = org_foreign_obj,
											org_url = org_url,
											email_1 = "" if u'Контактный адрес электронной почты' not in parsed_details else parsed_details[u'Контактный адрес электронной почты'],
											email_2 = "" if u'Адрес электронной почты для системных уведомлений' not in parsed_details else parsed_details[u'Адрес электронной почты для системных уведомлений'],
											fio = "" if u'Контактное лицо' not in parsed_details else parsed_details[u'Контактное лицо'],
											phone = "" if u'Телефон' not in parsed_details else parsed_details[u'Телефон'],
											fax = "" if u'Факс' not in parsed_details else parsed_details[u'Факс'],
											address = "" if u'Почтовый адрес' not in parsed_details else parsed_details[u'Почтовый адрес'],
											company_url = "" if u'Адрес организации в сети Интернет' not in parsed_details else parsed_details[u'Адрес организации в сети Интернет'],
											additional_contact = "" if u'Дополнительная контактная информация' not in parsed_details else parsed_details[u'Дополнительная контактная информация'],
											date_modified = timezone.now(),
										)
										contacts_transac.save()
										print(u"\t\t\t\t\t\t\tдобавил контактные данные организации по ФЗ: %s" % placeOfSearch)
									print('\t\t\t\t\t\t---------------------')
									print("\n")
			Regions.objects.filter(region_code=region_obj.region_code).update(date_completed=timezone.now())

			connection = mail.get_connection()
			connection.open()

			email = mail.EmailMessage('zakupki.global-tender.ru', u'Обработка региона "%s" завершена по указанному фильтру\n' % (region_obj.region_name), settings.DEFAULT_FROM_EMAIL,
								  settings.DEFAULT_TO_EMAIL, connection=connection)

			email.send()
			connection.close()







