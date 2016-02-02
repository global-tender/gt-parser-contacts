from django.db import models

class Organizations(models.Model):

	class Meta:
		verbose_name = 'Organization'

	def __unicode__(self):
		return u'' + str(self.id) + '  ' + self.org_name

	org_name            = models.CharField(max_length=1000)
	org_region          = models.CharField(max_length=1000)
	
	org_level_44        = models.CharField(max_length=1000, default="", blank=True)
	org_level_223       = models.CharField(max_length=1000, default="", blank=True)

	org_powers_44       = models.CharField(max_length=1000, default="", blank=True)
	org_powers_223      = models.CharField(max_length=1000, default="", blank=True)

	works_with_44       = models.BooleanField(default=False)
	works_with_223      = models.BooleanField(default=False)
	date_modified       = models.DateTimeField('date modified')
	date_checked        = models.DateTimeField('date checked')

class Contacts_223_FZ(models.Model):

	class Meta:
		verbose_name = 'Contacts_223_FZ'

	def __unicode__(self):
		return u'' + str(self.id) + '  org_id: ' + str(self.org_id.id)

	org_id              = models.ForeignKey(Organizations)
	org_url             = models.CharField(max_length=1000)
	email_1             = models.CharField(max_length=1000, blank=True)
	email_2             = models.CharField(max_length=1000, blank=True)
	fio                 = models.CharField(max_length=1000, blank=True)
	phone               = models.CharField(max_length=1000, blank=True)
	fax                 = models.CharField(max_length=1000, blank=True)
	address             = models.CharField(max_length=1000, blank=True)
	company_url         = models.CharField(max_length=1000, blank=True)
	additional_contact  = models.CharField(max_length=1000, blank=True) # info: empty for 223fz
	date_modified       = models.DateTimeField('date modified')

class Contacts_44_FZ(models.Model):

	class Meta:
		verbose_name = 'Contacts_44_FZ'

	def __unicode__(self):
		return u'' + str(self.id) + '  org_id: ' + str(self.org_id.id)

	org_id              = models.ForeignKey(Organizations)
	org_url             = models.CharField(max_length=1000)
	email_1             = models.CharField(max_length=1000, blank=True)
	email_2             = models.CharField(max_length=1000, blank=True)
	fio                 = models.CharField(max_length=1000, blank=True)
	phone               = models.CharField(max_length=1000, blank=True)
	fax                 = models.CharField(max_length=1000, blank=True)
	address             = models.CharField(max_length=1000, blank=True)
	company_url         = models.CharField(max_length=1000, blank=True)
	additional_contact  = models.CharField(max_length=1000, blank=True)
	date_modified       = models.DateTimeField('date modified')

class Regions(models.Model):

	class Meta:
		verbose_name = 'Region'

	def __unicode__(self):
		return u'' + self.region_name + '  id: ' + str(self.id)

	region_name         = models.CharField(max_length=1000)
	region_code         = models.CharField(max_length=1000)
	date_completed      = models.DateTimeField('date completed', null=True, blank=True)
	date_checked        = models.DateTimeField('date checked', null=True, blank=True)