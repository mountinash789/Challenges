from django.contrib import admin

from wedding.models import Guest, Party, DietaryReq, Starter, Main, Dessert


class GuestAdmin(admin.StackedInline):
    model = Guest
    extra = 1


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    change_form_template = 'wedding/admin/add_form.html'
    inlines = [
        GuestAdmin,
    ]


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
