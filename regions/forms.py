from django.forms import ModelForm
from regions.models import Contact


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ('region', 'name', 'phone', 'email', 'job')