from django.contrib import admin

from .models import CustomUser, Lessor, Renter, Manager


admin.site.register(CustomUser)
admin.site.register(Lessor)
admin.site.register(Renter)
admin.site.register(Manager)