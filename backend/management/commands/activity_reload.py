from django.core.management.base import BaseCommand

from backend.models import UserConnection


class Command(BaseCommand):
    help = 'Resets last_pulled on all user connections to force an update of all activities'

    def handle(self, *args, **options):
        users_connections = UserConnection.objects.exclude(last_pulled=None)
        for uc in users_connections:
            uc.last_pulled = None
            uc.save()
        self.stdout.write(self.style.SUCCESS('Successfully reset {} connection(s)'.format(users_connections.count())))
