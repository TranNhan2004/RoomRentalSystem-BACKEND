from django.contrib import admin

from .models import Province, District, Commune


admin.site.register(Province)
admin.site.register(District)
admin.site.register(Commune)