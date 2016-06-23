from django import template
from django.contrib.auth.models import User
from helpdesk.models import Project, ServiceType
from regions.models import Region

register = template.Library()


@register.inclusion_tag('helpdesk/quick_filter_menu.html')
def quick_filter_menu(active_nav=None, active_item=None):
    projects = Project.objects.all()
    service_types = ServiceType.objects.order_by('project')
    regions = Region.objects.order_by('name_short')
    users = User.objects.filter(is_active=True)
    return {'groups': {'project': projects,
                      'service_type': service_types,
                      'region': regions,
                      'user': users},
            'active_item': active_item,
            'active_nav': active_nav }
