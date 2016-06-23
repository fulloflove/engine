from django import template
from regions.models import Region, District

register = template.Library()

@register.inclusion_tag('regions/nav_list.html')
def regions_list(act_region=None):
    districts = District.objects.order_by('id')
    regions = Region.objects.order_by('region_id')
    return {'regions': regions, 'act_region': act_region, 'districts': districts}