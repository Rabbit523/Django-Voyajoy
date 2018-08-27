__author__ = 'eMaM'

from django.contrib.auth.models import User
from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.simple_tag()
def get_user(user):
    user_object = User.objects.get(email=user)
    name = user_object.get_full_name()
    print name
    return name
