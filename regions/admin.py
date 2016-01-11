from django.contrib import admin
from regions.models import Region, District, Contact


class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_id', 'name', 'gu')

admin.site.register(Region, RegionAdmin)

admin.site.register(District)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'region', 'legacy_id')

admin.site.register(Contact, ContactAdmin)