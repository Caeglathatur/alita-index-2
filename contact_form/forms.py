from captcha.fields import CaptchaField
from django import forms

from . import models


class ContactForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = models.Message
        fields = ['subject', 'message']
