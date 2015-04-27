from django.contrib import admin
from helpdesk.models import Project, Priority, Component, ServiceType, Source, Status, Issue, Comment, Contract

admin.site.register(Project)
admin.site.register(Priority)
admin.site.register(Component)
admin.site.register(Contract)


class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_short', 'name_full', 'project')

admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(Source)
admin.site.register(Status)
admin.site.register(Issue)
admin.site.register(Comment)
