from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.address.urls')),
    path('api/', include('apps.user_account.urls')),
    path('api/', include('apps.rental_room.urls')),
    path('api/', include('apps.contract.urls')),
    path('api/', include('apps.chat.urls')),
    path('api/', include('apps.distance.urls')),   
]