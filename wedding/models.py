from random import randint
from uuid import uuid1

from django.db import models
from django.utils.safestring import mark_safe
from django_extensions.db.models import TimeStampedModel
from django_hosts import reverse_lazy
from qr_code.templatetags.qr_code import qr_from_text


class Guest(TimeStampedModel):
    class Meta:
        ordering = ['sequence', 'created']

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.surname or '')

    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200, blank=True, null=True)
    party = models.ForeignKey('wedding.Party', on_delete=models.CASCADE)
    dietary_requirements = models.ManyToManyField('wedding.DietaryReq', blank=True)
    starter = models.ForeignKey('wedding.Starter', blank=True, null=True, on_delete=models.CASCADE)
    main = models.ForeignKey('wedding.Main', blank=True, null=True, on_delete=models.CASCADE)
    dessert = models.ForeignKey('wedding.Dessert', blank=True, null=True, on_delete=models.CASCADE)
    attending = models.BooleanField(default=False)
    dietary_requirements_text = models.CharField(max_length=500, blank=True, null=True)
    sequence = models.IntegerField(default=0)
    is_plus_one = models.BooleanField(default=False)


class Party(TimeStampedModel):
    def __str__(self):
        return self.description

    def guests_names(self):
        name = []
        for guest in self.guests().exclude(is_plus_one=True):
            name.append(guest.first_name)
        return ' + '.join(name)

    def guests(self):
        return Guest.objects.filter(party=self)

    def get_absolute_url(self):
        return reverse_lazy('rsvp', host='wedding', kwargs={'party_ref': self.reference})

    def qr_url(self):
        return 'https:{}'.format(self.get_absolute_url())

    def qr_code(self):
        return qr_from_text(self.qr_url(), size='3', image_format='png', border=2)

    def create_pin(self):
        pin = randint(100000, 999999)
        if Party.objects.filter(pin=pin).count() > 0:
            pin = self.create_pin()
        return pin

    def save(self, *args, **kwargs):
        if not self.pk:
            self.reference = uuid1()
            self.pin = self.create_pin()
        super().save(*args, **kwargs)

    reference = models.UUIDField(blank=True, null=True)
    pin = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=200)
    offering_hotel_room = models.BooleanField(default=False)
    offering_hotel_room_day_before = models.BooleanField(default=False)
    rsvp_responded = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(blank=True, null=True)

    # User set fields
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    wants_hotel_room = models.BooleanField(default=False)
    wants_hotel_room_day_before = models.BooleanField(default=False)


class DietaryReq(TimeStampedModel):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)


class MealOption(TimeStampedModel):
    class Meta:
        abstract = True

    def __str__(self):
        return self.description

    name = models.CharField(max_length=200)
    description = models.TextField()
    exclude_dietary_class = models.ManyToManyField(DietaryReq)


class Starter(MealOption):
    pass


class Main(MealOption):
    pass


class Dessert(MealOption):
    pass
