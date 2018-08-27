"""voyajoy_booking_dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from bookingApp import api
from bookingApp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', views.index, name='index_page'),
    url(r'^region/(?P<slug>.*)/$', views.browse_region, name='browse_region'),
    url(r'^rentals/(?P<slug>.*)$', views.room_detail, name='browse_room'),
    url(r'^booking_checkout/$', views.booking_request, name='booking_request'),
    url(r'^reservation_history/$', views.booking_list, name='booking_list'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^checkout_complete/$', views.complete_checkout, name='complete_checkout'),
    url(r'^accept/$', views.complete_checkout, name='accept'),
    url(r'^careers/$', views.careers, name='careers'),
    url(r'^tos/$', views.tos, name='tos'),
    url(r'^policy/$', views.policy, name='policy'),
    url(r'^about/$', views.about, name='about'),
    url(r'^view-reservation/(?P<reservation_id>.*)/$', views.viewBooking, name='view_reservation'),
    url(r'^accept-reservation/(?P<reservation_id>.*)/$', views.AcceptBooking, name='accept_reservation'),
    url(r'^reject-reservation/(?P<reservation_id>.*)/$', views.RejectBooking, name='reject_reservation'),

    # APIS
    url(r'^api/v1/listings$', api.create_new_listing, name='create_new_listing'),



    # serve static files
    url(r'^static/(?P<path>.*)$', django.views.static.serve,{'document_root':settings.STATIC_ROOT}),

]

urlpatterns += staticfiles_urlpatterns()

handler404 = views.handler404
handler500 = views.handler500
