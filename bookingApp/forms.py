# -*- coding: utf-8 -*-

__author__ = 'eMaM'
from django import forms
from django.utils.translation import ugettext_lazy as _


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First Name'),
                                 widget=forms.TextInput(attrs={'placeholder': _('First Name')}), required=True)
    last_name = forms.CharField(max_length=30, label=_('Last Name'),
                                widget=forms.TextInput(attrs={'placeholder': _('Last Name')}), required=True)
    email = forms.CharField(max_length=64, label=_('Email'),
                            widget=forms.TextInput(attrs={'placeholder': _('E-mail address')}))

    # def raise_duplicate_email_error(self):
    # # here I tried to override the method, but it is not called
    #     raise forms.ValidationError(
    #         _("An account already exists with this e-mail address."
    #           " Please sign in to that account."))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.save()


class ReservationForm(forms.Form):
    arrival_date = forms.CharField(max_length=30, label='Arrival Date',
                                   widget=forms.TextInput(attrs={'placeholder': _('Arrival Date')}), required=True)
    departure_date = forms.CharField(max_length=30, label='Departure date',
                                     widget=forms.TextInput(attrs={'placeholder': _('Departure date')}), required=True)
    no_of_guest = forms.CharField(max_length=30, label='Arrival Date',
                                  widget=forms.Select(attrs={'placeholder': _('Adults')}), required=True)

    def __init__(self, *args, **kwargs):
        max_agent = kwargs.pop('no_of_agent',None)
        super(ReservationForm, self).__init__(*args, **kwargs)
        if max_agent:
            pass
