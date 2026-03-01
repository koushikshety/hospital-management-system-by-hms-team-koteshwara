from django.contrib import admin
from .models import Patient, Doctor, Appoint, Payment, Room, Blooddonner, Dform
from .models import *

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appoint)
admin.site.register(Payment)
admin.site.register(Room)
admin.site.register(Blooddonner)
admin.site.register(Dform)
admin.site.register(Application)
admin.site.register(Contract)
