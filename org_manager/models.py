from django.db import models

class Organizations(models.Model):

	class Meta:
		verbose_name = 'Organization'

	org_name            = models.CharField(max_length=1000)
	org_region          = models.CharField(max_length=1000)
	org_level           = models.CharField(max_length=1000)
	org_powers          = models.CharField(max_length=1000)
	works_with_44       = models.BooleanField(default=False)
	works_with_223      = models.BooleanField(default=False)
	date_modified       = models.DateTimeField('date modified')
	date_checked        = models.DateTimeField('date checked')

class Contacts_223_FZ(models.Model):

	class Meta:
		verbose_name = 'Contacts_223_FZ'

	org_id              = models.IntegerField(default=0)
	org_url             = models.CharField(max_length=1000)
	email_1             = models.CharField(max_length=1000, blank=True)
	email_2             = models.CharField(max_length=1000, blank=True)
	fio                 = models.CharField(max_length=1000, blank=True)
	phone               = models.CharField(max_length=1000, blank=True)
	fax                 = models.CharField(max_length=1000, blank=True)
	address             = models.CharField(max_length=1000, blank=True)
	company_url         = models.CharField(max_length=1000, blank=True)
	date_modified       = models.DateTimeField('date modified')

class Contacts_44_FZ(models.Model):

	class Meta:
		verbose_name = 'Contacts_44_FZ'

	org_id              = models.IntegerField(default=0)
	org_url             = models.CharField(max_length=1000)
	email_1             = models.CharField(max_length=1000, blank=True)
	email_2             = models.CharField(max_length=1000, blank=True)
	fio                 = models.CharField(max_length=1000, blank=True)
	phone               = models.CharField(max_length=1000, blank=True)
	fax                 = models.CharField(max_length=1000, blank=True)
	address             = models.CharField(max_length=1000, blank=True)
	company_url         = models.CharField(max_length=1000, blank=True)
	date_modified       = models.DateTimeField('date modified')

class Regions(models.Model):

	class Meta:
		verbose_name = 'Region'

	region_name         = models.CharField(max_length=1000)
	region_code         = models.CharField(max_length=1000)
	date_completed      = models.DateTimeField('date completed', null=True, blank=True)
	date_checked        = models.DateTimeField('date checked', null=True, blank=True)