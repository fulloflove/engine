# coding: utf-8
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from forms import UserForm, IssueForm, ControlForm, CommentForm, DescriptionForm, ReportForm, IssuePeriodForm, \
    FilterForm
from models import Issue, Project, ServiceType, Status
from regions.models import Region
from regions.forms import ContactForm
from datetime import date, timedelta
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def issues(request, context):
    paginator = Paginator(context['issues'], 25)

    page = request.GET.get('page')
    try:
        issue_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        issue_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        issue_list = paginator.page(paginator.num_pages)
    context['issues'] = issue_list
    return render(request, 'helpdesk/issues.html', context)


@login_required
def issues_period(request, context):
    period_form = IssuePeriodForm()
    issue_list = []

    if 'period_form' in request.GET:
        period_form = IssuePeriodForm(request.GET)
        if period_form.is_valid():
            issue_list = context['issues']
            if period_form.cleaned_data.get('start'):
                start_date = period_form.cleaned_data.get('start')
                issue_list = issue_list.filter(created__gte=start_date)
            if period_form.cleaned_data.get('end'):
                end_date = period_form.cleaned_data.get('end')
                issue_list = issue_list.filter(created__lte=end_date)
            queries_without_page = request.GET.copy()
            if 'page' in queries_without_page:
                del queries_without_page['page']
            context['queries'] = queries_without_page

    context['period_form'] = period_form
    context['issues'] = issue_list
    context['title'] = _('Found issues')
    return issues(request, context)


def open_issues():
    return {'issues': Issue.objects.exclude(status=4), 'status': 'open', 'title': _('Open issues')}


def closed_issues():
    return {'issues': Issue.objects.filter(status=4), 'status': 'closed', 'title': _('Closed issues')}


@login_required
def my_issues(request, context):
    context['issues'] = context['issues'].filter(assignee=request.user)
    context['active_nav'] = 'my'
    return context


@login_required
def my_open_issues(request):
    context = my_issues(request, open_issues())
    context['title'] = _('Assigned to you')
    return issues(request, context)


@login_required
def my_closed_issues(request):
    return issues(request, my_issues(request, closed_issues()))


@login_required
def my_issues_period(request):
    return issues_period(request, my_issues(request, closed_issues()))


def all_issues(context):
    context['active_nav'] = 'all'
    return context


@login_required
def all_open_issues(request):
    return issues(request, all_issues(open_issues()))


@login_required
def all_closed_issues(request):
    return issues(request, all_issues(closed_issues()))


@login_required
def all_issues_period(request):
    return issues_period(request, all_issues(closed_issues()))


def issues_by_region(context, region_id):
    context['active_item'] = get_object_or_404(Region, pk=region_id)
    context['issues'] = context['issues'].filter(region=context['active_item'])
    context['active_nav'] = 'region'
    return context


@login_required
def open_issues_by_region(request, region_id):
    return issues(request, issues_by_region(open_issues(), region_id))


@login_required
def closed_issues_by_region(request, region_id):
    return issues(request, issues_by_region(closed_issues(), region_id))


@login_required
def closed_issues_by_region_period(request, region_id):
    return issues_period(request, issues_by_region(closed_issues(), region_id))


def issues_by_project(context, project_id):
    context['active_item'] = get_object_or_404(Project, pk=project_id)
    context['issues'] = context['issues'].filter(project=context['active_item'])
    context['active_nav'] = 'project'
    return context


@login_required
def open_issues_by_project(request, project_id):
    return issues(request, issues_by_project(open_issues(), project_id))


@login_required
def closed_issues_by_project(request, project_id):
    return issues(request, issues_by_project(closed_issues(), project_id))


@login_required
def closed_issues_by_project_period(request, project_id):
    return issues_period(request, issues_by_project(closed_issues(), project_id))


def issues_by_service_type(context, service_type_id):
    context['active_item'] = get_object_or_404(ServiceType, pk=service_type_id)
    context['issues'] = context['issues'].filter(service_type=context['active_item'])
    context['active_nav'] = 'service_type'
    return context


@login_required
def open_issues_by_service_type(request, service_type_id):
    return issues(request, issues_by_service_type(open_issues(), service_type_id))


@login_required
def closed_issues_by_service_type(request, service_type_id):
    return issues(request, issues_by_service_type(closed_issues(), service_type_id))


