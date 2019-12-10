import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from . import models
import datetime


class ProfileForm(forms.ModelForm):
    confirm_email = forms.EmailField(
        label="confirm email",
        required=True
    )

    bio = forms.CharField(widget=forms.Textarea, 
                          min_length=10, 
                          label="biography")

    class Meta:
        model = models.Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'confirm_email',
            'dob',
            'bio',
            'avatar'
        ]

    def clean(self):
        """check that both email given in verification are identicle"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('confirm_email')

        if email != verify:
            raise forms.ValidationError("Emails do not match!")