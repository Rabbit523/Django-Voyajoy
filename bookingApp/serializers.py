from rest_framework import serializers

from bookingApp.models import Listing

__author__ = 'eMaM'


class ListingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
