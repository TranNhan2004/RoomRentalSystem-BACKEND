from django.contrib import admin

from .models import Contract, RentalContract


admin.site.register(Contract)
admin.site.register(RentalContract)