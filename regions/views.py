from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from regions.models import Region, District, Contact
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
    contact_form = ContactForm()
    if request.method == 'POST':
        if 'contact_form' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                curr_contact = contact_form.save(commit=False)
                curr_contact.region = region
                curr_contact.save()
                contact_form = ContactForm()

    return render(request, 'regions/detail.html', {'region': region,
                                                   'contact_list': contact_list,
                                                   'last_issues': last_issues,
                                                   'contact_form': contact_form})


def edit(request, region_id):
    region = get_object_or_404(Region, pk=region_id)
    return render(request, 'regions/edit.html', {'region': region})


def submit(request, region_id):
    region = get_object_or_404(Region, pk=region_id)
    try:
        new_count = request.POST['region_count']
    except KeyError:
        # Redisplay form.
        return render(request, 'regions/edit.html', {
            'region': region,
            'error_message': "Incorrect data.",
        })
    else:
        region.region_count = new_count
        region.save()
        return HttpResponseRedirect(reverse('regions:detail', args=(region.id,)))
