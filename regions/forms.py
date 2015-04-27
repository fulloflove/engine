# coding: utf-8

from django.forms import ModelForm, EmailField
from regions.models import Contact
from django.utils.translation import ugettext as _


class ContactForm(ModelForm):
    email = EmailField(error_messages={'invalid': _('Your email address is incorrect')},
                       required=False,
                       label=u'E-mail')

    class Meta:
        model = Contact
        fields = ('region', 'name', 'phone', 'email', 'job')