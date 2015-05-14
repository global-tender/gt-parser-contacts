# -*- coding: utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup
import time
import xlsxwriter
import random, string

# First step, waiting user choice: request list of available regions
def getRegionList():
	errors = []
	url = 'http://www.zakupki.gov.ru/epz/organization/organization/extended/search/form.html'
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		stream = opener.open(url).read().decode('utf-8')
	except:
		errors.append(u'Ошибка, повторите позже. Debug info: step 0 (list of regions)')

	stream = stream.split('manySelect_regions')[1].split('bankDetails')[0]

	soup = BeautifulSoup(stream)

	regions = []

	for li in soup.find_all('li'):
		for input_v in li.find_all('input'):
			region_code = input_v.get('value')

		regions.append( [li.text, region_code] )
	return regions, errors

# Second step, several requests:
# 	1. Get amount of pages
#	2. Get oragnizations detail page URLs from all pages
#	3. Get detail information of all organizations

def getAmountPages(fz, region, pageNumber=1, perPage=10):
	errors = []
	pages = 1

	url = 'http://zakupki.gov.ru/epz/organization/organization/extended/search/result.html?placeOfSearch=%s&registrationStatusType=ANY&kpp=&_custLev=on&_custLev=on&_custLev=on&_custLev=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_okvedWithSubElements=on&okvedCode=&ppoCode=&address=&regionIds=%s&bik=&bankRegNum=&bankIdCode=&town=&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&spz=&_withBlocked=on&customerIdentifyCode=&_headAgencyWithSubElements=on&headAgencyCode=&_organizationsWithBranches=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&publishedOrderClause=true&_publishedOrderClause=on&unpublishedOrderClause=true&_unpublishedOrderClause=on&pageNumber=%s&searchText=&strictEqual=false&morphology=false&recordsPerPage=_%s&organizationSimpleSorting=PO_NAZVANIYU' % (
		fz, region, pageNumber, perPage)

	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		stream = opener.open(url).read().decode('utf-8')
	except:
		errors.append(u'Ошибка, повторите позже. Debug info: step 1 (pages)')

	data = re.findall( '.*<a href="javascript:goToPage\(.*\)">(.*)</a>.*', stream.split(u'<li>из</li>')[1].split('<li class="rightArrow">')[0] )
	if data:
		pages = data[0]
	return int(pages), errors

def getCompanyList(fz, region, pageNumber=1, perPage=10):
	errors = []
	url = 'http://zakupki.gov.ru/epz/organization/organization/extended/search/result.html?placeOfSearch=%s&registrationStatusType=ANY&kpp=&_custLev=on&_custLev=on&_custLev=on&_custLev=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_okvedWithSubElements=on&okvedCode=&ppoCode=&address=&regionIds=%s&bik=&bankRegNum=&bankIdCode=&town=&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&spz=&_withBlocked=on&customerIdentifyCode=&_headAgencyWithSubElements=on&headAgencyCode=&_organizationsWithBranches=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&publishedOrderClause=true&_publishedOrderClause=on&unpublishedOrderClause=true&_unpublishedOrderClause=on&pageNumber=%s&searchText=&strictEqual=false&morphology=false&recordsPerPage=_%s&organizationSimpleSorting=PO_NAZVANIYU' % (
		fz, region, pageNumber, perPage)

	kt = 0
	def strm(kt):
		kt = kt + 1
		if kt == 3:
			return None, kt
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			stream = opener.open(url).read().decode('utf-8')
			return stream, kt
		except:
			time.sleep(5)
			return strm(kt)
	stream, kt = strm(kt)

	if stream == None:
		errors.append(u'Ошибка получения детальной страницы организации: %s, %s' % (region, fz))

	soup = BeautifulSoup(stream)

	orgs = []
	organization_links = {}

	for dt in soup.find_all('dt'):
		orgs.append(dt)

	for org in orgs:
		
		for item in org.find_all('a'):
			href = item.get('href')
			if href:
				link = href

			onclick = item.get('onclick')
			if onclick:
				found_http = re.findall('\'(http.*)\'', onclick)
				if found_http:
					for http_link in found_http[0].split("', '"):
						if fz == "FZ_223" or fz == "EVERYWHERE":
							if '/223/' in http_link:
								link = http_link
								break
						if fz == "FZ_94":
							if '/pgz/' in http_link:
								link = http_link
								break

			name = item.text
			organization_links[link] = name.strip()

	return organization_links, errors

def getOrganizationContacts(url, name):
	errors = []

	contacts = {}
	contacts['Имя организации'] = name
	contacts['URL'] = url

	try:
		kt = 0
		def strm(kt):
			kt = kt + 1
			if kt == 3:
				return None, kt
			try:
				opener = urllib2.build_opener()
				opener.addheaders = [('User-agent', 'Mozilla/5.0')]
				stream = opener.open(url).read().decode('utf-8')
				return stream, kt
			except:
				time.sleep(5)
				return strm(kt)
		stream, kt = strm(kt)

		if stream == None:
			errors.append(u'Ошибка загрузки контактов по организации: %s' % name)

		if '/223/' in url:
			contacts['ФЗ'] = '№ 223-ФЗ'
			info = stream.split(u'Контактная информация')[1].split('noticeTabBoxWrapper')[1]
			soup = BeautifulSoup(info)

			for tr in soup.find_all('tr'):
				f_key = ''
				for td in tr.find_all('td'):
					if f_key == '':
						f_key = td.text.strip()
					else:
						contacts[f_key] = td.text.strip()
						f_key = ''
						break
		if '/pgz/' in url:
			contacts['ФЗ'] = '№ 44-ФЗ (94-ФЗ)'
			info = stream.split(u'Контактная информация')[1].split(u'Часовая зона')[0]
			soup = BeautifulSoup(info)

			f_key = ''
			for span in soup.find_all('span'):
				if f_key == '':
					f_key = span.text.strip()
				else:
					contacts[f_key] = span.text.strip()
					f_key = ''
					continue
	except Exception as e:
		errors.append(u"Не удалось получить контактную информацию по организации: %s (%s)" % (url, e))

	return contacts, errors