@login_required
def closed_issues_by_service_type_period(request, service_type_id):
    return issues_period(request, issues_by_service_type(closed_issues(), service_type_id))


def issues_by_assignee(context, assignee_id):
    context['active_item'] = get_object_or_404(User, pk=assignee_id)
    context['issues'] = context['issues'].filter(assignee=context['active_item'])
    context['active_nav'] = 'user'
    return context


@login_required
def open_issues_by_assignee(request, assignee_id):
    return issues(request, issues_by_assignee(open_issues(), assignee_id))


@login_required
def closed_issues_by_assignee(request, assignee_id):
    return issues(request, issues_by_assignee(closed_issues(), assignee_id))


@login_required
def closed_issues_by_assignee_period(request, assignee_id):
    return issues_period(request, issues_by_assignee(closed_issues(), assignee_id))


@login_required
def issue(request, issue_id, context=None):
    if context is None:
        context = {}
    current_issue = get_object_or_404(Issue, pk=issue_id)
    comment_form = CommentForm()
    description_form = DescriptionForm(instance=current_issue)
    report_form = ReportForm(instance=current_issue)
    control_form = ControlForm(instance=current_issue)
    if request.method == 'POST':
        if 'comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                curr_comment = comment_form.save(commit=False)
                curr_comment.author = request.user
                curr_comment.issue = current_issue
                curr_comment.save()
                comment_form = CommentForm()
        if 'description_form' in request.POST:
            description_form = DescriptionForm(request.POST, instance=current_issue)
            if description_form.is_valid():
                description_form.save()
                description_form = DescriptionForm(instance=current_issue)
        if 'report_form' in request.POST:
            report_form = ReportForm(request.POST, instance=current_issue)
            if report_form.is_valid():
                report_form.save()
                report_form = ReportForm(instance=current_issue)
        if 'control_form' in request.POST:
            control_form = ControlForm(request.POST, instance=current_issue)
            if control_form.is_valid():
                control_form.save()
                control_form = ControlForm(instance=current_issue)

    context['issue'] = current_issue
    context['comment_form'] = comment_form
    context['description_form'] = description_form
    context['report_form'] = report_form
    context['control_form'] = control_form
    context['status_list'] = Status.objects.all()
    return render(request, 'helpdesk/issue.html', context)


def issue_status(request, issue_id, status_id, context=None):
    if context is None:
        context = {}
    new_status = get_object_or_404(Status, pk=status_id)
    current_issue = get_object_or_404(Issue, pk=issue_id)
    if current_issue.status == new_status:
        message = "%s %s" % (_('Issue status is already set to: '), new_status)
    elif new_status == Status.objects.get(pk=4) and not current_issue.formed:
        message = _('Issue must be formed to be closed')
    elif new_status == Status.objects.get(pk=4) and not current_issue.contracts:
        message = _('Contracts must be set for issue to be closed')
    else:
        current_issue.status = new_status
        current_issue.save()
        message = "%s %s" % (_('Issue status is changed. New status: '), new_status)
    context['status_message'] = message
    return issue(request, issue_id, context)


