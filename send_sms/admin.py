from django.contrib import admin
from send_sms.models import Carrier, PhoneNumber

# Register your models here.
admin.site.register(Carrier)
admin.site.register(PhoneNumber)