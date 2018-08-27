# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import django
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from rest_framework import reverse

MANAGED = True


class BaseModel(models.Model):
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()


class Place(models.Model):
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    latlng = models.CharField(db_column='latLng', max_length=255, blank=True,
                              null=True)  # Field name made lowercase. Json arr
    state = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        managed = MANAGED
        db_table = 'place'


class Billing(models.Model):
    customer_id = models.CharField(db_column='customer_Id', max_length=255, null=False)  # Field name made lowercase.
    auth_user = models.ForeignKey(User, models.DO_NOTHING, related_name='billing_auth_user', db_column='aut_user_id')
    reservation = models.ForeignKey('Reservation', models.DO_NOTHING, related_name='reservation_payment',
                                    db_column='reservation_id')
    status = models.BooleanField()
    desc = models.CharField(max_length=200, null=True)
    payment_ref = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        managed = MANAGED
        db_table = 'billing'


class City(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    locality = models.CharField(max_length=255, blank=True, null=True)
    region = models.ForeignKey('Region', models.CASCADE, related_name='city_region', db_column='region_id')
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        managed = MANAGED
        db_table = 'city'


class Listing(models.Model):
    # place = models.ForeignKey('Place', related_name='listing_place', db_column='place_id')
    region = models.ForeignKey('Region', related_name='listing_region', db_column='region_id')
    auth_user = models.ForeignKey(User, related_name='listing_creator', db_column='auth_user_id')
    owner_name = models.CharField(max_length=200, null=False)
    owner_email = models.EmailField(max_length=200, null=True)
    owner_phone = models.CharField(max_length=200, null=True)
    # owner_fees = models.FloatField(default=0)
    accomodation_fee = models.FloatField(default=0)
    amenities = models.TextField(blank=True, null=True)  # has json array
    bathrooms = models.IntegerField(blank=True, null=True)
    bedrooms = models.IntegerField(blank=True, null=True)
    cleaning_fee = models.DecimalField(default=0, decimal_places=1, max_digits=5)
    discount_rate = models.DecimalField(default=0, decimal_places=1, max_digits=5)
    headline = models.TextField(blank=True, null=True)
    house_rules_text = models.TextField(blank=True, null=True)
    neighborhood_text = models.TextField(blank=True, null=True)
    housing_type = models.CharField(max_length=255, blank=True, null=True)
    max_guests = models.IntegerField(default=0)
    min_nights = models.IntegerField(default=0)
    overview_text = models.TextField(blank=True, null=True)
    security_deposit = models.IntegerField(default=0)
    src = models.CharField(max_length=255, blank=True, null=True)
    tax_rate_percentage = models.DecimalField(default=0, decimal_places=1, max_digits=5)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)
    place_txt = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True, max_length=400)

    @property
    def review_count(self):
        return self.listing_reviews_list.count()

    @property
    def get_review_img(self):
        total_rate = 0

        for n in self.listing_reviews_list.all():
            total_rate += n.rating
        print total_rate
        print self.review_count
        if total_rate > 0:
            rate = total_rate / self.review_count
            rate = round(rate)
        else:
            rate = 0

        return '/static/img-assets/rating-{}.png'.format(rate)

    @property
    def get_amentities(self):
        if self.amenities and len(self.amenities) > 2:
            return self.amenities.replace('[', '').replace(']', '').replace(':', '').split(',')
        return None

    @property
    def get_max_guests(self):
        arr = []
        for x in range(1, self.max_guests + 1):
            arr.append(x)
        return arr

    @property
    def get_price_after_discount(self):
        return self.accomodation_fee - (self.accomodation_fee * (self.discounted_rate / 100))

    @property
    def get_absolute_url(self):
        return reverse('browse_room', args={'slug': self.slug})

    def __unicode__(self):
        return self.headline

    class Meta:
        managed = MANAGED
        db_table = 'listing'


class ListingFees(models.Model):
    listing = models.ForeignKey(Listing, related_name='listing_fees', db_column='listing_id')
    fees_name = models.CharField(max_length=150, null=False)
    fees_amount = models.FloatField(default=0)

    class Meta:
        managed = MANAGED
        db_table = 'listing_fees'


class ListingPhoto(models.Model):
    photo = models.ForeignKey('Photo', related_name='listing_photo_photos', db_column='photo_id')
    listing = models.ForeignKey(Listing, related_name='listing_photo_listing', db_column='listing_id')
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        managed = MANAGED
        db_table = 'listing_photo'


