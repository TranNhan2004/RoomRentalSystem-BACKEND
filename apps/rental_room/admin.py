from django.contrib import admin
from .models import (
    RentalRoom,
    RoomImage,
    Charges,
    RoomCode,
    MonthlyRoomInvoice,
    MonitoringRental
)


admin.site.register(RentalRoom)
admin.site.register(RoomImage)
admin.site.register(Charges)
admin.site.register(RoomCode)
admin.site.register(MonthlyRoomInvoice)
admin.site.register(MonitoringRental)
