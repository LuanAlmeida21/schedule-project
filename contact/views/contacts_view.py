from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from contact.models import Contact

# Create your views here.


def index(request):
    messages.add_message(request, messages.SUCCESS, 'Sucess')
    contacts = Contact.objects.filter(show=True).order_by('-id')

    paginator = Paginator(contacts, 10)  # Show 10 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Default'
    }

    return render(
        request,
        'contact/index.html',
        context
    )


def contact(request, contact_id):

    single_contact = get_object_or_404(Contact.objects.filter(pk=contact_id))

    site_title = f'{single_contact.first_name} {single_contact.last_name}'

    context = {
        'contact': single_contact,
        'site_title': site_title
    }

    return render(
        request,
        'contact/single_contact.html',
        context,
    )


def search(request):

    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('contact:index')

    contacts = Contact.objects.filter(show=True).filter(
        Q(first_name__icontains=search_value) |
        Q(last_name__icontains=search_value) |
        Q(phone__icontains=search_value) |
        Q(email__icontains=search_value)
    ).order_by('-id')

    paginator = Paginator(contacts, 10)  # Show 10 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': search_value,
        'search_value': search_value,
    }

    return render(request, 'contact/index.html', context)
