# -*- coding: utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent

from django.utils import timezone

# First step, waiting user choice: request list of available regions
def getRegionList():
	errors = []
	regions = []
	url = 'http://zakupki.gov.ru/epz/organization/extendedsearch/search.html'
	try:
		ua = UserAgent()
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', ua.random)]
		stream = opener.open(url).read().decode('utf-8')
	except Exception, e:

		if '434' in str(e): # Ведутся регламентные работы (страницы вернула HTTP Status 434)
			print("--- Ведутся регламентные работы, следующая попытка запроса через 1 час. " + str(timezone.now()))
			time.sleep(3600) # Ждем 1 час, пробуем снова
			return getRegionList()

		errors.append(u'Ошибка, повторите позже. Debug info: step 0 (list of regions)')
		return regions, errors

	soup = BeautifulSoup(stream, 'html.parser')

	st = soup.find_all('ul', {'id':'regionsTagDataContainer'})[0]

	for li in st.find_all('li'):
		input_id = li.find_all('input')[0]
		region_code = str(input_id.get('id').split("_")[-1])

		regions.append( [li.text, region_code] )

	return regions, errors

# Second step, several requests:
# 	1. Get amount of pages
#	2. Get oragnizations detail page URLs from all pages
#	3. Get detail information of all organizations

def getAmountPages(regionIds, placeOfSearch, custLev, sorting_type, sortDirection, pageNumber='1', recordsPerPage='_10'):
	errors = []
	pages = 1
	stream = False

	url = 'http://zakupki.gov.ru/epz/organization/extendedsearch/results.html?searchString=&morphology=on&openMode=USE_DEFAULT_PARAMS&pageNumber=%s&sortDirection=%s&recordsPerPage=%s&sortBy=%s&registered94=on&notRegistered=on&registered223=on&blocked=on&inn=&ogrn=&kpp=&organizationRoleList=&okvedIds=&ppoIds=&address=&districtIds=&regions=%s%s%s' % (
		pageNumber, sortDirection, recordsPerPage, sorting_type, regionIds, '&'+placeOfSearch+'=on', '&'+custLev+'=on')

	kt = 0
	def strm(kt):
		kt = kt + 1
		if kt == 4:
			return None, kt
		try:
			delays = [15,20,25,30,35]
			time.sleep(random.choice(delays))

			ua = UserAgent()
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', ua.random)]
			stream = opener.open(url).read().decode('utf-8')
			return stream, kt
		except Exception, e:

			if '434' in str(e): # Ведутся регламентные работы (страницы вернула HTTP Status 434)
				print("--- Ведутся регламентные работы, следующая попытка запроса через 1 час. " + str(timezone.now()))
				time.sleep(3600) # Ждем 1 час, пробуем снова
				kt = 0
				return strm(kt)

			delays = [80,90,100,110]
			time.sleep(random.choice(delays))
			return strm(kt)
	stream, kt = strm(kt)

	if stream == None:
		errors.append(u'Ошибка получения количества страниц (pages) по региону: %s, %s' % (regionIds, placeOfSearch))
		return 0, errors


	if u'Поиск не дал результатов' in stream:
		pages = 0
		return pages, errors

	if 'javascript:goToPage' not in stream:
		pages = 1
		return pages, errors

	soup = BeautifulSoup(stream, 'html.parser')
	st = soup.find_all('li', {'class':'rightArrow'})[0]
	ahref = st.find_all('a')[0]
	pages = re.findall('javascript:goToPage\((.*)\)', str(ahref.get('href')))[0]

	return int(pages), errors

