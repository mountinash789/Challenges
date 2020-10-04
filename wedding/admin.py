from django.contrib import admin

from wedding.models import Guest, Party, DietaryReq, Starter, Main, Dessert


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    pass


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    pass


@admin.register(DietaryReq)
class DietaryReqAdmin(admin.ModelAdmin):
    pass


@admin.register(Starter)
class StarterAdmin(admin.ModelAdmin):
    pass


@admin.register(Main)
class MainAdmin(admin.ModelAdmin):
    pass


@admin.register(Dessert)
class DessertAdmin(admin.ModelAdmin):
    pass
