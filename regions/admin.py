from django.contrib import admin
from regions.models import Region, District, Contact

admin.site.register(Region)

admin.site.register(District)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'region', 'legacy_id')

admin.site.register(Contact, ContactAdmin)