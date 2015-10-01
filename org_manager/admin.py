from django.contrib import admin

from org_manager.models import Organizations
from org_manager.models import Contacts_223_FZ
from org_manager.models import Contacts_44_FZ
from org_manager.models import Regions

admin.site.register(Organizations)
admin.site.register(Contacts_223_FZ)
admin.site.register(Contacts_44_FZ)
admin.site.register(Regions)
