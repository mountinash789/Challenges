from uuid import uuid1

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_hosts import reverse_lazy


class Guest(TimeStampedModel):
    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.surname)

    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    party = models.ForeignKey('wedding.Party', on_delete=models.CASCADE)
    dietary_requirements = models.ManyToManyField('wedding.DietaryReq')
    starter = models.ForeignKey('wedding.Starter', blank=True, null=True, on_delete=models.CASCADE)
    main = models.ForeignKey('wedding.Main', blank=True, null=True, on_delete=models.CASCADE)
    dessert = models.ForeignKey('wedding.Dessert', blank=True, null=True, on_delete=models.CASCADE)


class Party(TimeStampedModel):
    def __str__(self):
        return self.description

    def guests_names(self):
        name = []
        for guest in self.guests():
            name.append(guest.get_full_name())
        return ', '.join(name)

    def guests(self):
        return Guest.objects.filter(party=self)

    def get_absolute_url(self):
        return reverse_lazy('rsvp', host='wedding', kwargs={'party_ref': self.reference})

    def save(self):
        if not self.pk:
            self.reference = uuid1()
        super().save()

    reference = models.UUIDField(blank=True, null=True)
    description = models.CharField(max_length=200)
    offering_hotel_room = models.BooleanField(default=False)
    offering_hotel_room_day_before = models.BooleanField(default=False)
    rsvp_responded = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(blank=True, null=True)

    # User set fields
    attending = models.BooleanField(default=False)
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
