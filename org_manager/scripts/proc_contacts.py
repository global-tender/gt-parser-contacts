# -*- coding: utf-8 -*-
import os, sys
import json
import xlsxwriter
import time, random, string

errors = []

def createXLSX(contacts):
	errors = []

	def randomword(length):
		return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

	t = time.localtime( time.time() )
	t = time.strftime( '%Y-%m-%dT%H-%M-%S', t )

	filename = t + '_' + randomword(10) + '.xlsx'
	fullpath = os.getcwd() + os.sep + 'org_manager/static/xlsx/' + filename

	workbook = xlsxwriter.Workbook(fullpath)
	worksheet = workbook.add_worksheet()


	row = 1
	col = None

	worksheet.write(0, 0, "Имя организации")
	worksheet.write(0, 1, "ФЗ")
	worksheet.write(0, 2, "Контактный адрес электронной почты")
	worksheet.write(0, 3, "Контактное лицо")
	worksheet.write(0, 4, "Телефон")
	worksheet.write(0, 5, "Факс")
	worksheet.write(0, 6, "Почтовый адрес")
	worksheet.write(0, 7, "Адрес электронной почты для системных уведомлений")
	worksheet.write(0, 8, "Адрес организации в сети Интернет")
	worksheet.write(0, 9, "Страница организации на zakupki.gov.ru")

	for org_url, org_details in contacts.items():

		for org_key, org_value in org_details.items():
			if org_key == "Имя организации":
				col = 0
			elif org_key == "ФЗ":
				col = 1
			elif org_key == "Контактный адрес электронной почты":
				col = 2
			elif org_key == "Контактное лицо":
				col = 3
			elif org_key == "Телефон":
				col = 4
			elif org_key == "Факс":
				col = 5
			elif org_key == "Почтовый адрес":
				col = 6
			elif org_key == "Адрес электронной почты для системных уведомлений":
				col = 7
			elif org_key == "Адрес организации в сети Интернет":
				col = 8
			elif org_key == "URL":
				col = 9
			else:
				col = None
			if col != None:
				worksheet.write(row, col, org_value)
		row = row + 1
		col = None

	workbook.close()

	return filename, errors


filename = sys.argv[1]

fo = open(filename, 'r')
content = fo.read()
fo.close()

data = json.loads(content)

filename, errors = createXLSX(data)

if errors:
	print('error')
else:
	print(filename)