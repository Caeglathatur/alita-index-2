from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from . import forms, models


class ContactFormView(CreateView):
    model = models.Message
    form_class = forms.ContactForm
    success_url = reverse_lazy('contact-success')


class ContactFormSuccessView(TemplateView):
    template_name = 'contact_form/success.html'
