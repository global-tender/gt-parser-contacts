#!/usr/bin/env python3

import urllib.request
import re
from bs4 import BeautifulSoup
import pprint
import time

fz = 'FZ_223'
region = '8408974'
pageNumber = '1'
perPage = '10'

all_regions = {}

def getRegionList():
	url = 'http://www.zakupki.gov.ru/epz/organization/organization/extended/search/form.html'
	stream = urllib.request.urlopen(url).read().decode('utf-8')

	stream = stream.split('manySelect_regions')[1].split('bankDetails')[0]

	soup = BeautifulSoup(stream)

	regions = {}

	for li in soup.find_all('li'):
		for input_v in li.find_all('input'):
			region_code = input_v.get('value')
		regions[li.text] = region_code
	return regions

all_regions = getRegionList()

def getAmountPages(fz, region, pageNumber=1, perPage=10):

	pages = 1

	url = 'http://zakupki.gov.ru/epz/organization/organization/extended/search/result.html?placeOfSearch=%s&registrationStatusType=ANY&kpp=&_custLev=on&_custLev=on&_custLev=on&_custLev=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_okvedWithSubElements=on&okvedCode=&ppoCode=&address=&regionIds=%s&bik=&bankRegNum=&bankIdCode=&town=&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&spz=&_withBlocked=on&customerIdentifyCode=&_headAgencyWithSubElements=on&headAgencyCode=&_organizationsWithBranches=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&publishedOrderClause=true&_publishedOrderClause=on&unpublishedOrderClause=true&_unpublishedOrderClause=on&pageNumber=%s&searchText=&strictEqual=false&morphology=false&recordsPerPage=_%s&organizationSimpleSorting=PO_NAZVANIYU' % (
		fz, region, pageNumber, perPage)

	stream = urllib.request.urlopen(url).read().decode('utf-8')
	data = re.findall( '.*<a href="javascript:goToPage\(.*\)">(.*)</a>.*', stream.split('<li>из</li>')[1].split('<li class="rightArrow">')[0] )
	if data:
		pages = data[0]
	return int(pages)

pages = getAmountPages(fz, region, pageNumber, perPage)


def getCompanyList(fz, region, pageNumber=1, perPage=10):
	url = 'http://zakupki.gov.ru/epz/organization/organization/extended/search/result.html?placeOfSearch=%s&registrationStatusType=ANY&kpp=&_custLev=on&_custLev=on&_custLev=on&_custLev=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_organizationRoleList=on&_okvedWithSubElements=on&okvedCode=&ppoCode=&address=&regionIds=%s&bik=&bankRegNum=&bankIdCode=&town=&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&_organizationTypeList=on&spz=&_withBlocked=on&customerIdentifyCode=&_headAgencyWithSubElements=on&headAgencyCode=&_organizationsWithBranches=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&_legalEntitiesTypeList=on&publishedOrderClause=true&_publishedOrderClause=on&unpublishedOrderClause=true&_unpublishedOrderClause=on&pageNumber=%s&searchText=&strictEqual=false&morphology=false&recordsPerPage=_%s&organizationSimpleSorting=PO_NAZVANIYU' % (
		fz, region, pageNumber, perPage)

	def strm():
		try:
			stream = urllib.request.urlopen(url).read().decode('utf-8')
			return stream
		except:
			time.sleep(5)
			return strm()
	stream = strm()

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
				found_http = re.findall('(http.*)\',', onclick)
				if found_http:
					for http_link in found_http:
						if '/223/' in http_link:
							link = http_link
							break

			name = item.text
			organization_links[link] = name.strip()

	return organization_links

all_links = {}
g_list = []
for page in range(pages):
	pg = page+1

	res = getCompanyList(fz, region, pg, perPage)

	all_links = dict(list(all_links.items()) + list(res.items()))

pp = pprint.PrettyPrinter(indent=4, width=200)
pp.pprint(all_links)