# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from bookingApp.models import *

admin.site.register(Listing)
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.register(Billing)
