from django.contrib import admin

from backend.models import Connection, UserConnection, TargetType, ChallengeTarget, Challenge, ChallengeSubscription, \
    ActivityType, StreamType, ServiceLog


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserConnection)
class UserConnectionAdmin(admin.ModelAdmin):
    pass


@admin.register(TargetType)
class TargetTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ChallengeTarget)
class ChallengeTargetAdmin(admin.ModelAdmin):
    pass


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    pass


@admin.register(ChallengeSubscription)
class ChallengeSubscriptionTargetAdmin(admin.ModelAdmin):
    pass


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(StreamType)
class StreamTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceLog)
class ServiceLogAdmin(admin.ModelAdmin):
    pass
