from django.http import Http404
from django.shortcuts import render, get_object_or_404
from regions.models import Region, Contact
from helpdesk.models import Issue
from regions.forms import ContactForm


def index(request):
    region_list = Region.objects.order_by('region_id')
    context = {'region_list': region_list}
    return render(request, 'regions/index.html', context)


def suggest_region(request):
    reg_list = []
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        if starts_with:
            reg_list = Region.objects.filter(name_short__istartswith=starts_with)
    return render(request, 'regions/nav_list_suggest.html', {'regions': reg_list})


def detail(request, region_id):
    region = get_object_or_404(Region, pk=region_id)
    contact_list = Contact.objects.filter(region=region)
    last_issues = Issue.objects.filter(region=region)[:5]
    context = {'region': region, 'contact_list': contact_list, 'last_issues': last_issues}
    if request.method == 'POST' and ('new_contact' in request.POST or 'edit_contact' in request.POST):
        if 'new_contact' in request.POST:
            context = contact_modal_context(request, context, region_id=request.POST.get('region'))
        elif 'edit_contact' in request.POST:
            context = contact_modal_context(request, context, contact_id=request.POST.get('contact_id'))
        if context['contact_form'].is_valid():
            context['contact_form'].save()

    return render(request, 'regions/detail.html', context)


def contact_modal_context(request, context=None, contact_id=None, region_id=None):
    if context is None:
        context = {}
    if contact_id:
        context['contact_id'] = contact_id
        curr_contact = get_object_or_404(Contact, pk=contact_id)
        context['contact_form'] = ContactForm(request.POST or None, instance=curr_contact)
        context['action'] = 'edit_contact'
    elif region_id:
        initial = {'region': region_id}
        context['contact_form'] = ContactForm(request.POST or None, initial=initial)
        context['action'] = 'new_contact'
    else:
        raise Http404
    return context


def contact_modal(request, contact_id=None, region_id=None):
    context = contact_modal_context(request, contact_id=contact_id, region_id=region_id)
    return render(request, 'regions/contact_form_modal.html', context)
