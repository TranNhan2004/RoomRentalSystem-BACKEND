from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/app.address/', include('apps.address.urls')),
    path('api/app.user-account/', include('apps.user_account.urls')),
    path('api/app.rental-room/', include('apps.rental_room.urls')),
    path('api/app.contract/', include('apps.contract.urls')),
    path('api/app.distance/', include('apps.distance.urls')),   
    path('api/app.review/', include('apps.review.urls')),   
    path('api/app.save-for-later/', include('apps.save_for_later.urls')),   
]