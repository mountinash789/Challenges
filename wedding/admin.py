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


class MealOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['active']


@admin.register(Starter)
class StarterAdmin(MealOptionAdmin):
    pass


@admin.register(Main)
class MainAdmin(MealOptionAdmin):
    pass


@admin.register(Dessert)
class DessertAdmin(MealOptionAdmin):
    pass
