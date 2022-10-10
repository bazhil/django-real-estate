import random
import string

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class PropertyPublishedManager(models.Manager):
    def get_queryset(self):
        return (super(PropertyPublishedManager, self).get_queryset().filter(published_status=True))


class Property(TimeStampedUUIDModel):
    class AdvertType(models.TextChoices):
        FOR_SALE = 'For Sale', _('For Sale')
        FOR_RENT = 'For Rent', _('For Rent')
        AUCTIO = 'Auction', _('Auction')

    class PropertyType(models.TextChoices):
        HOUSE = 'House', _('House')
        PARTMENT = 'Apartment', _('Apartment')
        OFFICE = 'Office', _('Office')
        WAREHOUSE = 'Warehouse', _('Warehouse')
        COMMEARCIAL = 'Commercial', _('Commercial')
        OTHER = 'Other', _('Other')

    user = models.ForeignKey(User, verbose_name=_('Agent, seller or buyer'),
                             related_name='agent_buyer', on_delete=models.DO_NOTHING)
    title = models.CharField(verbose_name=_('Property title'), max_length=250)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    ref_code = models.CharField(verbose_name=_('Property reference code'), max_length=255,
                                unique=True, blank=True)
    description = models.TextField(verbose_name=_('Description'), default='')
    country = CountryField(verbose_name=_('Country'), default='RU', blank_label='(select country)')
    city = models.CharField(verbose_name=_('City'), max_length=180, default='Moscow')
    postal_code = models.CharField(verbose_name=_('Postal code'), max_length=100, default='140000')
    street_address = models.CharField(verbose_name=_('Street address'), max_length=180, default='Tverskaya')
    property_number = models.IntegerField(verbose_name=_('Property number'),
                                          validators=[MinValueValidator(1)],
                                          default=11)
    price = models.DecimalField(verbose_name=_('Price'), max_digits=8, decimal_places=2, default=0.0)
    tax = models.DecimalField(verbose_name=_('Property tax'), max_digits=6, decimal_places=2, default=0.13,
                              help_text='13% tax')
    plot_area = models.DecimalField(verbose_name=_('Plot area (m^2)'), max_digits=8, decimal_places=2, default=0.0)
    total_floors = models.IntegerField(verbose_name=_('Number of Floors'), default=0)
    bedrooms = models.IntegerField(verbose_name=_('Bedrooms'), default=1)
    bathrooms = models.DecimalField(verbose_name=_('Bathrooms'), max_digits=4, decimal_places=2, default=1.0)
    advert_type = models.CharField(verbose_name=_('Advert type'), max_length=50, choices=AdvertType.choices,
                                   default=AdvertType.FOR_SALE)
    property_type = models.CharField(verbose_name=_('Property Type'), max_length=50, choices=PropertyType.choices,
                                     default=PropertyType.OTHER)
    cover_photo = models.ImageField(verbose_name=_('Main photo'), default=None, null=True, blank=True)
    photo_1 = models.ImageField(default=None, null=True, blank=True)
    photo_2 = models.ImageField(default=None, null=True, blank=True)
    photo_3 = models.ImageField(default=None, null=True, blank=True)
    photo_4 = models.ImageField(default=None, null=True, blank=True)
    published_status = models.BooleanField(verbose_name=_('Published status'))
    views = models.IntegerField(verbose_name=_('Total views'), default=0)
    objects=models.Manager()
    published = PropertyPublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.description(self.description)
        self.ref_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super(Property, self).save(*args, **kwargs)

    @property
    def final_property_price(self):
        tax_percentage = self.tax
        property_price = self.price
        tax_amount = round(tax_percentage * property_price, 2)
        price_after_tax = float(round(property_price + tax_amount, 2))

        return price_after_tax


class PropertyViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_('IP Address'), max_length=250)
    property = models.ForeignKey(Property, related_name='property_views', on_delete=models.CASCADE)

    def __str__(self):
        return f'Total views on - {self.property.title} is - {self.property.views} view(s)'


    class Meta:
        verbose_name = 'Total Views on Property'
        verbose_name_plural = 'Total Property Views'
