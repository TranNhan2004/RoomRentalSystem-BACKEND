from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.address.urls')),
    path('api/', include('apps.user_account.urls')),
    path('api/', include('apps.rental_room.urls')),
    path('api/', include('apps.contract.urls')),
    path('api/', include('apps.chat.urls')),
    path('api/', include('apps.distance.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)