def getCompanyList(regionIds, placeOfSearch, custLev, sorting_type, sortDirection, pageNumber='1', recordsPerPage='_10'):
	errors = []
	organization_links = {}

	url = 'http://zakupki.gov.ru/epz/organization/extendedsearch/results.html?searchString=&morphology=on&openMode=USE_DEFAULT_PARAMS&pageNumber=%s&sortDirection=%s&recordsPerPage=%s&sortBy=%s&registered94=on&notRegistered=on&registered223=on&blocked=on&inn=&ogrn=&kpp=&organizationRoleList=&okvedIds=&ppoIds=&address=&districtIds=&regions=%s%s%s' % (
		pageNumber, sortDirection, recordsPerPage, sorting_type, regionIds, '&'+placeOfSearch+'=on', '&'+custLev+'=on')

	kt = 0
	def strm(kt):
		kt = kt + 1
		if kt == 4:
			return None, kt
		try:
			ua = UserAgent()
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', ua.random)]
			stream = opener.open(url).read().decode('utf-8')
			return stream, kt
		except Exception, e:

			if '434' in str(e): # Ведутся регламентные работы (страницы вернула HTTP Status 434)
				print("--- Ведутся регламентные работы, следующая попытка запроса через 1 час. " + str(timezone.now()))
				time.sleep(3600) # Ждем 1 час, пробуем снова
				kt = 0
				return strm(kt)

			delays = [80,90,100,110]
			time.sleep(random.choice(delays))
			return strm(kt)
	stream, kt = strm(kt)

	if stream == None:
		errors.append(u'Ошибка получения списка организаций: %s, %s' % (regionIds, placeOfSearch))
		return organization_links, errors

	soup = BeautifulSoup(stream, 'html.parser')

	st = soup.find_all('td', {'class':'descriptTenderTd'})

	for td in st:
		for a in td.find_all('a'):
			if a.get('href'):
				link = a.get('href')
			elif a.get('onclick'):
				found_http = re.findall('\'(http.*)\'', a.get('onclick'))
				for http_link in found_http[0].split("', '"):
					if placeOfSearch == 'fz223':
						if '/223/' in http_link:
							link = http_link
							break
					if placeOfSearch == 'fz94':
						if '/pgz/' in http_link:
							link = http_link
							break

			organization_links[link] = a.text.strip()

	return organization_links, errors

def getOrganizationContacts(url, name):
	errors = []

	contacts = {}
	contacts[u'Имя организации'] = unicode(name)
	contacts[u'URL'] = url

	try:
		kt = 0
		def strm(kt):
			kt = kt + 1
			if kt == 4:
				return None, kt
			try:
				delays = [15,20,25,30,35]
				time.sleep(random.choice(delays))
				ua = UserAgent()
				opener = urllib2.build_opener()
				opener.addheaders = [('User-agent', ua.random)]
				stream = opener.open(url).read().decode('utf-8')
				return stream, kt
			except Exception, e:

				print('__ Getting contacts exception (repeating): ' + str(e))

				if '434' in str(e): # Ведутся регламентные работы (страницы вернула HTTP Status 434)
					print("--- Ведутся регламентные работы, следующая попытка запроса через 1 час. " + str(timezone.now()))
					time.sleep(3600) # Ждем 1 час, пробуем снова
					kt = 0
					return strm(kt)

				delays = [80,90,100,110]
				time.sleep(random.choice(delays))
				return strm(kt)
		stream, kt = strm(kt)

		if stream == None:
			errors.append(u'Ошибка загрузки контактов по организации: %s' % name)

		if '/223/' in url:
			contacts['ФЗ'] = '№ 223-ФЗ'
			info = stream.split(u'Контактная информация')[1].split('noticeTabBoxWrapper')[1]
			soup = BeautifulSoup(info, 'html.parser')

			for tr in soup.find_all('tr'):
				f_key = ''
				for td in tr.find_all('td'):
					if f_key == '':
						f_key = unicode(td.text.strip())
					else:
						contacts[f_key] = unicode(td.text.strip())
						f_key = ''
						break
		if '/pgz/' in url:
			contacts[u'ФЗ'] = u'№ 44-ФЗ (94-ФЗ)'
			info = stream.split(u'Контактная информация')[1].split(u'Часовая зона')[0]
			soup = BeautifulSoup(info, 'html.parser')

			f_key = ''
			for span in soup.find_all('span'):
				if f_key == '':
					f_key = unicode(span.text.strip())
				else:
					contacts[f_key] = unicode(span.text.strip())
					f_key = ''
					continue
	except Exception as e:
		errors.append(u"Не удалось получить контактную информацию по организации, возможно не зарегистрирована или заблокирована: %s (%s)" % (url, e))

	return contacts, errors
