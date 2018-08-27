from django.core.signing import JSONSerializer
from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from bookingApp.models import Listing, Region, Photo, Review, Reservation
from bookingApp.serializers import ListingSerializers

__author__ = 'eMaM'


@api_view(['POST'])
@parser_classes((JSONParser,))
def create_new_listing(request):
    data = request.data

    # check if data exist
    exist_record = Listing.objects.get(slug=slugify(data['name']))
    if exist_record:
        return Response(data=ListingSerializers(exist_record).data, status=status.HTTP_200_OK)

    try:
        # create region
        obj, created = Region.objects.get_or_create(
            image='',
            name=data['state'],
            weight=1
        )
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        # create listing
        listingRecord = Listing()
        listingRecord.region = obj
        listingRecord.owner_name = data['owner_name']
        listingRecord.owner_email = data['owner_email']
        listingRecord.owner_phone = data['owner_phone']
        listingRecord.amenities = ','.join(data['amenities'])
        listingRecord.bathrooms = data['details']['bathroom']
        listingRecord.bedrooms = data['details']['bedroom']
        listingRecord.cleaning_fee = data['other_fees']['clean_fees']
        listingRecord.discount_rate = 0
        listingRecord.accomodation_fee = data['price']
        listingRecord.headline = data['name']
        listingRecord.house_rules_text = data['rules']
        listingRecord.neighborhood_text = data['neighborhood']
        listingRecord.housing_type = data['details']['type']
        listingRecord.max_guests = int(data['max_guest'])
        listingRecord.min_nights = int(data['details']['minimum_stay'])
        listingRecord.overview_text = data['desc']
        listingRecord.security_deposit = data['other_fees']['security_deposit']
        listingRecord.src = data['src']
        listingRecord.tax_rate_percentage = data['other_fees']['tax_fees']
        listingRecord.place_txt = None
        listingRecord.slug = slugify(data['name'])
        listingRecord.auth_user_id = 1
        listingRecord.save()
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for image in data['images']:
        try:
            photo_obj = Photo(
                large=image,
                thumb=image
            )
            photo_obj.save()

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if photo_obj:
            try:
                listingRecord.listing_photo_listing.create(
                    photo=photo_obj
                )
            except Exception as e:
                return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for review in data['reviews']:
        review_record = Review(
            body=review['desc'],
            date_stayed=review['date'],
            datetime_submitted=review['date'],
            reviewer_name=review['reviewer'],
            title=review['title']
        )
        try:
            review_record.save()
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if review_record:
            try:
                listingRecord.listing_reviews_list.create(
                    review=review_record
                )
            except Exception as e:
                return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    listingRecord.map_list.create(
        tripz=data['url']
    )

    return Response(data=ListingSerializers(listingRecord).data, status=status.HTTP_201_CREATED)




@api_view(['GET'])
def reservationAccepted(request, id):
    reservation = Reservation.objects.get(pk=request.POST.get('reservation_id', None))
    reservation.approved=True
    reservation.save()
    return Response('Ok',status=status.HTTP_200_OK)