class ListingUrlMapping(models.Model):
    listing = models.ForeignKey('Listing', related_name='map_list', db_column='listing_id')
    id_airbnb = models.CharField(max_length=255, blank=True, null=True)
    id_flipkey = models.CharField(max_length=255, blank=True, null=True)
    id_vrbo = models.CharField(max_length=255, blank=True, null=True)
    tripz = models.URLField(null=True)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)

    @property
    def is_airbnb(self):
        if self.id_airbnb:
            return True
        return False

    @property
    def is_flipkey(self):
        if self.id_flipkey:
            return True
        return False

    @property
    def is_vrbo(self):
        if self.id_vrbo:
            return True
        return False

    class Meta:
        managed = MANAGED
        db_table = 'listing_url_mapping'


class Photo(models.Model):
    caption = models.TextField(blank=True, null=True)
    large = models.URLField(null=False)
    thumb = models.URLField(null=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        managed = MANAGED
        db_table = 'photo'


class Region(models.Model):
    image = models.URLField(null=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True, max_length=400)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)

    @property
    def has_properties(self):
        if self.listing_region.all().count() > 0:
            return True
        return False

    def __unicode__(self):
        return self.name

    class Meta:
        managed = MANAGED
        db_table = 'region'


class Reservation(models.Model):
    listing = models.ForeignKey('Listing', related_name='reservation_listing', db_column='listing_id')
    renter = models.ForeignKey(User, related_name='reservation_user', db_column='auth_user_id')

    arrival_date = models.DateField(null=False)
    departure_date = models.DateField(null=False)

    no_of_adults = models.IntegerField(default=0)
    no_of_childs = models.IntegerField(default=0)
    num_nights = models.IntegerField(default=0)

    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    # completed = models.BooleanField(default=False)

    cleaning_fee = models.FloatField(default=0)
    discounted_rate = models.FloatField(default=0)
    # discount_per_night = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    security_deposit = models.FloatField(default=0)
    owner_fees = models.FloatField(default=0)

    taxes = models.FloatField(default=0)
    tax_rate = models.FloatField(default=0)
    total = models.FloatField(default=0)
    total_discount = models.FloatField(default=0)

    # pricing_days_json = models.CharField(max_length=255, blank=True, null=True)
    # rental_fee = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    rental_fee_total_with_discount = models.FloatField(default=0)
    rental_fee_total_without_discount = models.FloatField(default=0)
    reservation_reply_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)

    @property
    def reservation_ref(self):
        return self.pk


    @property
    def get_reservation_status(self):
        if not self.approved and not self.rejected:
            return '<b style="color: orange">Pending</b>'
        elif self.approved:
            return '<b style="color:green;">Approved</b>'
        elif self.rejected:
            return '<b style="color: red">Not-Approved</b>'
        else:
            return '<b style="color: red">unknown</b>'


    @property
    def has_bill(self):
        if self.reservation_payment.all().count() >0:
            return True
        return False

    class Meta:
        managed = MANAGED
        db_table = 'reservation'


class ReservationFees(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='reservation_fees', db_column='reservtion_id')
    fees_name = models.CharField(max_length=150, null=False)
    fees_amount = models.FloatField(default=0)

    class Meta:
        managed = MANAGED
        db_table = 'reservation_fees'


class ListingReviews(models.Model):
    listing = models.ForeignKey('Listing', related_name='listing_reviews_list',
                                db_column='listing_id')
    review = models.ForeignKey('Review', related_name='listing_reviews_review', db_column='review_id')

    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        managed = MANAGED
        db_table = 'listing_reviews'


class ReservationSmsCounter(models.Model):
    auth_user = models.ForeignKey(User, related_name='reservation_counter_user', db_column='auth_user_id')
    counter = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        managed = MANAGED
        db_table = 'reservation_sms_counter'


class Review(models.Model):
    body = models.CharField(max_length=7000, blank=True, null=True)
    date_stayed = models.CharField(max_length=255, blank=True, null=True)
    datetime_submitted = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(default=0)
    reviewer_avatar = models.CharField(max_length=7000, blank=True, null=True)
    reviewer_location = models.CharField(max_length=7000, blank=True, null=True)
    reviewer_name = models.CharField(max_length=7000, blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=django.utils.timezone.now)
    updated_at = models.DateTimeField(default=django.utils.timezone.now)

    @property
    def get_rate_img_url(self):
        return '/static/img-assets/rating-{}.png'.format(self.rating)

    @property
    def get_rating(self):
        arr = []
        for x in range(0, self.rating):
            arr.append(x)
        return arr

    @property
    def get_remain_rate(self):
        arr = []
        base = 5
        range_ = base - self.rating
        for x in range(0, range_):
            arr.append(x)

        print len(arr)
        return arr

    class Meta:
        managed = MANAGED
        db_table = 'review'
