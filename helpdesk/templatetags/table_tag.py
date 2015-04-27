from django import template
from helpdesk.models import Issue

register = template.Library()


@register.inclusion_tag('helpdesk/issue_table.html')
def filter_list(assignee=None, status=None):

    issues = Issue.objects.order_by('created')

    if assignee:
        issues = Issue.objects.filter(assignee=assignee).order_by('created')
    if status:
        issues = issues.filter(status=status)
    return {'requests': issues}