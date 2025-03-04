from django.contrib import admin

from .models import (
    RentalRoom,
    RentalRoomImage,
    ChargesList,
    RoomCode,
    MonthlyChargesDetails,
    MonitoringRental
)


admin.site.register(RentalRoom)
admin.site.register(RentalRoomImage)
admin.site.register(ChargesList)
admin.site.register(RoomCode)
admin.site.register(MonthlyChargesDetails)
admin.site.register(MonitoringRental)
