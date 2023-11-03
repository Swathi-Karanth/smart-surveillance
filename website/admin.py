from django.contrib import admin
from .models import EMERGENCY_CONTACTS
from .models import Roles,staff_master
admin.site.register(EMERGENCY_CONTACTS)
admin.site.register(Roles)
admin.site.register(staff_master)

