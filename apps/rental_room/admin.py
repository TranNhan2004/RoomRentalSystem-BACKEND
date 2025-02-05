from django.contrib import admin

from .models import RentalRoom, ChargesList, RentalRoomImage


admin.site.register(RentalRoom)
admin.site.register(ChargesList)
admin.site.register(RentalRoomImage)