def mail_new_issue(curr_issue):
    sys_from = settings.EMAIL_ADDRESS
    plaintext = get_template('mail/email.txt')
    html = get_template('mail/email.html')
    url = settings.BASE_URL + reverse('helpdesk:issue', args=[curr_issue.id])
    d = Context({'issue': curr_issue, 'url': url})
    text_content = plaintext.render(d)
    html_content = html.render(d)
    to = [curr_issue.creator.email]
    if curr_issue.project.common_email:
        to.append(curr_issue.project.common_email)
    if curr_issue.assignee != curr_issue.creator:
        to.append(curr_issue.assignee.email)
    theme = u"{0}. {1} {2}".format(curr_issue.project.name_short, _("New issue"), curr_issue.issue_id)
    msg = EmailMultiAlternatives(theme, text_content, sys_from, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def save_issue(form, current_user, continue_editing=False):
    curr_issue = form.save(commit=False)
    curr_region = curr_issue.region
    curr_region.region_count += 1
    curr_region.save()
    curr_issue.issue_id = 'FU-{0}-{1}-{2}'.format(curr_region.region_id,
                                                  date.today().strftime("%y"),
                                                  curr_region.region_count)
    curr_issue.creator = current_user
    curr_issue.save()
    curr_issue.save_m2m()
    mail_new_issue(curr_issue)

    if continue_editing:
        return HttpResponseRedirect(reverse('helpdesk:edit_issue', args=[curr_issue.id]))
    return HttpResponseRedirect(reverse('helpdesk:issue', args=[curr_issue.id]))


@login_required
def filter_issues(request):
    filter_form = FilterForm(request.GET)
    print request.GET.urlencode()
    issue_list = Issue.objects.filter(**request.GET)
    for item in request.GET:
        if request.GET.get(item) != '':
            print "%s %s" % (request.GET.get(item), item)
    return render(request, 'helpdesk/filter.html', {'filter_form': filter_form, 'issues': issue_list})


@login_required
def new_issue(request):
    current_user = request.user
    context = {}
    contact_form = ContactForm()

    if request.method == 'POST' and ('new_issue' in request.POST or 'continue_editing' in request.POST):
        form = IssueForm(request.POST)
        if form.is_valid():
            if 'continue_editing' in request.POST:
                return save_issue(form, current_user, True)
            return save_issue(form, current_user)

    elif request.method == 'POST' and 'new_contact' in request.POST:
        contact_form = ContactForm(request.POST)     
        if contact_form.is_valid():
            curr_region = get_object_or_404(Region, pk=contact_form['region'].value())
            contact = contact_form.save(commit=False)
            contact.region = curr_region
            contact.save()
            contact_form = ContactForm()
            submitted_data = request.POST.copy()
            submitted_data['contact'] = contact.id
            form = IssueForm(submitted_data)
            context['created_contact'] = contact
        else:
            form = IssueForm(request.POST)

    else:
        initial_data = {'control': date.today() + timedelta(days=7),
                        'assignee': current_user.id,
                        'project': 1,
                        'service_type': 4,
                        'status': 1,
                        'priority': 3,
                        'formed': False}
        form = IssueForm(initial=initial_data)

    context['form'] = form
    context['contact_form'] = contact_form
    return render(request, 'helpdesk/new_issue.html', context)


@login_required
def edit_issue(request, issue_id):
    current_issue = get_object_or_404(Issue, pk=issue_id)
    contact_form = ContactForm()
    form = IssueForm(instance=current_issue)

    if request.method == 'POST' and ('new_issue' in request.POST or 'continue_editing' in request.POST):
        form = IssueForm(request.POST or None, instance=current_issue)
        if form.is_valid():
            form.save()
            if 'continue_editing' in request.POST:
                return HttpResponseRedirect(reverse('helpdesk:edit_issue', args=[current_issue.id]))
            return HttpResponseRedirect(reverse('helpdesk:issue', args=[current_issue.id]))

    elif request.method == 'POST' and 'new_contact' in request.POST:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            new_contact = contact_form.save(commit=False)
            new_contact.region = current_issue.region
            new_contact.save()
            contact_form = ContactForm()
            current_issue.contact = new_contact
            current_issue.save()
            form = IssueForm(instance=current_issue)

    return render(request, 'helpdesk/new_issue.html', {'form': form,
                                                       'current_issue': current_issue,
                                                       'contact_form': contact_form})


@login_required
def popover(request, region_id=None):
    if region_id:
        curr_region = get_object_or_404(Region, pk=region_id)
    else:
        curr_region = None
    return render(request, 'helpdesk/popover.html', {'region': curr_region})


def accounts(request):
    return render(request, 'registration/accounts.html', {'accounts': User.objects.all()})


@login_required
def account_change(request):
    success = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            success = True
    else:
        user_form = UserForm(instance=request.user)

    return render(request, 'registration/edit_account.html', {'user_form': user_form, 'success': success})


def register(request):
    registered = False

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        if 1 == 1:
            # Save the user's form data to the database.
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()

            registered = True
        else:
            print 'errors'

    else:
        action = 1

    return render(request,
                  'helpdesk/register.html',
                  {'action': action, 'registered': registered})


def test(request, issue_id):
    test_issue = get_object_or_404(Issue, pk=issue_id)
    return render(request, 'mail/email.html', {'issue': test_issue,
                                               'url': settings.BASE_URL + reverse('helpdesk:issue', args=[test_issue.id])})