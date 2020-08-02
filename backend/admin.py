from django.contrib import admin

from backend.models import Connection, UserConnection


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserConnection)
class UserConnectionAdmin(admin.ModelAdmin):
    pass
