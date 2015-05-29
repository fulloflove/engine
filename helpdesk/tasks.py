from celery import task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.template import Context


def notification_mail(context_dict, template, theme, to):
    sys_from = settings.EMAIL_ADDRESS
    plaintext = get_template('mail/' + template + '.txt')
    html = get_template('mail/' + template + '.html')
    d = Context(context_dict)
    text_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(theme, text_content, sys_from, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def issue_notification(issue, mode, to=None):
    context_dict = {'issue': issue}
    template = 'issue_' + mode
    theme = u'[{0} {1}] {2}'.format(issue.project, mode.capitalize(), issue.issue_id)
    if to is None:
        to = []
    to.append(issue.assignee.email)
    notification_mail(context_dict, template, theme, to)


@task
def issue_creation(issue):
    to = []
    if issue.project.common_email:
        to.append(issue.project.common_email)
    if issue.assignee != issue.creator:
        to.append(issue.creator.email)
    issue_notification(issue, 'new', to)


@task
def issue_info_morning(common=False):
    for user in User.objects.filter(pk=1):
        not_closed_issues = user.issues_assigned.exclude(status=4)
        expiring_tomorrow_issues = [issue for issue in not_closed_issues if issue.expires_tomorrow]
        for issue in expiring_tomorrow_issues:
            to = None
            if common:
                to = [issue.project.common_email] if issue.project.common_email else None
            issue_notification(issue, 'info', to)


@task
def issue_info_afternoon():
    issue_info_morning(common=True)


@task
def issue_assign(issue):
    issue_notification(issue, 'assign')


@task
def issue_warning():
    for user in User.objects.filter(pk=1):
        not_closed_issues = user.issues_assigned.exclude(status=4)
        expiring_today_issues = [issue for issue in not_closed_issues if issue.expires_today]
        for issue in expiring_today_issues:
            to = [issue.project.common_email] if issue.project.common_email else None
            issue_notification(issue, 'warning', to)