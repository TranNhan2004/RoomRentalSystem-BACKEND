from django.contrib import admin

from .models import RentalRoom, RentalRoomImage, RoomChargesList, ElectricityWaterChargesList, OtherChargesList


admin.site.register(RentalRoom)
admin.site.register(RentalRoomImage)
admin.site.register(RoomChargesList)
admin.site.register(ElectricityWaterChargesList)
admin.site.register(OtherChargesList)